# Open-source contribution workflow

This document describes the intended contribution process for this project.
It is a workflow guide, not evidence that an external contribution, issue,
pull request, review, or merge has already occurred.

## Before starting

1. Find an existing issue or discuss a proposed change with the maintainers.
2. Read the relevant code and documentation; confirm the scope and expected
   behavior before implementation.
3. Create a focused branch from the current default branch, for example
   `fix/ticket-category-label`.
4. Implement the change using the existing Flask/Jinja/SQLAlchemy patterns.
   Keep changes additive where possible and do not include credentials,
   databases, caches, or unrelated files.
5. Add or update tests for behavior changes and run the test suite:

   ```powershell
   python -m pytest -q -p no:cacheprovider tests
   ```

6. Update documentation when behavior, configuration, or setup instructions
   change.
7. Commit the focused change with a clear message, then push the branch to the
   configured remote.
8. Open a Pull Request describing the problem, implementation, test results,
   and any remaining limitations. Link the relevant issue when one exists;
   do not invent issue numbers or contribution evidence.
9. Respond to review feedback with follow-up commits and rerun relevant tests.
10. A maintainer reviews and merges the pull request according to the
    repository's actual settings. Do not claim a merge until it has happened.

## Contribution evidence

Record actual issue, pull request, review, and merge links here only after
they exist. No external contribution evidence is claimed by this document.
