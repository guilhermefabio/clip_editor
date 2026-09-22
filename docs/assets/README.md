# Pipeline demo

`pipeline_bodycam.gif` is the English visual introduction to clip_editor:

**Original gameplay → Interest curve → Peak selection → Shorts assembled → Final result.**

The 960×540 looping GIF uses real footage from the working BODYCAM recordings,
actual cached interest scores, three cut intervals from an existing edit plan,
and an excerpt of the matching rendered Short. The diagram and timeline are a
minimal conceptual presentation, not a recording of the Studio UI. Three cuts
illustrate the workflow; they are not the complete edit plan.

The GIF preview replaces the existing Portuguese title/footer with English
captions. Gameplay images and the original video files remain unchanged.
The last readable output frame is briefly held before the animation loops.
GIF has no audio. This local asset creation does not publish any media.

`scripts/build_pipeline_demo.py` builds the asset with Pillow and FFmpeg using
explicit `--recording`, `--scores`, `--plan`, and optional `--short-index` inputs.
It requires the matching private media and the merged recording's `.origens.json`
map; those files are not distributed. The precise inputs, score peak timestamps,
and review frames are saved locally under ignored `docs/local/demo/`. The previous
GIF is backed up there as `pipeline_bodycam.previous.gif`.
