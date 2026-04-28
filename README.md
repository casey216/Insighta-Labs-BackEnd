# Insighta Labs — Intelligence Query Engine

A FastAPI-powered demographic intelligence API with advanced filtering, sorting, pagination, and natural language query support.

---

## Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (production) / SQLite (dev)
- **ORM**: SQLAlchemy
- **IDs**: UUID v7 (time-ordered)
- **Deployment**: Railway / Render / Docker

---

## Local Setup

### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd insighta
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your DATABASE_URL and SEED_URL
```

### 3. Seed the database

```bash
python seed.py
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

API available at `http://localhost:8000`  
Docs at `http://localhost:8000/docs`

---

## API Endpoints

### `GET /api/profiles`

Advanced filtering with sorting and pagination.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `gender` | string | `male` or `female` |
| `age_group` | string | `child`, `teenager`, `adult`, `senior` |
| `country_id` | string | ISO 2-letter code (e.g. `NG`, `KE`) |
| `min_age` | int | Minimum age |
| `max_age` | int | Maximum age |
| `min_gender_probability` | float | Min gender confidence (0.0–1.0) |
| `min_country_probability` | float | Min country confidence (0.0–1.0) |
| `sort_by` | string | `age`, `created_at`, `gender_probability` |
| `order` | string | `asc` (default) or `desc` |
| `page` | int | Page number (default: 1) |
| `limit` | int | Results per page (default: 10, max: 50) |

**Example:**
```
GET /api/profiles?gender=male&country_id=NG&min_age=25&sort_by=age&order=desc&page=1&limit=20
```

**Response:**
```json
{
  "status": "success",
  "page": 1,
  "limit": 20,
  "total": 342,
  "data": [ ... ]
}
```

---

### `GET /api/profiles/search?q=<query>`

Natural language query interface. No AI — pure rule-based parsing.

**Example queries:**

| Query | Parsed As |
|-------|-----------|
| `young males from nigeria` | `gender=male, min_age=16, max_age=24, country_id=NG` |
| `females above 30` | `gender=female, min_age=30` |
| `people from angola` | `country_id=AO` |
| `adult males from kenya` | `gender=male, age_group=adult, country_id=KE` |
| `male and female teenagers above 17` | `age_group=teenager, min_age=17` |
| `senior women from ghana` | `gender=female, age_group=senior, country_id=GH` |

Supports `page` and `limit` parameters.

**Uninterpretable query response:**
```json
{ "status": "error", "message": "Unable to interpret query" }
```

---

### `GET /api/profiles/{id}`

Fetch a single profile by UUID.

---

## Natural Language Parsing — How It Works

The NLP parser (`app/nlp_parser.py`) is **entirely rule-based** — no AI, no LLMs.

### 1. Gender Detection
Scans for gender keywords:
- Male: `male`, `man`, `men`, `boy`, `boys`, `guys`
- Female: `female`, `woman`, `women`, `girl`, `girls`, `ladies`
- If **both** are detected, gender filter is omitted

### 2. Age Group Detection
Matches keywords to stored age groups:
- `child/children/kids` → `age_group=child`
- `teenager/teen/youth` → `age_group=teenager`
- `adult/adults` → `age_group=adult`
- `senior/elderly` → `age_group=senior`
- `young` → `min_age=16, max_age=24` *(special case — not a stored group)*

### 3. Explicit Age Ranges
Regex patterns for:
- `above/over X` → `min_age=X`
- `below/under X` → `max_age=X`
- `between X and Y` → `min_age=X, max_age=Y`
- `aged X` → `min_age=X, max_age=X`

### 4. Country Matching
Dictionary of 100+ country names and demonyms → ISO codes.  
Examples: `nigerian` → `NG`, `kenyan` → `KE`, `south african` → `ZA`

---

## Error Responses

All errors follow:
```json
{ "status": "error", "message": "<description>" }
```

| Code | Meaning |
|------|---------|
| 400 | Missing or empty parameter |
| 404 | Profile not found |
| 422 | Invalid parameter type or value |
| 500 | Server error |

---

## Database Schema

```sql
CREATE TABLE profiles (
  id                  VARCHAR(36) PRIMARY KEY,
  name                VARCHAR UNIQUE NOT NULL,
  gender              VARCHAR NOT NULL,
  gender_probability  FLOAT NOT NULL,
  age                 INT NOT NULL,
  age_group           VARCHAR NOT NULL,
  country_id          VARCHAR(2) NOT NULL,
  country_name        VARCHAR NOT NULL,
  country_probability FLOAT NOT NULL,
  created_at          TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

IDs are UUID v7 (time-ordered, 128-bit).

---

## Deployment

### Railway / Render

1. Push to GitHub
2. Connect repo to Railway or Render
3. Add environment variables:
   - `DATABASE_URL` — PostgreSQL connection string
   - `SEED_URL` — URL to your seed JSON file
4. Run seed: `python seed.py`
5. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Docker

```bash
docker build -t insighta .
docker run -p 8000:8000 -e DATABASE_URL=... insighta
```

---

## Performance Notes

- Indexed columns: `id`, `name`, `country_id`
- Pagination uses SQL `OFFSET`/`LIMIT` — avoids full-table scans for filtered queries
- Total count uses `COUNT(*)` on filtered query (not full table)
- Max page `limit` is 50 to prevent large payloads
