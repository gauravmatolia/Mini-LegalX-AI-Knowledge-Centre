import os
from langchain_classic.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from config import EMBEDDING_MODEL, LLM_MODEL
from dotenv import load_dotenv


load_dotenv()
def initialize_rag_system():
    print("Initializing RAG System...")
    
    # 1. Load documents
    loader = PyPDFDirectoryLoader("legal_documents/")
    documents = loader.load()
    if not documents:
        raise ValueError("No documents found in 'legal_documents/'. Please add files first.")

    # 2. Split text into manageable chunks for accurate context retrieval
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)

    # 3. Embed chunks and store in a local vector database
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vector_store = Chroma.from_documents(splits, embeddings, persist_directory="./chroma_db")
    
    # 4. Create retriever
    retriever = vector_store.as_retriever(search_kwargs={"k": 5}) # Retrieves top 5 relevant context blocks
    return retriever

def create_legal_assistant_chain(retriever):
    llm = ChatGoogleGenerativeAI(model=LLM_MODEL)

    # Define system prompt to keep the AI grounded in the source text
    system_prompt = (
        "You are an expert legal assistant. Answer the user's question using exclusively the provided context. "
        "If you do not know the answer or if it's not present in the context, say that you cannot find it in the provided documents. "
        "Do not make up information. Provide citations (document name/page if available) in your answer.\n\n"
        "Context:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # Combine documents and create retrieval chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    return rag_chain

def main():
    try:
        retriever = initialize_rag_system()
        rag_chain = create_legal_assistant_chain(retriever)
        
        print("\n✅ Legal Assistant is ready! Type 'exit' to quit.\n")
        
        while True:
            query = input("Ask a question about your legal documents: ")
            if query.lower() == 'exit':
                break
                
            if not query.strip():
                continue
                
            response = rag_chain.invoke({"input": query})
            
            print("\n🤖 Assistant Answer:")
            print(response["answer"])
            print("-" * 50 + "\n")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()