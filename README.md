# Project README

## Local Setup

### 1. Clone Repository

```bash
git clone https://github.com/singh-gaurav32/Lender-Matching.git
cd Lender-Matching
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

- Default: SQLite (`./test.db`)
- Can be migrated to PostgreSQL by updating `SQLALCHEMY_DATABASE_URL` in `database/session.py`
- Run migrations if using Alembic:

```bash
alembic upgrade head
```

### 5. Run Application

```bash
uvicorn main:app --reload
```

### 6. Run Tests

```bash
pytest
```

### Notes

- `.env` file can be used to override DB URL or other secrets.
- Ensure Python 3.12+ is used.

---

## Architectural Overview

The system follows a **modular FastAPI backend architecture** with SQLAlchemy ORM and workflow orchestration.

### Components

1. **API Layer (FastAPI)**
   - Handles HTTP requests and responses.
   - Routes organized by resource: `lenders`, `programs`, `businesses`, `loans`.
   - Dependency injection provides database sessions.

2. **Database Layer (SQLAlchemy ORM)**
   - Models: `Business`, `PersonalGuarantor`, `BusinessCredit`, `LoanRequest`, `Lender`, `LenderProgram`, `PolicyRule`, `BusinessFeature`, `MatchResult`.
   - Uses SQLite for local development; can switch to PostgreSQL.
   - Relationships define foreign key associations.

3. **Services / Domain Logic**
   - `FeatureService`: derives features.
   - `MatchingService`: matches loans against programs and rules.
   - `LoanWorkflowService`: orchestrates feature derivation and matching.

4. **Workflow Orchestration (Hatchet)**
   - Matching process runs as a Hatchet workflow: `derive_features` → `match_loan` → `persist_results`.
   - Tasks are separate and testable.

5. **Testing**
   - Pytest fixtures for `db_session`, `business`, `loan_request`, `lender_program`.
   - Integration tests cover lender creation, rule addition, business creation, loan matching, result retrieval.

### Data Flow

```
Business + Guarantor + Credit
            │
            ▼
      LoanRequest Created
            │
            ▼
    LoanWorkflowService.run()
     ├─ derive_features
     ├─ match_loan
     └─ persist_results
            │
            ▼
      MatchResult stored
            │
            ▼
       Retrieved via API
```

---

## API Documentation

### Base URL

```
http://localhost:8000
```

### 1. Lenders

#### Create Lender

```
POST /lenders
```

**Body:**

```json
{
  "name": "ABC Bank"
}
```

**Response:**

```json
{
  "id": 1,
  "name": "ABC Bank"
}
```

#### Add Program to Lender

```
POST /lenders/{lender_id}/programs
```

**Body:**

```json
{
  "name": "SME Loan Program"
}
```

**Response:**

```json
{
  "id": 1,
  "lender_id": 1,
  "name": "SME Loan Program",
  "rules": []
}
```

#### Add Rule to Program

```
POST /lenders/programs/{program_id}/rules
```

**Body:**

```json
[
  {
    "rule_type": "fico",
    "operator": ">=",
    "value": "700",
    "weight": 3
  }
]
```

**Response:**

```json
{
  "id": 1,
  "lender_id": 1,
  "name": "SME Loan Program",
  "rules": [
    {
      "id": 1,
      "rule_type": "fico",
      "operator": ">=",
      "value": "700",
      "weight": 3,
      "is_hard": false
    }
  ]
}
```

### 2. Business

#### Create Business

```
POST /businesses
```

**Body:**

```json
{
  "legal_name": "Test Pvt Ltd",
  "industry": "Manufacturing",
  "state": "KA",
  "years_in_business": 5,
  "annual_revenue": 1000000,
  "guarantor": {
    "fico_score": 720,
    "has_bankruptcy": false,
    "has_tax_liens": false
  },
  "credit": {
    "paynet_score": 80.5,
    "trade_line_count": 10
  }
}
```

**Response:**

```json
{
  "id": 1,
  "legal_name": "Test Pvt Ltd",
  "industry": "Manufacturing",
  "state": "KA",
  "years_in_business": 5,
  "annual_revenue": 1000000,
  "guarantor": { ... },
  "credit": { ... }
}
```

### 3. Loans

#### Create Loan

```
POST /loans
```

**Body:**

```json
{
  "business": { ... },
  "amount": 500000,
  "term_months": 36,
  "equipment_type": "excavator",
  "equipment_year": 2022
}
```

**Response:**

```json
{
  "id": 1,
  "business": { ... },
  "amount": 500000,
  "term_months": 36,
  "equipment_type": "excavator",
  "equipment_year": 2022
}
```

#### Initiate Loan Matching

```
POST /loans/initiate_match?loan_request_id=1
```

**Response:**

```
"Loan Matching Initiated"
```

#### Get Loan Matches

```
GET /loans/{loan_id}/matches
```

**Response:**

```json
[
  {
    "id": 1,
    "loan_request_id": 1,
    "program_id": 1,
    "score": 85.0,
    "matched_rules": [...]
  }
]
```
