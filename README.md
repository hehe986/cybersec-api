# 🔐 Cybersecurity Incident Management API

**UTS Pemrograman Web Lanjut — TK070**
**Muhammad Ardita Hilmi | 23.83.0981 | 23TK01**
**Universitas Amikom Yogyakarta | Tahun Akademik 2026/2027**

---

## 📌 Deskripsi Proyek

REST API untuk mengelola insiden keamanan siber dalam sebuah organisasi secara terpusat. Sistem ini memungkinkan tim SOC untuk melacak **insiden**, **aset IT**, **kerentanan (vulnerability)**, serta **audit log** aktivitas sistem.

| Info | Detail |
|------|--------|
| **Domain** | Cybersecurity |
| **Stack** | Python Flask, SQLAlchemy ORM, SQLite |
| **Arsitektur** | MVC (Model-View-Controller) |
| **Versi** | v1.0 |

**Masalah yang Diselesaikan:**
Organisasi tidak memiliki sistem terpusat untuk mencatat insiden keamanan, aset IT, dan kerentanan yang ditemukan. Tim SOC harus tracking secara manual via spreadsheet, tidak ada trail aktivitas (siapa melakukan apa kapan).

**Target Pengguna:**
- SOC Analyst — melaporkan insiden, tracking vulnerability
- IT Admin — mendaftarkan dan mengelola aset
- Security Manager — memantau status insiden & kerentanan

---

## 🏗️ Struktur Folder

```
uts_pwl_0981/
├── app.py                      # Entry point, blueprint registration, error handlers
├── config.py                   # Flask app, DB config, password hashing
├── seed.py                     # Inisialisasi DB + seed data realistis
├── test_api.py                 # Automated test (pytest) — 15 test cases
├── openapi.yaml                # OpenAPI 3.0 specification lengkap
├── requirements.txt
├── README.md
├── .gitignore
├── controllers/
│   ├── UserController.py
│   ├── AssetController.py
│   ├── IncidentController.py
│   ├── VulnerabilityController.py
│   └── AuditLogController.py
├── models/
│   ├── UserModel.py
│   ├── AssetModel.py
│   ├── IncidentModel.py
│   ├── VulnerabilityModel.py
│   └── AuditLogModel.py
└── routes/
    ├── user_bp.py
    ├── asset_bp.py
    ├── incident_bp.py
    ├── vulnerability_bp.py
    └── auditlog_bp.py
```

---

## ⚙️ Instalasi & Menjalankan

### Prasyarat
- Python 3.10+
- pip

### Langkah-langkah

```bash
# 1. Clone repo
git clone https://github.com/hehe986/cybersec-api
cd cybersec-api

# 2. Buat virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

# 3. Install dependency
pip install -r requirements.txt

# 4. Inisialisasi database + seed data
python seed.py

# 5. Jalankan server
python app.py
# → Server berjalan di http://127.0.0.1:5000
```

---

## 🧪 Menjalankan Test

```bash
pytest test_api.py -v
```

**Coverage test (15 test cases):**

| Test | Endpoint | Skenario |
|------|----------|----------|
| test_get_users_success | GET /api/users | ✅ Berhasil |
| test_create_user_success | POST /api/users | ✅ Berhasil |
| test_create_user_missing_field | POST /api/users | ❌ Validasi gagal |
| test_create_user_duplicate_username | POST /api/users | ❌ 409 Conflict |
| test_get_user_not_found | GET /api/users/9999 | ❌ 404 Not Found |
| test_create_incident_success | POST /api/incidents | ✅ Berhasil |
| test_create_incident_invalid_severity | POST /api/incidents | ❌ Enum tidak valid |
| test_get_incidents_filter_severity | GET /api/incidents?severity=critical | ✅ Filter benar |
| test_delete_incident_not_found | DELETE /api/incidents/9999 | ❌ 404 Not Found |
| test_create_vulnerability_success | POST /api/vulnerabilities | ✅ Berhasil |
| test_create_vulnerability_missing_field | POST /api/vulnerabilities | ❌ Validasi gagal |
| test_get_vulnerability_not_found | GET /api/vulnerabilities/9999 | ❌ 404 Not Found |
| test_create_asset_success | POST /api/assets | ✅ Berhasil |
| test_get_assets_success | GET /api/assets | ✅ Berhasil |
| test_create_asset_missing_owner | POST /api/assets | ❌ Validasi gagal |
| test_get_audit_logs_success | GET /api/audit-logs | ✅ Berhasil |

