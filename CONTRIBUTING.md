# Contributing

This project is licensed under GNU AGPL v3.0 only (`AGPL-3.0-only`); see [LICENSE](LICENSE). Contributions to the project must be provided under the same license. Preserve third-party copyright and license notices, and identify any separately licensed material you propose to add.

Use Windows/Python 3.13, install FFmpeg/FFprobe and `studio/requirements.txt`, and run `python -m pytest studio/tests -q`. Tests synthesize media and must not depend on private recordings, credentials, trained weights or YouTube access. GitHub Actions runs the same tests on Windows.

Use a feature branch. Keep Studio + harness behavior compatible, preserve original media and production history, and include regression tests for behavior changes. Never commit `.env`, OAuth credentials/tokens, SQLite databases, logs, private datasets, weights or exports. Clear notebook outputs before committing. Review `git diff --cached` and `git status --ignored` selectively; do not paste credential contents.

For ML changes, document recording provenance, sampling, class counts, fold metrics and threshold selection. Do not promote historical or training-set scores to independent benchmark results. Run `python scripts/audit_secrets.py` before a release and inspect its local report; a pattern scan alone is not a security guarantee.

Describe the problem, resulting behavior and validation in pull requests. Publishing media, uploading to YouTube and posting to social platforms require separate owner authorization.
