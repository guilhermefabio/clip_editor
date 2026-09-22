# Public-release preparation review

Prepared on branch `chore/public-release-preparation`. No commit, push, repository visibility change, social post, mention, or YouTube upload was performed. `main` was not modified. This is a reviewable preparation, **not clearance to publish the existing history**.

## Tests before and after

| Check | Result |
| --- | --- |
| Baseline `python -m pytest studio/tests -q` | 81 passed in 3.16 s |
| Final suite, same command | 86 passed in 4.30 s |
| Harness CLI `python harness/shorts.py --help` | Passed |
| Git whitespace check | Passed |
| Notebook cells versus HEAD | Code/markdown sources unchanged; outputs and execution counts cleared |
| Legacy script content versus HEAD | Same content, accounting for Git checkout line endings |
| Production state preservation | All 25 files removed from index still exist locally |
| Historical scorer metadata | Unchanged |

Both pytest runs reported the same sandbox permission warning when writing the pytest cache. No test failures or skips. The suite includes real FFmpeg-generated video/audio merge tests and mocked YouTube API tests; it does not require private media or credentials. Added five tests cover recording/still group equivalence, explicit provenance, unknown-origin exclusion on both sides of CV, fold metrics, single-class/one-recording limits, and local/PATH/missing FFmpeg discovery.

`harness/validar_harness.py` is a separate historical real-media validator, not part of pytest. Its two referenced source videos are absent, so it was not run. No full-size Short was rendered. GitHub Actions is configured, but no remote CI run or clean-environment package installation was performed. JavaScript changes only distinguish evaluation and suggested thresholds; no browser UI automation was run.

## Changes

- Reframed the English README around the end-to-end ML pipeline, with Mermaid, experimental metrics, installation, explicit missing-data/weights prerequisites and non-affiliation notice. Added model card, dataset provenance, dependency/license review, demo guide, contribution and security documentation.
- Fixed the evaluation namespace mismatch between raw recordings and screenshots. Unknown screenshot origins and unmapped kill clips are retained for the final fit but excluded from both training/test CV partitions. Added a private provenance mapping and removed truncation of kill-clip group names.
- Added group/fold counts, per-fold class counts/metrics, mean/std and explicit undefined/skipped-fold handling. Removed the single-recording temporal fallback from independent validation reporting. Primary PR/F1 now use fixed 0.5; operational threshold tuning is reported separately as a non-independent diagnostic. Studio labels show the applicable evaluation threshold.
- Added a shared media-tool resolver used by Studio, harness rendering/CLI and frame review: `_tools/` first, PATH second, actionable error otherwise. Kept Windows artwork fonts and default rendering behavior.
- Made Torch/torchvision explicit requirements. Added a direct-version snapshot, preserving the existing script layout rather than introducing package/import changes through pyproject.toml.
- Added Windows/Python 3.13 GitHub Actions with FFmpeg installation and the full Studio test suite. Added `.gitattributes` to exclude notebooks from primary language statistics.
- Cleared notebook outputs while preserving all cell sources. Original output-bearing notebook and old Studio session notes are backed up under ignored `legacy/local/`.
- Added generic `examples/example_plan.json`; retained the approved historical harness example as an editorial reference. Expanded ignore rules for credentials, databases, datasets, weights, logs and generated state.

## Files moved / removed only from tracking

Moved unchanged historical scripts into `legacy/`:

- `1_PREPARAR_CLIPES.bat`
- `2_EXTRAIR_AUDIO.bat`
- `3_RENDER_FINAL.bat`
- `4_RENDER_5_SHORTS.bat`
- `phonk_fps.py`

No active Studio/harness references to these entry points were found. Old relative-path scripts are archived, not supported entry points from their new directory.

Removed **only from Git's index**, preserving original disk paths: `harness/historico.json`, `harness/inventario.json` and 23 tracked `harness/plano*.json` files. The pre-existing untracked `harness/plano_lote22.json` remains local and is now ignored. This preserves duplicate tracking, batch numbering, music-grid discovery and historical plans for the installed pipeline. Do not delete those local records when reviewing the staged removals.

## ML metrics

No model was retrained or overwritten and no production metric was recalculated. Historical metadata stays at ROC-AUC 0.8038, AP 0.3804, precision 0.443, recall 0.383 and F1 0.411, threshold 0.300. New fold means/std cannot be recovered from those aggregate numbers. They will be calculated from actual predictions on the next explicit training run. New recording-disjoint results may be materially lower or unavailable where provenance is insufficient; that is a correction in evaluation scope, not proof of a model regression.

## Security/history review

