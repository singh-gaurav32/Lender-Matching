# Design Decisions

### 1. Database

- **SQLite** for rapid prototyping; schema designed for PostgreSQL.
- SQLAlchemy ORM used for models and relationships.
- Business uniqueness not enforced by default, but can be ensured via PAN or other identifiers.
- One active `LoanRequest` per business enforced via unique constraint on `LoanRequest.business_id`.

### 2. API Design

- FastAPI routes organized by resource (`lenders`, `programs`, `businesses`, `loans`).
- Nested creation of `Business`, `PersonalGuarantor`, and `BusinessCredit` in a single endpoint for simplicity.
- Pydantic schemas validate all input fields, including nested structures.
- `from_attributes=True` allows direct serialization of SQLAlchemy models to JSON.
- Minimal endpoints for demo: POST/GET for businesses, lenders, and loans.
- Extensible: update/delete endpoints or service layer can be added later.

### 3. Workflow / Task Orchestration

- Matching workflow separated into `LoanWorkflowService` → `FeatureService` → `MatchingService`.
- Workflow designed to be moved into Hatchet for orchestration.
- Workflow steps are testable and reusable.

### 4. Policy Rule Decisions

#### Weight Levels

- Low = 1, Medium = 2, High = 3.
- Fit Score = `(sum of passed rule weights / sum of all rule weights) * 100`.
- Rationale: simple, explainable, and extensible; adding rules won’t bias score.

#### Hard vs Soft Rules

- **Hard rules (`is_hard=True`)** → fail immediately if not satisfied (eligibility block), still counted in fit score.
  - Examples: state restrictions, industry exclusions, minimum time in business.
- **Soft rules (`is_hard=False`)** → affect fit score but don’t block eligibility.
  - Examples: FICO/PayNet ranges, loan amount, equipment age.

#### Rule Type

- `rule_type` is an enum in `PolicyRule`, no separate `rule_types` table.
- Supported types are fixed at deploy time; validation handled in code.
- Future migration to table only if dynamic rule configuration is required.

### 5. Validation & Error Handling

- Loan status prevents duplicate initiation.
- Input validation at Pydantic level (FICO, PayNet, years, revenue).
- API returns clear HTTP status codes and error messages.

### 6. Extensibility

- New rules, lenders, programs can be added without breaking API.
- Modular services allow adding workflow steps or scoring metrics.
- Business and loan models can later support updates and deletions.

### 7. Testing

- Pytest fixtures for `db_session`, `business`, `loan_request`, `lender_program`.
- Integration tests cover end-to-end flows: lender → program → rule → business → loan → result retrieval.
- Matching logic is tested separately via unit tests.

### 8. Configuration

- `.env` file for DB URLs and secrets.
- Dependency injection of DB session for testability.

### 9. Business & Loan Assumptions (Demo)

- One active loan per business.
- Loan status transitions are not strictly enforced (no state machine) as of now.

### 10. Tech Stack

- Python 3.12+, FastAPI, SQLAlchemy, Pydantic v2.
- SQLite (dev) / PostgreSQL (prod), Hatchet for orchestration.
- Pytest for testing.

### 11. Rule Management

- Policy rules are added manually via API or database; no dynamic admin UI exists for creating rules.
- Rules must be defined and deployed by developers.
- Future enhancements may include a UI or service for dynamic rule creation.
