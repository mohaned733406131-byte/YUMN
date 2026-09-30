# describ — Platform Transaction Rules (sponsor specification)

> **Provenance:** content authored by the project sponsor and provided on 2026-09-28 (session 007).
> It restores the 0-byte placeholder tracked as defect **`D-16`** (`memory.md` §4 → `RESOLVED 2026-09-28`).
> **Standing:** a sponsor input under evaluation — it does **not** override
> [`docs/00-project-overview/project-constraints.md`](docs/00-project-overview/project-constraints.md)
> (`C-01…C-26`) until the change-control process amends those constraints (root `docs/README.md` §9).
> **Reconciliation status:** each rule below was checked against the approved canon (session 007);
> agreements, contradictions, and gaps are registered in
> [`docs/20-validation/core/contradiction-audit.md`](docs/20-validation/core/contradiction-audit.md) (`CT-23`…`CT-30`),
> [`docs/20-validation/core/missing-information.md`](docs/20-validation/core/missing-information.md) (`GAP-13`, `GAP-14`),
> and the session work file [`docs/sessions/session-007-describ-reconciliation.md`](docs/sessions/session-007-describ-reconciliation.md).

---

## 1. Accounts on registration

Once a customer or merchant is registered **and verified**, a financial account is created for them
on the platform; this account includes **sub-accounts denominated in various currencies**.

## 2. What types of transactions can be performed on the account?

### Funding scenarios

The customer accesses their account to add funds, then selects a funding method from the available
options — for example:

1. **Via external wallets integrated with the system via API.** The user enters the payment ID and
   the PIN generated within their external wallet (such as **Al-Kuraimi** or **Jeeb**). The system
   verifies the transaction through the connected API and adds the amount to the balance.
2. **Via transfers or other methods.** The user submits proof of payment, which an administrator then
   verifies before adding the funds to the customer's account.
3. **Via account funding.** Another person transfers funds from their own account to this user's account.

## 3. Customer account operations

1. **Upon making a purchase, the amount is deducted from the account balance after verification.**
   - Example: if the user holds a balance in Yemeni currency but places an order in Saudi Riyals,
     the system displays the equivalent deduction based on the system's standard exchange rate, or
     deducts the amount from an account holding the same currency as the order.
2. Users can **deposit funds into another person's account** or **request a withdrawal to an external
   wallet**, subject to the options available in the system.
3. A **detailed account statement** is provided, covering transactions for both the main account and
   the sub-accounts.

## 4. For merchants

- The account serves as the **repository for all financial entitlements** due to the merchant.
- A merchant may hold a **primary account with multiple sub-accounts** that they personally manage.
- Each **store has an account** linked to both the merchant and the store itself, through which all
  store-related transactions are processed.
- The **management function** (administration) enables operations on and the viewing of accounts —
  either individually or collectively — as well as any actions deemed appropriate for account management.

## 5. Returns and escrow

**Returnable products are designated by the merchant**; the value of these items is held in an
**escrow account for the duration of the merchant-defined return period**. Funds for items that are
**not returned are released directly**.

## 6. Currency management

**Currency management is handled by the platform**, which controls the **exchange rate** and updates
it across the entire system.

## 7. Login

Login is performed using a **phone number and/or email**; the **phone number is mandatory**, while the
**email is optional**. Upon initial registration, the **phone number is verified**.

Login options:

1. Phone number and password.
2. Email and password.
3. "Forgot Password" (involving account and phone number verification).

## 8. Use-case coverage note

A use case not previously mentioned — but found in similar platforms — could be added; it should be
included and implemented according to standard rules to ensure the system covers all relevant
operations and scenarios in this domain.

> **Session-007 disposition of this note:** the missing standard use cases in this domain were
> identified as the customer-initiated **wallet top-up** (only the admin half, `UC-034`, existed) and
> the **wallet statement view** (required by `FR-013` with no use case to trace to). They are authored
> as `UC-041` and `UC-042` in `docs/01-business-analysis/`.

---

## Change History

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 2026-09-28 | Initial content: sponsor-provided transaction-rule specification (restores 0-byte placeholder) | Sponsor input delivered in session 007; defect `D-16` closed; reconciliation registered in `docs/20-validation/` |
