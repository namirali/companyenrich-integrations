# Haystack CompanyEnrich integration preparation

The tested components, thirteen-tool toolset, package metadata, documentation, and tests are on the
[CompanyEnrich branch in the Haystack fork](https://github.com/namirali/haystack-core-integrations/tree/codex/companyenrich-integration/integrations/companyenrich).
The [integration proposal](https://github.com/deepset-ai/haystack-core-integrations/issues/4179) is open.
There is no upstream PR yet. Proposal acceptance is not an explicit prerequisite for opening a PR;
the remaining submission work is live API validation and publishing the prepared CI workflow changes.

`CompanyEnrichCompanyEnricher` and `CompanyEnrichCompanyEnricherTool` retain their domain-enrichment APIs. Eleven additional core components and an advanced request component provide company/people discovery, lookup, workforce, property and batch enrichment, ID retrieval and counts. `CompanyEnrichToolset` exposes all thirteen tools. The fixed advanced selector covers 42 documented operations, including the twelve core routes; see [coverage](../ENDPOINT_COVERAGE.md).

Components preserve full responses, support native sync/async HTTP and use Haystack `Secret`. New operations make one request without retries; the original enricher keeps its explicit user-configured retry option, defaulting to zero. Beta email operations require explicit opt-in, exports require explicit counts, and job/status URLs are never followed automatically. Obtain a key from the
[CompanyEnrich dashboard](https://app.companyenrich.com/).

## Install source

```bash
pip install "git+https://github.com/namirali/haystack-core-integrations.git@codex/companyenrich-integration#subdirectory=integrations/companyenrich"
```

## Pending CI patch

`upstream-ci.patch` is inert review material. It is **not active CI**. GitHub rejected pushing
workflow changes because the current OAuth token lacks the `workflow` scope. The source branch
therefore omits the new CompanyEnrich workflow and coverage-workflow registration. The patch
contains those two files. The expanded source commit is `932face`.

With `companyenrich-integrations` and `haystack-core-integrations` checked out as sibling directories,
run these commands **from the root of the Haystack checkout** on `codex/companyenrich-integration`:

```bash
git apply --check ../companyenrich-integrations/haystack/upstream-ci.patch
git apply ../companyenrich-integrations/haystack/upstream-ci.patch
```

A maintainer or credential authorized for workflow changes must review and push the applied files.
The proposed workflow gates paid tests behind the `COMPANYENRICH_RUN_PAID_TESTS=1` repository variable
and `COMPANYENRICH_API_KEY` secret, only on Linux/Python 3.11. It does not retry paid tests.

## Verification and remaining submission requirement

Verified with Python 3.12 on macOS and Haystack 3.4.1:

- 210 mocked unit tests passed, covering sync/async HTTP, credentials, errors, timeout, validation,
  component/tool serialization, and actual tool invocation.
- Ruff lint and formatting passed.
- Full Hatch mypy check passed for all nine source modules.
- Hatch built the wheel and source archive; documentation generation passed.
- Two live tests skipped because no API key or paid-test opt-in was supplied.

Haystack's [agent guidelines](https://github.com/deepset-ai/haystack-core-integrations/blob/main/AGENTS.md)
require contributors to run external API tests locally with a personal key before submission.
This has not been done, so the upstream PR is withheld. From `integrations/companyenrich`, after
supplying an authorized key and explicitly opting into two credit-consuming calls:

```bash
export COMPANYENRICH_RUN_PAID_TESTS=1
hatch run test:integration
```

The two existing live smoke tests cover domain enrichment and consume two CompanyEnrich credits in total. They do not constitute live validation of the expanded endpoint set. No live authenticated API or LLM request
has been performed during this work. Other Python/OS combinations have not been tested locally.
