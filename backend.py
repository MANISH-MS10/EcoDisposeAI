import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI(title="EcoDispose AI Core API")

# Cloud-Safe API Key Configuration
if "GOOGLE_API_KEY" not in os.environ or not os.environ["GOOGLE_API_KEY"]:
    import dotenv
    dotenv.load_dotenv()

class QueryRequest(BaseModel):
    question: str

retriever = None
rag_chain = None

@app.on_event("startup")
def initialize_rag():
    global retriever, rag_chain
    try:
        if not os.path.exists("ewaste_policy.pdf"):
            print("❌ Error: 'ewaste_policy.pdf' missing from root folder!")
            return
            
        loader = PyPDFLoader("ewaste_policy.pdf")
        docs = loader.load()
        
        # FIXED: Removed duplicate blocks and tuned chunk size to 500 for fast processing
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(docs)
        
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        
        # FIXED: Removed duplicate vectorstore creation line to prevent memory crashes
        vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db_store")
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
        
        system_prompt = (
            "You are an expert urban e-waste coordinator. Answer the user's inquiry clearly using the "
            "provided context. If the exact answer isn't in the context, guide them using general environmental safety principles.\n\n"
            "Context:\n{context}"
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        qa_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, qa_chain)
        print("✅ LangChain Engine & ChromaDB Vector Core Ready!")
    except Exception as e:
        print(f"❌ Core Initialization Failed: {str(e)}")

@app.post("/api/chat")
async def handle_chat(payload: QueryRequest):
    if not rag_chain:
        raise HTTPException(status_code=503, detail="AI engine is initializing or data file is unreadable.")
    try:
        response = rag_chain.invoke({"input": payload.question})
        return {"answer": response["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))