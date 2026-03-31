# LOCAL RAG PLATFORM

## 🚀 Proje Özeti
Bu proje, lokal çalışan bir RAG (Retrieval-Augmented Generation) sistemini zamanla çok kullanıcılı, production seviyesinde bir platforma dönüştürmeyi amaçlar.

---

## 🎯 Özellikler
- Lokal LLM (Ollama)
- Doküman yükleme ve indeksleme
- Semantic search (embedding)
- Hybrid search (dense + sparse)
- Reranking
- Kaynaklı cevap üretimi
- Modüler mimari
- Çok kullanıcılı sisteme uygun yapı

---

## 🧱 Teknoloji Stack

- Python
- FastAPI
- Ollama
- LanceDB (başlangıç)
- Qdrant (ileride)
- Sentence Transformers
- PyPDF

---

## 📂 Proje Yapısı

app/
services/
db/
parsers/
api/
workers/
data/

---

## ⚡ Kurulum

```bash
python3 -m venv rag_env
source rag_env/bin/activate
pip install -r requirements.txt
```

---

## ▶️ Çalıştırma

```bash
uvicorn app.main:app --reload
```

---

## 🔄 Temel Akış

1. Doküman yüklenir
2. Chunk + embedding yapılır
3. Vector DB’ye yazılır
4. Kullanıcı soru sorar
5. Retrieval yapılır
6. LLM cevap üretir

---

## 🧠 Pipeline

- Query normalize
- Dense embedding
- Sparse representation
- Hybrid search
- Top-K selection
- Reranking
- LLM answer

---

## 📈 Roadmap

### Phase 1
- Local RAG
- Basic retrieval

### Phase 2
- Hybrid search
- Reranker

### Phase 3
- Multi-user
- Auth

### Phase 4
- Qdrant
- Scaling
- Production

---

## 🔐 Güvenlik

- Tenant izolasyonu
- Auth
- Prompt injection önlemleri

---

## 📌 Not
Bu proje öğrenme + gerçek ürün geliştirme amacıyla tasarlanmıştır.
