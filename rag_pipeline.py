"""
rag_pipeline.py - Fixed with retry logic + fallback models
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

from data_loader import EduDataLoader

load_dotenv()

SYSTEM_PROMPT = """You are Edugator, a friendly educational guidance assistant for Indian students.
Help students with: stream selection after 10th/12th, entrance exams (JEE, NEET, UPSC, TNPSC, SSC, Banking),
career guidance, government jobs, IT careers, higher studies, and placement preparation.

Be warm, encouraging, and give step-by-step guidance tailored to the Indian education system.

Context from knowledge base:
{context}

Student's Question: {question}

Answer (be detailed and encouraging, use bullet points for clarity):"""

# Models to try in order (free tier, slowest quota first)
MODELS_TO_TRY = [
    "gemini-2.5-flash",
]

class EduGatorRAG:

    def __init__(self):
        self.vectorstore    = None
        self.embeddings     = None
        self.llm            = None
        self.vector_db_path = "vector_db"
        self.working_model  = None

    def initialize(self):
        print("📂 Loading educational data...")
        self._setup_embeddings()
        self._load_or_build_vectorstore()
        self._setup_llm()
        print("✅ RAG pipeline ready!")

    def _setup_embeddings(self):
        print("🔡 Loading embedding model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
        print("✅ Embeddings ready!")

    def _load_or_build_vectorstore(self):
        faiss_index = os.path.join(self.vector_db_path, "index.faiss")
        if os.path.exists(faiss_index):
            print("📦 Loading existing FAISS vector store...")
            self.vectorstore = FAISS.load_local(
                self.vector_db_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print("✅ Vector store loaded!")
        else:
            print("🔨 Building new vector store...")
            self._build_vectorstore()

    def _build_vectorstore(self):
        loader    = EduDataLoader()
        documents = loader.load_all()
        if not documents:
            print("⚠️  No files in data/ — using built-in knowledge base.")
            documents = loader.get_fallback_docs()

        print(f"📄 Loaded {len(documents)} documents")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", "!", "?", ",", " "]
        )
        chunks = splitter.split_documents(documents)
        print(f"✂️  Split into {len(chunks)} chunks")

        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        Path(self.vector_db_path).mkdir(exist_ok=True)
        self.vectorstore.save_local(self.vector_db_path)
        print(f"💾 Vector store saved!")

    def _setup_llm(self):
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ GOOGLE_API_KEY not found in .env!")

        # Try each model and pick first one that works
        for model_name in MODELS_TO_TRY:
            try:
                print(f"🤖 Trying model: {model_name} ...")
                llm = ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=api_key,
                    temperature=0.4,
                    max_output_tokens=1024,
                    convert_system_message_to_human=True
                )
                # Quick test to verify it works
                test = llm.invoke("Say OK")
                print(f"✅ Model {model_name} is working!")
                self.llm          = llm
                self.working_model = model_name
                return
            except Exception as e:
                err = str(e)
                if "429" in err or "RESOURCE_EXHAUSTED" in err:
                    print(f"   ⚠️  {model_name} quota exceeded, trying next...")
                    time.sleep(2)
                elif "404" in err or "not found" in err.lower():
                    print(f"   ⚠️  {model_name} not available, trying next...")
                else:
                    print(f"   ❌ {model_name} error: {err[:80]}")

        raise ValueError(
            "❌ All Gemini models exhausted quota.\n"
            "   Wait 1 minute and restart, or get a new API key from:\n"
            "   https://makersuite.google.com/app/apikey"
        )

    def _call_llm_with_retry(self, prompt_text: str) -> str:
        """Call LLM with automatic retry on quota errors."""
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

        for attempt in range(3):   # try up to 3 times
            for model_name in MODELS_TO_TRY:
                try:
                    llm = ChatGoogleGenerativeAI(
                        model=model_name,
                        google_api_key=api_key,
                        temperature=0.4,
                        max_output_tokens=1024,
                        convert_system_message_to_human=True
                    )
                    response = llm.invoke(prompt_text)
                    return response.content if hasattr(response, "content") else str(response)

                except Exception as e:
                    err = str(e)
                    if "429" in err or "RESOURCE_EXHAUSTED" in err:
                        print(f"   ⏳ Quota hit on {model_name}, waiting 10s...")
                        time.sleep(10)
                        continue
                    else:
                        raise e

        return "I'm temporarily unavailable due to API limits. Please wait 1 minute and try again."

    def get_answer(self, question: str, chat_history: list = None) -> dict:
        try:
            # Step 1: Retrieve relevant chunks
            retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
            docs = retriever.invoke(question)

            # Step 2: Build context
            context = "\n\n".join([doc.page_content for doc in docs])

            # Step 3: Fill prompt
            prompt = PromptTemplate(
                input_variables=["context", "question"],
                template=SYSTEM_PROMPT
            )
            filled_prompt = prompt.format(context=context, question=question)

            # Step 4: Call LLM with retry logic
            answer = self._call_llm_with_retry(filled_prompt)

            # Step 5: Sources
            sources = []
            for doc in docs:
                src = doc.metadata.get("source", "Knowledge Base")
                if src not in sources:
                    sources.append(src)

            return {"answer": answer, "sources": sources[:3]}

        except Exception as e:
            print(f"❌ Error in get_answer: {e}")
            return {
                "answer": "I'm having trouble right now. Please wait a moment and try again.",
                "sources": []
            }

    def rebuild_vectorstore(self):
        import shutil
        if os.path.exists(self.vector_db_path):
            shutil.rmtree(self.vector_db_path)
        self._build_vectorstore()
        print("✅ Vector store rebuilt!")