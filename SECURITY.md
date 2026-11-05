# Security Policy

This repository holds the Informatica / SAS to dbt migration workshop: legacy
Informatica and SAS sources, synthetic seed data, baseline outputs, and the Python
parity tooling under `tools/` (DuckDB, pandas, Snowflake connector).

## Supported Versions

This project is not released as versioned artifacts. Only the latest commit on
`main` is supported; fixes are made on `main` and are not backported.

| Version          | Supported |
| ---------------- | --------- |
| `main` (latest)  | Yes       |
| Any other branch | No        |

## Reporting a Vulnerability

Please **do not** open a public issue, pull request, or discussion for security
problems.

Report privately through GitHub Private Vulnerability Reporting:

1. Open the repository's **Security** tab.
2. Choose **Report a vulnerability** (or go to
   `https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/security/advisories/new`).
3. Describe the issue, affected files (e.g. `tools/`, `baseline/`,
   `.github/workflows/`), reproduction steps, and impact.

Examples of in-scope reports: leaked credentials or Snowflake connection details,
vulnerable pinned dependencies in `requirements.txt`, unsafe handling of input
files in the parity/baseline tooling, or insecure CI workflow configuration.
All data in this repository is synthetic; reports about real customer data
exposure should still be filed privately.

Maintainers (see `.github/CODEOWNERS`) aim to acknowledge reports within
5 business days and will coordinate a fix and disclosure through the private
advisory.
