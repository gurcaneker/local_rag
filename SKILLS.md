# SKILLS.md

## Proje Adı
Local / Multi-User RAG Platform

## Amaç
Bu proje, önce tek kullanıcı için lokal çalışan, daha sonra çok kullanıcılı ve production seviyesine büyüyebilen bir RAG platformu geliştirmek için tasarlanır. Hedef; doküman yükleme, indeksleme, retrieval, reranking ve LLM tabanlı cevap üretimini modüler şekilde kurmaktır.

---

## 1. Teknik Yetkinlikler

### Python
- Python 3.11+
- virtualenv / venv kullanımı
- paket yönetimi
- type hint kullanımı
- modüler proje yapısı
- logging
- exception handling

### FastAPI
- REST API geliştirme
- router yapısı
- request / response modelleme
- dependency injection
- health check endpointleri
- auth middleware temelleri
- streaming response mantığı

### Retrieval / RAG
- chunking stratejileri
- metadata tasarımı
- dense retrieval
- sparse retrieval
- hybrid search
- reranking
- context assembly
- citation / source grounding
- hallucination azaltma prensipleri

### LLM Entegrasyonu
- Ollama ile lokal model çağırma
- prompt template tasarımı
- sistem promptu / kullanıcı promptu ayrımı
- context window yönetimi
- model seçimi
- inference maliyeti ve gecikme farkları

### Embedding
- embedding mantığı
- query embedding
- document embedding
- embedding dimension uyumu
- model değiştirme etkileri
- semantic similarity prensipleri

### Vector Database
- LanceDB ile local PoC geliştirme
- Qdrant ile server tabanlı büyüme
- collection tasarımı
- tenant bazlı filtreleme
- metadata filtresi
- upsert / search / delete operasyonları

### Doküman İşleme
- PDF parse
- TXT / Markdown parse
- metin temizleme
- chunk metadata üretme
- dosya tipine göre ingestion akışı

### Production Mimarisi
- çok kullanıcılı sistem tasarımı
- tenant izolasyonu
- auth / authorization
- worker mantığı
- queue tabanlı ingestion
- logging / monitoring / observability
- rate limiting
- yatay ölçekleme temelleri

### Frontend / UX (opsiyonel)
- chat arayüzü mantığı
- dosya yükleme ekranı
- kaynak gösterimi
- ingestion durum takibi

---

## 2. Öğrenme Hedefleri

Bu projede aşağıdaki kavramların öğrenilmesi hedeflenir:

- RAG sisteminin uçtan uca nasıl çalıştığı
- Bir query'nin retrieval pipeline içinde nasıl işlendiği
- Dense ve sparse aramanın farkı
- Hybrid search neden gereklidir
- Reranker neden son kalite katmanıdır
- LLM neden retrieval'dan ayrı düşünülmelidir
- Local mimari production'a nasıl evrilir
- Tek kullanıcıdan SaaS mimariye geçiş nasıl yapılır

---

## 3. Başarı Ölçütleri

Aşağıdaki çıktılar elde edildiğinde proje başarılı kabul edilir:

- Kullanıcı doküman yükleyebiliyor
- Dokümanlar chunk'lanıp indeksleniyor
- Kullanıcı soru sorabiliyor
- Sistem alakalı chunk'ları bulabiliyor
- LLM kaynaklı cevap üretiyor
- Kaynak parçaları gösterilebiliyor
- Mimari modüler biçimde büyütülebiliyor
- Tenant / workspace yapısına uygun genişleyebiliyor

---

## 4. Faz Bazlı Yetkinlik Gelişimi

### Faz 1 — Local PoC
- Ollama
- embedding
- LanceDB
- FastAPI
- basit chunking
- top-k retrieval

### Faz 2 — Gelişmiş Retrieval
- metadata filtering
- sparse retrieval
- hybrid search
- reranker
- source citation

### Faz 3 — Multi-User
- user / workspace yapısı
- auth
- ingestion worker
- queue
- chat history
- tenant izolasyonu

### Faz 4 — Production
- Qdrant
- cache
- observability
- rate limiting
- deployment
- yüksek eşzamanlılık

---

## 5. Minimum Stack

- Python
- FastAPI
- Ollama
- Embedding model
- LanceDB
- pypdf / parser
- basic logging

## 6. Hedef Stack

- Python
- FastAPI
- Qdrant
- Ollama ve/veya vLLM
- reranker
- async ingestion workers
- Postgres metadata store
- Redis / cache
- frontend chat UI

---

## 7. Not
Bu dosya, Antigravity veya benzeri bir code agent'a projenin hangi beceri alanlarını kapsadığını ve geliştirici tarafında hangi odaklarla ilerlenmesi gerektiğini anlatmak için hazırlanmıştır.
