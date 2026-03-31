# ARCHITECTURE.md

## Proje Adı
Local RAG to Multi-User Production RAG Architecture

## Mimari Vizyon
Tek kullanıcı için lokal çalışan bir RAG prototipini, zamanla çok kullanıcılı, tenant-aware, modüler ve production-ready bir platforma dönüştürmek.

---

## 1. Yüksek Seviye Mimari

### Faz 1 — Local PoC
- FastAPI
- Ollama
- Embedding service
- LanceDB
- Local file ingestion
- Basic prompt orchestration

### Faz 2 — Structured App
- API katmanı
- Retrieval service
- Ingestion service
- Metadata store
- User/workspace yapısı

### Faz 3 — Multi-User
- Auth
- Queue tabanlı ingestion
- Tenant-aware retrieval
- Chat history
- Workspace isolation

### Faz 4 — Production Scale
- Qdrant
- Postgres
- Redis
- Worker pool
- Monitoring
- Separate LLM serving
- Horizontal scaling

---

## 2. Mantıksal Bileşenler

### A. API Layer
Sistemin dış dünyaya açılan katmanıdır.

Sorumluluklar:
- request kabul etme
- auth kontrolü
- tenant çözümleme
- rate limiting
- response döndürme

Örnek endpointler:
- POST /documents/upload
- POST /documents/reindex
- GET /documents
- POST /chat/ask
- GET /health

---

### B. Ingestion Service
Dokümanların işlenmesinden sorumludur.

Adımlar:
1. dosya al
2. parse et
3. normalize et
4. chunk oluştur
5. metadata ekle
6. embedding üret
7. vector store'a yaz
8. metadata store'a kaydet

Bu servis ileride queue üzerinden worker mantığı ile çalışmalıdır.

---

### C. Retrieval Service
Sorgu bazlı aramayı yönetir.

Adımlar:
1. query normalize et
2. dense embedding üret
3. sparse representation üret
4. hybrid search yap
5. top-k aday getir
6. reranker ile sıralamayı düzelt
7. en iyi chunk'ları döndür

Bu servis LLM'den bağımsız olmalıdır.

---

### D. LLM Service
Cevap üretim katmanıdır.

Sorumluluklar:
- prompt assembly
- model seçimi
- cevap üretimi
- streaming support
- token kullanım kaydı

İlk aşamada Ollama ile çalışır.
İleride vLLM veya başka inference engine ile genişleyebilir.

---

### E. Vector Store Layer
Chunk embedding'lerini ve metadata referanslarını tutar.

Başlangıç:
- LanceDB

Gelişmiş:
- Qdrant

Gereken operasyonlar:
- create_collection
- upsert
- search
- delete
- filter_by_tenant
- health_check

---

### F. Metadata Store
Yapısal verilerin tutulduğu katmandır.

Önerilen varlıklar:
- users
- workspaces
- documents
- chunks
- chat_sessions
- chat_messages
- ingestion_jobs

İlk sürümde hafif tutulabilir.
Production'da Postgres tercih edilmelidir.

---

## 3. Veri Modeli

### users
- id
- name
- email
- created_at

### workspaces
- id
- name
- owner_user_id
- created_at

### documents
- id
- workspace_id
- tenant_id
- file_name
- file_type
- upload_status
- created_at

### chunks
- id
- document_id
- tenant_id
- workspace_id
- chunk_index
- page_number
- text
- embedding_ref
- created_at

### chat_sessions
- id
- user_id
- workspace_id
- title
- created_at

### chat_messages
- id
- session_id
- role
- content
- created_at

### ingestion_jobs
- id
- document_id
- status
- error_message
- started_at
- finished_at

---

## 4. Retrieval Pipeline Architecture

1. Query normalization
2. Dense embedding generation
3. Sparse representation generation
4. Hybrid search
5. Top 20 candidate selection
6. Reranking
7. Top 5 context assembly
8. Prompt generation
9. LLM response
10. Citation generation

Bu zincir sistemin doğruluk katmanıdır.

---

## 5. Tenant / Multi-User Mimarisi

### Temel ilke
Her veri tenant-aware olmalıdır.

Her kayıt mümkünse şu alanlardan en az birini taşımalıdır:
- user_id
- workspace_id
- tenant_id

### İzolasyon seçenekleri
1. shared collection + tenant filter
2. dedicated collection / shard per tenant

Başlangıç için:
- shared index + metadata filter

Kurumsal büyüme için:
- dedicated collection / shard

---

## 6. Dağıtım Stratejisi

### Local Geliştirme
- tek makine
- tek API
- local Ollama
- local LanceDB

### Staging
- ayrı config
- test verisi
- auth açık
- Qdrant opsiyonel

### Production
- reverse proxy
- separate app service
- vector db service
- worker service
- llm service
- metadata db
- monitoring

---

## 7. Klasör Yapısı Önerisi

```text
project-root/
├── app/
│   ├── api/
│   │   ├── routes_chat.py
│   │   ├── routes_documents.py
│   │   └── routes_health.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── prompts.py
│   ├── services/
│   │   ├── ingestion_service.py
│   │   ├── retrieval_service.py
│   │   ├── llm_service.py
│   │   ├── rerank_service.py
│   │   └── embedding_service.py
│   ├── db/
│   │   ├── metadata_db.py
│   │   ├── vector_store_base.py
│   │   ├── vector_store_lancedb.py
│   │   └── vector_store_qdrant.py
│   ├── parsers/
│   │   ├── pdf_parser.py
│   │   ├── txt_parser.py
│   │   └── markdown_parser.py
│   ├── models/
│   │   ├── document.py
│   │   ├── chunk.py
│   │   └── chat.py
│   └── main.py
├── workers/
│   └── ingestion_worker.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── lancedb/
├── tests/
├── scripts/
├── requirements.txt
└── README.md
```

---

## 8. Kritik Mimari Kurallar

- Retrieval ve LLM ayrı olmalı
- Vector store implementasyonu soyutlanmalı
- Prompt yönetimi merkezi olmalı
- Tenant bilgisi tüm akışta korunmalı
- Chunk metadata zorunlu olmalı
- Ingestion işlemi uzun vadede async yapılmalı
- Chat geçmişi uygulama katmanında tutulmalı
- LLM'e sadece seçilmiş context gönderilmeli

---

## 9. Gelecek Evrim Planı

### Bugün
- local tek kullanıcı
- basit retrieval
- local model

### Yarın
- auth
- workspace
- hybrid search
- reranker

### Sonra
- Qdrant
- workers
- cache
- analytics
- usage metering
- admin panel

---

## 10. Mimari Özeti

Bu mimari şu prensiple kurulmuştur:

Önce öğren, sonra doğrula, sonra modülerleştir, sonra ölçekle.

Yani sistemin ilk sürümü küçük olabilir; fakat tasarım kararları gelecekte:
- çok kullanıcı
- tenant izolasyonu
- production retrieval
- ayrı LLM serving
- kurumsal kullanım

için hazır olmalıdır.
