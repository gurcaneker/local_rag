# DESIGN.md

## Proje Adı
Local-to-Production RAG Platform

## Tasarım Hedefi
Önce öğrenme ve deneme amaçlı lokal çalışan, daha sonra çok kullanıcılı, modüler ve production seviyesinde büyüyebilen bir RAG sistemi tasarlamak.

---

## 1. Tasarım Prensipleri

### Basit başla, modüler büyüt
İlk sürüm öğrenme odaklı olmalı. Gereksiz karmaşıklık eklenmemeli. Ancak her bileşen ileride değiştirilebilir şekilde tasarlanmalı.

### Retrieval ve generation ayrımı
Retrieval katmanı ile LLM cevap üretim katmanı birbirinden ayrılmalı. Böylece retrieval kalitesi bağımsız geliştirilebilir.

### Storage soyutlaması
Bugün LanceDB kullanılırken yarın Qdrant'a geçişi kolaylaştırmak için vector store erişimi soyut bir arayüz üzerinden yapılmalı.

### Tenant-first düşünce
İlk sürüm tek kullanıcı olsa bile veri modelinde user_id / workspace_id / tenant_id alanları öngörülmeli.

### Kaynaklı cevap
Sistem sadece cevap üretmekle kalmamalı, hangi chunk veya belgeye dayanarak cevap verdiğini de gösterebilmeli.

### Observability unutulmamalı
İlk sürümde bile loglama, hata yönetimi ve basic metrik toplama düşünülmeli.

---

## 2. Kullanıcı Deneyimi Hedefi

Kullanıcı aşağıdaki akışı yaşayabilmeli:

1. Sisteme doküman yükler
2. Dokümanın işlendiğini görür
3. Soru sorar
4. Sistem en ilgili bilgileri bulur
5. Cevabı ve kaynakları gösterir
6. Gerekirse sohbet geçmişine geri döner

---

## 3. Temel Akış Tasarımı

### Ingestion Flow
- Kullanıcı dosya yükler
- Dosya parse edilir
- Metin temizlenir
- Chunking uygulanır
- Her chunk için metadata üretilir
- Embedding hesaplanır
- Vector store'a yazılır

### Query Flow
- Kullanıcı soru sorar
- Query normalize edilir
- Dense embedding üretilir
- Sparse representation üretilir
- Hybrid search yapılır
- Top candidate chunk'lar alınır
- Reranker ile yeniden sıralanır
- En iyi chunk'lar LLM'e verilir
- Cevap ve kaynaklar döner

---

## 4. Bileşen Tasarım Kararları

### LLM Katmanı
İlk aşamada Ollama kullanılmalı. Ama LLM çağrıları abstraction arkasında olmalı. Gelecekte vLLM veya başka bir inference engine eklenebilmeli.

### Embedding Katmanı
Embedding modeli değişebilir olduğu için ayrı servis veya ayrı sınıf mantığıyla tasarlanmalı. Query ve document embedding aynı yerden yönetilmeli.

### Vector Store Katmanı
Aşağıdaki operasyonlar ortak bir interface ile tanımlanmalı:
- upsert_documents
- search
- delete_by_document
- delete_by_tenant
- health_check

### Metadata Tasarımı
Her chunk için minimum metadata:
- chunk_id
- document_id
- source_file
- page_number
- tenant_id
- workspace_id
- created_at
- document_type

### Prompt Tasarımı
Prompt'lar kod içine gömülmemeli. Ayrı dosya veya şablon sistemi ile yönetilmeli.
Türleri:
- system prompt
- answer prompt
- source-aware answer prompt
- no-answer fallback prompt

---

## 5. Retrieval Tasarım Kararı

Production hedefi için retrieval zinciri şu şekilde tasarlanmalı:

1. Query normalization
2. Dense retrieval
3. Sparse retrieval
4. Hybrid search
5. Candidate selection
6. Reranking
7. Context assembly
8. LLM answer generation

Bu zincirin amacı:
- semantik benzerliği yakalamak
- kritik terimleri kaçırmamak
- LLM'e gereksiz bağlam göndermemek
- doğruluğu artırmak

---

## 6. Ölçeklenebilirlik Tasarımı

### Faz 1
Tek servis + local storage + local vector db

### Faz 2
Auth + tenant yapısı + ingestion ve chat ayrımı

### Faz 3
Ayrı retrieval service + separate vector db + queue worker

### Faz 4
Distributed inference + multi-tenant vector setup + cache + monitoring

---

## 7. Güvenlik Tasarımı

- kullanıcı bazlı veri erişimi
- workspace bazlı izolasyon
- API auth
- upload validation
- file type kontrolü
- prompt injection'a karşı context sınırlandırma
- sistem promptunu kullanıcıdan ayırma

---

## 8. Performans Tasarımı

- chunk boyutu kontrollü tutulmalı
- embedding batch'leri desteklenmeli
- query cache opsiyonel düşünülmeli
- sık kullanılan promptlar optimize edilmeli
- reranker sadece daraltılmış adaylar üzerinde çalışmalı

---

## 9. Başlangıç İçin UI Tasarımı

İlk sürümde minimum ekranlar:
- login (opsiyonel)
- file upload
- document list
- chat screen
- source panel
- ingestion status

---

## 10. Tasarım Özeti

Bu sistemin tasarım felsefesi:
- local-first
- modular
- observable
- upgradeable
- source-grounded
- tenant-aware

Bu yaklaşım sayesinde aynı proje hem eğitim amaçlı kullanılabilir hem de ileride gerçek ürün mimarisine dönüştürülebilir.
