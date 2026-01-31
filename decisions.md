Weight Levels Decision

Policy rules are assigned relative weights to calculate a normalized fit score (0–100) and ensure no rule dominates:

Low = 1, Medium = 2, High = 3

Fit Score: (sum of passed rule weights / sum of all rule weights) \* 100

Rationale: Simple, explainable, and extensible; adding new rules won’t bias the score.

---

Hard vs Soft Rules

Purpose: Separate rules that block eligibility from rules that influence fit score.

Hard Rules (is_hard=True) → fail = ineligible immediately

Examples: state restrictions, industry exclusions, minimum time in business

Still counted in fit score for future flexibility

Soft Rules (is_hard=False) → affect fit score but don’t block eligibility

Examples: FICO/PayNet ranges, loan amount, equipment age

---

“SQLite used for rapid prototyping; schema designed for PostgreSQL.”

---

## Rule Type Design Decision

**Decision:**  
Use an **enum for `rule_type`** inside `PolicyRule`. Do **not** create a separate `rule_types` table for now.

**Rationale:**

- Rule types are **developer-defined** and limited.
- Faster iteration and simpler schema.
- Validation, operators, and value shape handled in code.

**Implications:**

- Supported rule types are fixed at deploy time.
- Policies reference rule types via enum values.

**Future Migration Path:**
Introduce a `rule_types` table only if:

- Rule types must be added without code changes
- Admins configure rules dynamically
- Rule metadata (labels, schemas, scoring behavior) is required

**Status:** Accepted

---

# Business CRUD Design Decisions

1. Nested creation of Business, PersonalGuarantor, and BusinessCredit in a single API endpoint.
2. API handles DB operations directly for simplicity (no service layer) due to 48‑hour demo constraint.
3. Pydantic schemas validate all input fields, including nested structures.
4. from_attributes=True allows SQLAlchemy models to be serialized directly to JSON.
5. Only minimal endpoints created: POST /businesses and GET /businesses/{id}.
6. Design is extensible: update/delete endpoints or a service layer can be added later.

# Business Identity (Demo Assumption)

- All businesses assumed to be domestic (single country).
- PAN used as unique identifier.
- Unique constraint enforced in DB to prevent duplicates.

# One Loan per Business

- Each business can have only one active loan request at a time.
- Enforced in API or via unique constraint on `LoanRequest.business_id`.
- Ensures matching is always based on the latest business details.

Loan status transitions not guarded (no state machine / checks)
