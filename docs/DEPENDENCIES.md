# Dependency and license review

The project is licensed under **GNU AGPL v3.0 only** (`AGPL-3.0-only`), as selected by the owner. [LICENSE](../LICENSE) contains the full GNU Affero General Public License, version 3, dated 19 November 2007. Its standard text was copied verbatim from the installed Ultralytics distribution license file. Third-party dependencies retain their own licenses; this choice is not an exhaustive transitive compatibility audit.

Direct dependency versions below were read from the installed package metadata on the baseline machine. They document the tested environment, not a complete transitive SBOM or a guarantee about every future release. Requirements use lower bounds; a fresh installation can resolve newer versions.

| Dependency | Locally tested version | Declared license |
| --- | --- | --- |
| fastapi | 0.119.0 | MIT |
| uvicorn | 0.35.0 | BSD-3-Clause |
| pydantic | 2.11.7 | MIT |
| scikit-learn | 1.7.1 | BSD-3-Clause |
| joblib | 1.5.2 | BSD-3-Clause |
| ultralytics | 8.4.143 | AGPL-3.0 |
| opencv-python | 4.12.0.88 | Apache-2.0 |
| pillow | 11.3.0 | MIT-CMU |
| scipy | 1.16.1 | BSD-3-Clause (bundled components have additional notices) |
| numpy | 2.2.6 | BSD-3-Clause (bundled components have additional notices) |
| torch | 2.8.0 | BSD-3-Clause |
| torchvision | 0.23.0 | BSD |
| google-api-python-client | 2.200.0 | Apache-2.0 |
| google-auth | 2.57.1 | Apache-2.0 |
| google-auth-oauthlib | 1.4.1 | Apache-2.0 |
| pytest | 9.0.3 | MIT |

Ultralytics' [official licensing page](https://www.ultralytics.com/license) describes AGPL-3.0 and Enterprise alternatives for its code/models. This is the central reason a blanket MIT label was not applied. The [scikit-learn license](https://github.com/scikit-learn/scikit-learn/blob/main/COPYING) identifies BSD-3-Clause. [FFmpeg's legal page](https://www.ffmpeg.org/legal.html) explains that LGPL/GPL obligations depend on build options; no executable is distributed here. Native wheels may bundle components with further notices. The table is not a legal compatibility opinion or exhaustive transitive audit.

BODYCAM game assets, music, Windows fonts, channel artwork and model weights are not licensed by this repository. Public demos and any redistributed binaries/weights require their own rights review. No Reissad Studio logo has been added.

## Reproducibility scope

The existing script entry points and `studio/requirements.txt` are preserved instead of introducing packaging changes through a `pyproject.toml`. Torch and torchvision are now explicit. Install FFmpeg/FFprobe separately. `studio/constraints-tested.txt` records direct dependency versions observed during local tests; optionally install with:

```powershell
python -m pip install -r studio/requirements.txt -c studio/constraints-tested.txt
```

This is not a complete lockfile: OS wheels, transitive dependencies and FFmpeg builds can differ. Python 3.13 on Windows is the tested target. CI is configured for that target but has not been executed on GitHub during this local preparation. NVIDIA acceleration is optional; CPU rendering is available through the harness `--encoder libx264`. Windows fonts currently prevent claiming portable rendering support.
