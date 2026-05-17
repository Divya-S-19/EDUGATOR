"""
diagnose.py - Run this to find ALL problems in your Edugator setup
Just run: python diagnose.py
"""

import sys
import os

print("=" * 55)
print("  EDUGATOR DIAGNOSTIC TOOL")
print("=" * 55)

# ── 1. Python version ──────────────────────────────────────
print("\n[1] Python Version")
print(f"    {sys.version}")
if sys.version_info < (3, 9):
    print("    ❌ Need Python 3.9 or higher!")
else:
    print("    ✅ Python version OK")

# ── 2. Check .env file ─────────────────────────────────────
print("\n[2] Checking .env file")
if os.path.exists(".env"):
    print("    ✅ .env file found")
    with open(".env") as f:
        content = f.read()
    if "GOOGLE_API_KEY" in content:
        key_line = [l for l in content.splitlines() if "GOOGLE_API_KEY" in l]
        val = key_line[0].split("=", 1)[-1].strip() if key_line else ""
        if val and val != "your_gemini_api_key_here" and len(val) > 10:
            print(f"    ✅ GOOGLE_API_KEY is set ({val[:8]}...)")
        else:
            print("    ❌ GOOGLE_API_KEY is empty or still has placeholder!")
            print("       Fix: paste your real key from makersuite.google.com")
    else:
        print("    ❌ GOOGLE_API_KEY not found in .env!")
        print("       Fix: add line → GOOGLE_API_KEY=your_key_here")
else:
    print("    ❌ .env file NOT found!")
    print("       Fix: create a file named .env in this folder")
    print("       Contents:")
    print("         GOOGLE_API_KEY=your_key_here")

# ── 3. Check required packages ─────────────────────────────
print("\n[3] Checking installed packages")

packages = {
    "flask":                    "flask",
    "flask_cors":               "flask-cors",
    "dotenv":                   "python-dotenv",
    "langchain":                "langchain",
    "langchain_community":      "langchain-community",
    "langchain_core":           "langchain-core",
    "langchain_google_genai":   "langchain-google-genai",
    "sentence_transformers":    "sentence-transformers",
    "faiss":                    "faiss-cpu",
    "pypdf":                    "pypdf",
}

missing = []
for module, pip_name in packages.items():
    try:
        __import__(module)
        print(f"    ✅ {pip_name}")
    except ImportError:
        print(f"    ❌ {pip_name}  ← NOT installed")
        missing.append(pip_name)

if missing:
    print(f"\n    👉 Run this to fix:")
    print(f"       pip install {' '.join(missing)}")

# ── 4. Check project files ─────────────────────────────────
print("\n[4] Checking project files")

required_files = [
    "app.py",
    "rag_pipeline.py",
    "data_loader.py",
    "requirements.txt",
    "templates/index.html",
    "static/style.css",
    "static/script.js",
]

for f in required_files:
    if os.path.exists(f):
        size = os.path.getsize(f)
        if size < 50:
            print(f"    ⚠️  {f} exists but looks EMPTY ({size} bytes)")
        else:
            print(f"    ✅ {f}  ({size} bytes)")
    else:
        print(f"    ❌ {f}  ← FILE MISSING")

# ── 5. Check folders ────────────────────────────────────────
print("\n[5] Checking folders")
for folder in ["templates", "static", "data", "vector_db"]:
    if os.path.exists(folder):
        print(f"    ✅ {folder}/")
    else:
        if folder == "vector_db":
            print(f"    ℹ️  {folder}/ — will be created on first run (OK)")
        else:
            print(f"    ❌ {folder}/  ← FOLDER MISSING — create it!")

# ── 6. Test Gemini connection ──────────────────────────────
print("\n[6] Testing Gemini API connection")
try:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("    ⚠️  Skipping — no valid API key in .env")
    else:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content("Say hello in one word")
        print(f"    ✅ Gemini connected! Response: {resp.text.strip()}")
except ImportError:
    print("    ❌ google-generativeai not installed")
    print("       Run: pip install google-generativeai")
except Exception as e:
    print(f"    ❌ Gemini error: {e}")
    if "API_KEY_INVALID" in str(e) or "invalid" in str(e).lower():
        print("       Fix: your API key is wrong — get a new one from makersuite.google.com")
    elif "quota" in str(e).lower():
        print("       Fix: API quota exceeded — wait or use a different key")

# ── 7. Test embeddings ─────────────────────────────────────
print("\n[7] Testing HuggingFace embeddings")
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    vec = model.encode(["test"])
    print(f"    ✅ Embeddings working! Vector size: {vec.shape[1]}")
except ImportError:
    print("    ❌ sentence-transformers not installed")
    print("       Run: pip install sentence-transformers")
except Exception as e:
    print(f"    ❌ Embedding error: {e}")

# ── 8. Test FAISS ──────────────────────────────────────────
print("\n[8] Testing FAISS")
try:
    import faiss
    import numpy as np
    index = faiss.IndexFlatL2(4)
    index.add(np.random.rand(5, 4).astype("float32"))
    print(f"    ✅ FAISS working! Version: {faiss.__version__}")
except ImportError:
    print("    ❌ faiss-cpu not installed")
    print("       Run: pip install faiss-cpu")
except Exception as e:
    print(f"    ❌ FAISS error: {e}")

# ── SUMMARY ────────────────────────────────────────────────
print("\n" + "=" * 55)
print("  Done! Fix any ❌ items above, then run: python app.py")
print("=" * 55 + "\n")