# TASKS.md

## 🎯 Genel Hedef
Local çalışan RAG sistemini adım adım production seviyesine çıkarmak.

---

# 🧱 PHASE 1 — LOCAL RAG

## Setup
- [ ] Python env kur
- [ ] Ollama kur
- [ ] Model indir (mistral / qwen)
- [ ] Proje klasör yapısı oluştur

## Core
- [ ] PDF parser yaz
- [ ] Chunking fonksiyonu yaz
- [ ] Embedding servisi yaz
- [ ] LanceDB bağlantısı kur

## Retrieval
- [ ] Basic vector search
- [ ] Top-K retrieval

## LLM
- [ ] Ollama entegrasyonu
- [ ] Basit prompt

## API
- [ ] FastAPI kur
- [ ] /ask endpoint
- [ ] /ingest endpoint

---

# 🚀 PHASE 2 — ADVANCED RETRIEVAL

- [ ] Query normalization
- [ ] Sparse search ekle
- [ ] Hybrid search implement et
- [ ] Reranker ekle
- [ ] Source citation ekle

---

# 👥 PHASE 3 — MULTI USER

- [ ] User modeli
- [ ] Workspace sistemi
- [ ] Auth sistemi (JWT)
- [ ] Tenant isolation
- [ ] Chat history

---

# ⚙️ PHASE 4 — SCALING

- [ ] LanceDB → Qdrant geçiş
- [ ] Queue sistemi (ingestion)
- [ ] Worker service
- [ ] Redis cache
- [ ] Logging

---

# 🧠 PHASE 5 — PRODUCTION

- [ ] Rate limiting
- [ ] Monitoring
- [ ] Error tracking
- [ ] Admin panel
- [ ] Usage tracking

---

# 🔥 BONUS

- [ ] UI (React / Next.js)
- [ ] Streaming response
- [ ] File status tracking
- [ ] Model switching
