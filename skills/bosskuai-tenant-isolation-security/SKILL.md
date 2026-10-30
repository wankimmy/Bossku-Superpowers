---
name: bosskuai-tenant-isolation-security
description: "Use when checking multi-tenant data isolation: organization scoping, cross-tenant leaks, authorization boundaries, row-level access, and SaaS tenant security review."
---

# BosskuAI Tenant Isolation Security

Use this skill when the question is **whether tenant A can ever observe tenant B's data**, through any path.

## How this differs from nearby skills

- **`bosskuai-cybersecurity-risk`**: covers the whole threat surface; this skill covers only the tenant boundary.
- **`bosskuai-database-engineering`**: designs schema and indexes; this skill checks that every access path carries a tenant predicate.
- **`bosskuai-business-logic-review`**: validates workflow correctness; this skill assumes the workflow is right and asks who can see the result.
- **`bosskuai-laravel-security`**: Laravel-specific policy/gate mechanics; this skill is framework-neutral.

## Treat as high severity

Any confirmed cross-tenant read or write is an incident, not a bug ticket. Establish exposure window, affected tenants, and affected record counts before discussing the fix.

## Where isolation actually leaks

Check each path independently. A correct controller does not imply a correct export.

- **Queries and relations**: nested/eager loads and `whereHas` that scope the parent but not the child.
- **Direct object references**: any lookup by id that omits the tenant predicate.
- **Cache keys**: keys missing a tenant segment serve one tenant's payload to another.
- **Background jobs**: serialized job payloads that resolve tenant context at run time rather than enqueue time.
- **Exports, reports, invoices, PDFs**: batch paths that bypass the request-scoped tenant guard.
- **Webhooks and callbacks**: inbound handlers that trust a tenant id from the payload.
- **Search indexes**: shared indexes without a tenant filter applied at query time.
- **Aggregates and analytics**: counts and dashboards computed across the whole table.
- **File and object storage**: predictable paths or signed URLs without tenant checks.
- **Admin and impersonation**: elevated roles that silently widen scope.
- **Row-level security itself**: table owners and superusers bypass RLS unless `FORCE ROW LEVEL SECURITY` is set; a tenant id set with session-level `SET` leaks to the next borrower under transaction pooling (use `SET LOCAL` inside the transaction); on Supabase/PostgREST a table with RLS disabled is readable with the public anon key.
- **Vector stores and RAG retrieval**: a shared embedding index without a tenant filter at query time returns another tenant's chunks to the model.
- **Unique keys and permission caches**: a global unique index, or an "already taken" error, shows tenant A that tenant B has a value. A cached "allowed" answer keeps working after a role change, so key permission caches by tenant and user, and clear them when a role or membership changes.
- **Tenant moves, deletes and restores**: a user moved to another tenant, or a deleted tenant, keeps sessions, tokens, files, cache and search entries that point at the old tenant until they expire. A restore from backup can bring a deleted tenant back, so run the deletion again after any restore.

## Identity checks that tenant scope depends on

- **SSO and SCIM**: per-tenant IdP config must not let one tenant's IdP assert users into another; deprovisioning must revoke sessions and tokens, not only disable the login.
- **Tokens**: tenant comes from the authenticated context, not from a claim the client can swap. Refresh tokens rotate; a reused one revokes the whole family and raises an alert.
- **Recovery and impersonation**: password reset, MFA reset and support impersonation are the common bypasses. Test them across tenants, and write an audit event for each.
- Auth changes need failure-path tests: expired, revoked, replayed, cross-tenant.

## Guardrails

- Enforce tenant scope **server-side**. Never trust `tenant_id`, `org_id`, or a workspace slug supplied by the client.
- Prefer a default-deny mechanism (global scope, row-level security, repository base query) over remembering to filter at each call site.
- A missing tenant filter is not fixed by adding one filter; find the shared helper and fix the class of bug.
- Do not rely on UUIDs as a security control. Unguessable is not unauthorized.
- Do not close an isolation finding without a regression test.
- Do not fill `tenant_id` from a default or a guess in a backfill. Take it from the parent row, and check that every child matches its parent's tenant.
- Do not copy production data for testing without masking personal fields. The copy holds every tenant, so keep it off public hosts.

## Required regression tests

Every fix adds at least these cases:

- Same user, different tenant: must be denied.
- Same tenant, different role: must respect role limits.
- Unauthenticated access to the same resource: must be denied.
- The batch path (job, export, or report) that mirrors the fixed request path.
- Two tenants with the same ids, names and values, so a query that forgets the tenant returns the other tenant's row.

## Output format

```text
Boundary: [what separates tenants: column, schema, database, index filter]
Enforcement: [where it is applied, and whether it is default-deny]

Findings:
  P0/P1/P2 - [path] - [how it leaks] - [fix]

Exposure (if a leak is confirmed):
  Window: [when it became reachable]
  Affected: [tenants / records, or how to determine]

Fix plan: [smallest change that closes the class, not the instance]
Regression tests: [cases added]
Verification: [what was actually run]
```

## References

- `../../references/checklists/tenant-isolation-security-checklist.md`
- `../../references/checklists/engineering-quality-bar.md`

Adapted from engineering/engineering-identity-access-engineer.md (agency-agents, MIT).