Neither gitleaks nor trufflehog was available on PATH. The included `scripts/audit_secrets.py` scanned all two commits reachable through local refs (115 unique blob/path combinations), current tracked/untracked nonignored files and local credential locations using known patterns. It reports only paths, commit IDs and candidate types, never matched values. The local machine-readable report is ignored at `docs/local/security-audit.json`.

No confirmed credential was found. The pattern report flagged `studio/notebooks/modelo_elementos.ipynb` in commit `79fcced8501f8278dae51da9190278eeb182354a`:

- Apparent Google refresh-token strings were manually located inside PNG base64 outputs (six pattern matches across cells 10, 14 and 18), not source code or text token fields. Classified as image-data false positives.
- Personal Windows paths occur in historical notebook outputs. The current notebook has those outputs cleared.

Historical tracked paths contain no `.env`, SQLite, raw video, NPZ, joblib or model-weight file extensions checked in the audit. This is a pattern/path check, not proof that no secret or private content exists. Unreachable Git objects, remote-only refs and arbitrary entropy-based secrets were not audited. Existing notebook outputs embed gameplay images; their privacy and publication rights were not approved here. Old production plans and paths also remain accessible in previous commits.

**Before publication, review/sanitize the old notebook and production-state history or prepare a clean source-only publication history.** No history was rewritten in this preparation. Run a dedicated scanner such as gitleaks on the final candidate history when available. A clean current tree and `.gitignore` do not make old commits private.

## Remaining decisions and compatibility limits

1. **License resolved: GNU AGPL v3.0 only** (`AGPL-3.0-only`), as selected by the owner. `LICENSE` now contains the complete license text, and the English documentation, contribution guide and dependency review reflect that choice. This follow-up changes documentation only; the license copy was verified byte-for-byte against the installed distribution, and staged whitespace/link checks were run. The application tests were not rerun for this documentation-only follow-up. Third-party materials retain their own terms; see [dependency review](DEPENDENCIES.md).
2. Historical image/path/production-state review remains a publication gate. An English conceptual pipeline GIF was subsequently created from real working footage at the owner's request; Studio UI screenshots remain pending.
3. A fresh clone requires user-supplied data, weights and permitted music. Historical private metrics are not independently reproducible from the repository. Direct dependency constraints are not a complete transitive lock.
4. Future training intentionally changes grouping/validation and may change suggested thresholds. Existing scorer artifacts and installed editing/rendering presets remain unchanged. Unknown-origin data can train the final model but do not support its held-out claims.
5. Exact hashes cannot identify all overlapping/re-encoded sources or same-session recordings. Curated provenance and an untouched test set remain necessary. Internal early stopping is row-based within outer training data; older standalone image-model experiments are separate.
6. Legacy entry-point paths changed. Production history no longer ships in a clone. Missing FFmpeg/FFprobe now fail with an explicit setup error. Windows/Python 3.13 is the only tested environment; full rendering uses Windows fonts, and the Studio renderer defaults to NVENC. CPU rendering is exposed by the harness.

Review the staged diff with `git diff --cached --stat` and `git diff --cached`. All changes are left for owner review without committing or publishing.

## English documentation follow-up

All Markdown files in the public source tree now use English, including
`AGENTS.md`, the Studio/harness guides, and the YouTube collector guide. The
superseded Portuguese introduction is preserved only in ignored
`legacy/local/README.pt-BR.before-english.md`; the main README no longer links
to a separate Portuguese edition. Private historical backups and generated
production records were preserved rather than rewritten.

Actual paths, command names, configuration keys, and the approved editorial
preset remain unchanged. The application UI and notebook cells are outside
this Markdown-only translation. Documentation explains that the current UI
uses Portuguese labels. Existing technical details and operating constraints
were retained; stale fixed batch numbering and illustrative JSON syntax were
clarified while translating.

Validation: reviewed every public Markdown file for remaining Portuguese prose
and checked relative documentation links. No runtime code changed, so the
previous 86-passing-test result remains the latest application test run.

## Real-footage GIF follow-up

Replaced `docs/assets/pipeline_bodycam.gif` with a minimal English animation
showing source gameplay, saved model scores, three selected moments, a conceptual
beat-aligned timeline, and an excerpt of the matching vertical export. Linked it
near the top of the README. Added a reproducible local builder and asset notes.
Original videos and model artifacts were not changed. The previous GIF and input
provenance remain in ignored `docs/local/demo/`.

The 15.7-second, 960×540 GIF was decoded for frame/duration checks and inspected
through representative frames from all five stages and the final action sequence.
The diagram is conceptual; scores and footage come from the actual local project.
No publication or full-length playback review is claimed.