---

## 🗃️ ERD (Entity Relationship Diagram)

```
┌─────────────┐       ┌─────────────────┐       ┌────────────────────┐
│    users    │       │     assets      │       │     incidents      │
│─────────────│       │─────────────────│       │────────────────────│
│ id (PK)     │──┐    │ id (PK)         │──┐    │ id (PK)            │
│ username    │  │    │ name            │  │    │ title              │
│ password    │  │    │ ip_address      │  │    │ description        │
│ email       │  │    │ asset_type      │  │    │ severity           │
│ role        │  │    │ status          │  │    │ status             │
│ is_active   │  │    │ description     │  └───►│ asset_id (FK)      │
│ created_at  │  └───►│ owner_id (FK)   │       │ reported_by (FK)◄──┤
└─────────────┘       └─────────────────┘       │ created_at         │
       │                      │                 │ updated_at         │
       │                      │                 └────────────────────┘
       │                      │
       │               ┌──────────────────────┐
       │               │   vulnerabilities    │
       │               │──────────────────────│
       │               │ id (PK)              │
       │               │ title                │
       │               │ cve_id               │
       │               │ severity             │
       │               │ status               │
       │               │ description          │
       │               │ asset_id (FK)◄───────┤
       └──────────────►│ discovered_by (FK)   │
       │               │ created_at           │
       │               └──────────────────────┘
       │
       │               ┌──────────────────────┐
       │               │     audit_logs       │
       │               │──────────────────────│
       │               │ id (PK)              │
       │               │ action               │
       │               │ entity_type          │
       │               │ entity_id            │
       │               │ description          │
       └──────────────►│ performed_by (FK)    │
                       │ timestamp            │
                       └──────────────────────┘
```

**Relasi:**
- `users` → `assets` (1:N, owner aset)
- `users` → `incidents` (1:N, pelapor)
- `users` → `vulnerabilities` (1:N, penemu)
- `users` → `audit_logs` (1:N, aktor)
- `assets` → `incidents` (1:N)
- `assets` → `vulnerabilities` (1:N)

---

## 📡 Daftar Endpoint API

### Users `(/api/users)`
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | /api/users | List user (filter role, pagination) |
| GET | /api/users/:id | Detail user |
| POST | /api/users | Buat user baru |
| PUT | /api/users/:id | Update user |
| DELETE | /api/users/:id | Hapus user |

### Assets `(/api/assets)`
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | /api/assets | List aset (filter status/type, search, sort) |
| GET | /api/assets/:id | Detail aset |
| POST | /api/assets | Daftarkan aset |
| PUT | /api/assets/:id | Update aset |
| DELETE | /api/assets/:id | Hapus aset |

### Incidents `(/api/incidents)`
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | /api/incidents | List insiden (filter, search, sort, pagination) |
| GET | /api/incidents/:id | Detail insiden |
| POST | /api/incidents | Laporkan insiden |
| PUT | /api/incidents/:id | Update insiden |
| DELETE | /api/incidents/:id | Hapus insiden |

### Vulnerabilities `(/api/vulnerabilities)`
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | /api/vulnerabilities | List vuln (filter severity/status, search CVE, sort) |
| GET | /api/vulnerabilities/:id | Detail vuln |
| POST | /api/vulnerabilities | Catat vulnerability |
| PUT | /api/vulnerabilities/:id | Update vulnerability |
| DELETE | /api/vulnerabilities/:id | Hapus vulnerability |

### Audit Logs `(/api/audit-logs)` — Read Only
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | /api/audit-logs | List log (filter entity_type, action, performed_by) |
| GET | /api/audit-logs/:id | Detail log |

---

