# Dataset provenance and training

Keep recordings, screenshots, approved cuts, caches and models private. Supply labels from your own gameplay; a fresh clone has no fitted scorer. `python studio/pipeline/train.py` fits and overwrites local scorer artifacts. The release preparation does not run that command.

Recognized screenshots use `gt_<12 lowercase hexadecimal characters>_fXXXXXX.jpg` (PNG/JPEG also accepted). The embedded prefix must belong to the original recording SHA-256, not a rendered Short or independently hashed screenshot. Raw recording groups use the same SHA prefix during evaluation.

Frames with other names remain available for fitting but are marked `unknown:frame:<stem>`. Kill clips keep `kill:<stem>` IDs; their names alone cannot prove parentage. These unknown-origin samples are excluded from training and test partitions during cross-validation. Merely putting unknown files in one shared group would not prevent overlap with a known recording, so it is not used as a workaround.

To restore known provenance, create ignored `studio/model/provenance.json`:

```json
{
  "unknown:frame:my_screenshot": "<full 64-character SHA-256 of original recording>",
  "kill:my_clip": "<same original recording SHA-256>"
}
```

Use real hashes, not those placeholders. Keys may also override an existing `frame:<sha12>` or raw `<sha12>` group when consolidating excerpts from a common source. Map every related group consistently. Values must be full 64-character hexadecimal hashes; invalid entries fail training rather than silently creating independent groups. A renamed or re-encoded clip needs verified provenance, not just a content hash of the clip. Equal stems are conservatively kept together.

The manifest is curator-provided evidence, not automatic proof. Audit originals, extracted clips, merged sources and repeated sessions for overlap. GroupKFold only enforces the supplied grouping. Fewer than two known groups means no defensible recording-disjoint estimate, explicitly reported by training.
