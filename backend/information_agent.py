import os
from pydantic import BaseModel, Field
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
from config import EMBEDDING_MODEL, LLM_MODEL

load_dotenv()

# 1. Define the final output structure using Pydantic
class LegalAnalysis(BaseModel):
    topic_name: str = Field(description="The overarching topic or title of the legal document.")
    short_description: str = Field(description="A brief 1-2 sentence description of what this document covers.")
    summary: str = Field(description="An easy-to-understand summary under 250 words, perfectly suited for non-legal users based on document context and web research.")
    key_rights: str = Field(description="Key rights granted or protected by this document.")
    important_provisions: str = Field(description="Crucial clauses, rules, or provisions mentioned.")
    important_penalties: str = Field(description="Any penalties, fines, or legal consequences outlined.")
    who_can_benefit: str = Field(description="The specific individuals, groups, or entities who benefit from this document.")
    web_context_additions: str = Field(description="Important external real-world context, updates, or clarifications found via web search regarding this legal topic.")

def extract_field_with_rag(retriever, llm, field_name, extraction_instruction):
    """Queries the local vector store for chunks relevant to a specific heading."""
    query = f"Find all details regarding: {field_name}. Focus on {extraction_instruction}"
    relevant_docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert legal researcher. Analyze the provided legal text chunks "
            "and extract information strictly relevant to the field: '{field_name}'.\n"
            "Instructions for this field: {instruction}\n"
            "If the information is not present in the text, write 'Not specified in the document.' "
            "Do not make things up."
        )),
        ("user", "Relevant Text Chunks:\n\n{context}\n\nExtracted Clean Info:")
    ])
    
    chain = prompt | llm
    response = chain.invoke({
        "field_name": field_name,
        "instruction": extraction_instruction,
        "context": context
    })
    return response.content

def run_vector_information_agent():
    """
    Processes all PDF files in legal_documents/ folder and returns extracted legal information as JSON-compatible format.
    Returns a list of dictionaries, each containing legal analysis for one document.
    """
    loader = PyPDFDirectoryLoader("legal_documents/")
    all_pages = loader.load()
    
    if not all_pages:
        print("No documents found in the 'legal_documents/' folder.")
        return []

    # Group pages by source document
    docs_by_source = {}
    for page in all_pages:
        source = page.metadata.get('source')
        if source not in docs_by_source:
            docs_by_source[source] = []
        docs_by_source[source].append(page)

    # Initialize LLM, Embeddings, and Web Search Tool
    llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0.1)
    structured_llm = llm.with_structured_output(LegalAnalysis)
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    search_tool = DuckDuckGoSearchRun()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    # List to store all extracted legal information
    all_topics = []
    doc_index = 0

    for source, pages in docs_by_source.items():
        doc_name = os.path.basename(source)
        print(f"\nProcessing document: {doc_name}...")
        
        try:
            chunks = text_splitter.split_documents(pages)
            doc_vector_store = Chroma.from_documents(
                chunks, 
                embeddings, 
                persist_directory=f"./chroma_databases/temp_chroma_{doc_name.replace('.', '_')}"
            )
            retriever = doc_vector_store.as_retriever(search_kwargs={"k": 5}) 

            print(f"Extracting legal information...")
            rights_info = extract_field_with_rag(retriever, llm, "Key Rights", "Identify explicit legal rights given to individuals or entities.")
            provisions_info = extract_field_with_rag(retriever, llm, "Important Provisions", "Identify critical operational clauses, definitions, and rules.")
            penalties_info = extract_field_with_rag(retriever, llm, "Important Penalties", "Identify specific legal penalties, fines, termination terms, or consequences.")
            benefits_info = extract_field_with_rag(retriever, llm, "Who Can Benefit", "Identify the core target audience, beneficiaries, or protected parties.")
            
            # Dynamic Web Search execution
            print("Fetching web context...")
            preview_chunks = retriever.invoke("Overview, title, act name, or scope")
            preview_text = "\n".join([c.page_content for c in preview_chunks[:2]])
            
            query_generation_prompt = ChatPromptTemplate.from_messages([
                ("system", "Based on this text snippet from a legal document, generate a single, highly effective search engine query to find recent news, real-world implementations, or government updates about this topic. Return only the raw query string."),
                ("user", "{preview}")
            ])
            
            query_chain = query_generation_prompt | llm | StrOutputParser()
            search_query = query_chain.invoke({"preview": preview_text}).strip().replace('"', '')
            
            print(f"   Web Query: {search_query}")
            try:
                web_results = search_tool.invoke(search_query)
            except Exception as e:
                web_results = "Could not fetch online details at this time."
                print(f"   Web search error: {e}")

            # Final aggregation with Pydantic structure
            print("Formatting legal analysis...")
            final_formatting_prompt = ChatPromptTemplate.from_messages([
                ("system", (
                    "You are a master legal summarizer. Your job is to take raw, isolated findings "
                    "about a legal document along with real-time web research findings, and map them into a flawless structured layout. "
                    "Ensure the 'summary' field remains strictly under 250 words and is tailored for non-legal readers. "
                    "Synthesize the web insights clearly into the 'web_context_additions' field."
                )),
                ("user", (
                    "Raw Document Data:\n"
                    "- Pre-extracted Rights: {pre_rights}\n"
                    "- Pre-extracted Provisions: {pre_provisions}\n"
                    "- Pre-extracted Penalties: {pre_penalties}\n"
                    "- Pre-extracted Beneficiaries: {pre_benefits}\n\n"
                    "Live Web Search Context:\n{web_data}"
                ))
            ])
            
            formatting_chain = final_formatting_prompt | structured_llm
            analysis = formatting_chain.invoke({
                "pre_rights": rights_info,
                "pre_provisions": provisions_info,
                "pre_penalties": penalties_info,
                "pre_benefits": benefits_info,
                "web_data": web_results
            })
            
            # Convert Pydantic model to dictionary
            analysis_dict = {
                "_id": str(doc_index),
                "name": analysis.topic_name,
                "shortDescription": analysis.short_description,
                "summary": analysis.summary,
                "keyRights": analysis.key_rights,
                "importantProvisions": analysis.important_provisions,
                "importantPenalties": analysis.important_penalties,
                "whoCanBenefit": analysis.who_can_benefit,
                "webContext": analysis.web_context_additions
            }
            
            all_topics.append(analysis_dict)
            doc_index += 1
            
            # Display the results
            print("=" * 60)
            print(f"✅ Processed: {doc_name}")
            print("=" * 60)
            print(f"Topic: {analysis.topic_name}")
            print(f"Description: {analysis.short_description[:100]}...")
            print("-" * 60)
            
            # Clean up database resources
            doc_vector_store.delete_collection()
            
        except Exception as e:
            print(f"❌ Error processing {doc_name}: {e}")
            continue

    print(f"\n✅ Successfully processed {len(all_topics)} document(s)")
    return all_topics

if __name__ == "__main__":
    import json
    results = run_vector_information_agent()
    print("\n" + "=" * 60)
    print("FINAL JSON OUTPUT FOR FRONTEND:")
    print("=" * 60)
    print(json.dumps(results, indent=2))
    print("=" * 60)