## 📬 Contoh Request & Response

### POST /api/incidents — Laporkan Insiden
```bash
curl -X POST http://127.0.0.1:5000/api/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Unauthorized SSH Access",
    "description": "Brute force attack detected on web server",
    "severity": "critical",
    "reported_by": 1,
    "asset_id": 1
  }'
```
**Response 201:**
```json
{
  "status": "success",
  "message": "Incident created",
  "data": {
    "id": 5,
    "title": "Unauthorized SSH Access",
    "severity": "critical",
    "status": "open",
    "reported_by": 1,
    "asset_id": 1,
    "created_at": "2026-11-05T14:25:52"
  }
}
```

### GET /api/incidents — Filter + Search + Pagination
```bash
curl "http://127.0.0.1:5000/api/incidents?severity=critical&status=open&search=SSH&page=1&per_page=5"
```
**Response 200:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 2,
      "title": "Unauthorized SSH Access",
      "severity": "critical",
      "status": "open"
    }
  ],
  "total": 1,
  "page": 1
}
```

### POST /api/users — Buat User
```bash
curl -X POST http://127.0.0.1:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "analyst_baru",
    "password": "pass123",
    "email": "analyst@cybersec.id",
    "role": "analyst"
  }'
```
**Response 201:**
```json
{
  "status": "success",
  "message": "User created",
  "data": {
    "id": 4,
    "username": "analyst_baru",
    "email": "analyst@cybersec.id",
    "role": "analyst",
    "is_active": true
  }
}
```

### Error Response (400)
```json
{
  "status": "error",
  "message": "severity is required"
}
```

### GET /api/audit-logs — Lihat Semua Activity Log
```bash
curl "http://127.0.0.1:5000/api/audit-logs?entity_type=incident&action=CREATE"
```
**Response 200:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "action": "CREATE",
      "entity_type": "incident",
      "entity_id": 2,
      "description": "Incident 'Unauthorized SSH Access' reported",
      "performed_by": 1,
      "timestamp": "2026-11-05T14:25:52"
    }
  ],
  "total": 1,
  "page": 1
}
```

---

## 🔐 Praktik Keamanan

| Aspek | Implementasi |
|-------|-------------|
| Password Hashing | SHA-256 via `hashlib` sebelum simpan ke DB |
| Input Validation | Wajib untuk semua required fields |
| Enum Validation | Whitelist check untuk severity, status, role |
| Duplicate Check | 409 Conflict untuk username & email |
| Error Response | Format konsisten `{status, message}` |
| Global Error Handler | 404 & 405 ditangani di `app.py` |
| Audit Trail | Setiap CREATE/UPDATE/DELETE tercatat otomatis |

---

## 🚀 Rencana Pengembangan (UAS)

1. **JWT Authentication & Authorization**
   - `POST /api/auth/login` → return access token
   - Middleware `@jwt_required` di semua endpoint
   - Role-based access control (admin/analyst/viewer)

2. **Deployment ke Railway/Render**
   - Switch ke PostgreSQL untuk production
   - Environment variable untuk config sensitif
   - Domain publik dengan HTTPS

3. **Frontend Dashboard**
   - HTML/JS dashboard visualisasi insiden
   - Pie chart severity distribution, timeline insiden

4. **Penguatan Keamanan**
   - Flask-Limiter untuk rate limiting
   - Input sanitization lebih ketat (regex validation)
   - CORS configuration proper

5. **Swagger UI Interaktif**
   - Flasgger atau Flask-RESTX
   - Endpoint `/docs` untuk interactive testing

6. **Query Optimization**
   - Index pada kolom `severity`, `status`, `created_at`
   - Eager loading untuk foreign key joins

---

## 📚 Referensi & Tools

- Flask: https://flask.palletsprojects.com
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com
- Python pytest: https://docs.pytest.org
- OpenAPI Spec: https://swagger.io/specification
- Bantuan AI: Claude (Anthropic) — digunakan untuk scaffolding struktur kode, review, dan dokumentasi

---

**Made with 🔥 by Muhammad Ardita Hilmi | 23.83.0981**
