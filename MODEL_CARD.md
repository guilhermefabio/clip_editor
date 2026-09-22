# Model card · experimental gameplay interest scorer

## Intended use

Suggest candidate gameplay highlights for human review and beat-aware short-form editing. This is an experimental BODYCAM-specific scorer, not a production system, a state-of-the-art claim, a calibrated kill detector, or a predictor of YouTube success.

## Labels and data

Positive means a sampled frame inside an approved source cut, a frame from a raw kill clip (excluding 0.5 s at either edge where possible), or a manually reviewed `frames/kill` still. A clip label is weak supervision: not every frame depicts a kill.

Negative means a frame outside approved cuts with a 2 s guard band, or a reviewed `frames/nada` still. Unselected gameplay can contain worthwhile action, so negative labels are imperfect. Raw recordings subsample negatives to at most three per positive where positives exist; reviewed stills are not balanced this way. Rendered Shorts and added music are not training input for this scorer.

The historical 2026-09-10 artifact reports 14,363 rows: 1,510 positive and 12,853 negative (10.51% positive), two raw recording sources and a reviewed-frame aggregate containing 490 positive and 9,793 negative stills; no kill clips in that run. Three source entries do not mean three independent recordings. The private dataset and weights are not shipped.

## Algorithm and features

`HistGradientBoostingClassifier`: 400 maximum iterations, learning rate 0.05, depth 6, L2 1.0, random seed 0; internal early stopping uses 15% of the training partition. That internal split is row-based, not recording-disjoint, but never includes the outer test recording. It is a remaining model-selection limitation.

Video is analyzed at 3 FPS, scaled to width 640. Pretrained YOLOv8n person detections are features, not a detector fine-tuned on BODYCAM boxes. HUD heuristics estimate friendly/enemy status. There are 22 base signals and 48 derived signals: motion/center motion, brightness, contrast, saturation, red/flash/dark fractions, edge density, audio RMS/high/low bands, person geometry/confidence, hitmarker and friendly-green signals, and enemy geometry/counts. Temporal windows, spikes, idle and walking flags bring the total to 70. See the feature list in `studio/model/scorer_meta.json`.

Stills have no audio (NaN), no inter-frame motion, and degenerate temporal windows. This modality mismatch can correlate with labels and inflate apparent performance.

## Historical evaluation · not corrected results

| Metric | Recorded value |
| --- | --- |
| Pooled cross-validated ROC-AUC | 0.8038 |
| Pooled Average Precision | 0.3804 |
| Precision / Recall / F1 | 0.443 / 0.383 / 0.411 |
| Suggested threshold | 0.300 |

The artifact says GroupKFold(5), but did not save fold scores or group counts. Those cannot be reconstructed from the JSON. Its raw recording IDs and screenshot IDs used different namespaces; unrecognized screenshots could receive independent groups. These results are provisional and potentially optimistic. Precision/recall/F1 were measured on the same OOF scores used to select the threshold. They are not an independent threshold evaluation. No new training or metrics are claimed by this release preparation.

## Revised validation

The current training code canonicalizes raw recordings and `gt_<sha12>_fXXXXXX` stills to the same recording key. An optional private provenance manifest maps legacy screenshot/clip IDs to the original recording SHA-256. Unknown screenshot origins and unmapped kill clips are excluded from **both sides** of CV, counted explicitly, and retained only for fitting the final model. A hash of an extracted clip is not proof of its original recording. See [provenance instructions](docs/DATASET.md).

GroupKFold uses up to five known recording groups. Fewer than two groups produces no validation estimate. Single-class training folds are skipped explicitly. Single-class test folds have undefined ROC-AUC/AP recorded as null, not fabricated values. Reports include `n_cv_groups`, `n_folds`, each fold's train/test class counts and metrics, valid-fold counts, unweighted mean and population standard deviation for ROC-AUC/AP, and pooled metrics over usable OOF rows. Fold standard deviation is not a confidence interval.

Primary precision/recall/F1 now use a predeclared threshold 0.5. The operational suggested threshold still uses the 35th percentile of positive OOF scores, clipped to [0.3, 0.8], preserving that selection heuristic. Its diagnostic PR/F1 is explicitly labelled as selected and measured on the same predictions. With no usable OOF estimate the threshold defaults to 0.5. Neither evaluation establishes performance of the final fit on unknown-origin samples. A future untouched recording-level test set and nested threshold tuning are needed.

## Limitations and risks

- Recording hashes identify exact copies; they do not detect re-encoded duplicates, overlapping excerpts or separate files from the same session. Provenance must capture those relationships before defensible evaluation. SHA prefixes are conservative group keys, not identity certificates.
- Labels reflect one editor's selection and particular maps, players, capture settings, HUD and music-editing preferences. Rows are highly correlated and are not independent trials.
- Class imbalance makes accuracy misleading; AP depends on prevalence. Sampling changes prevalence relative to continuous footage.
- Dark scenes, HUD changes, menus, false person detections, missing audio/YOLO and compression affect features. Still-image statistics differ from video statistics.
- The 2 s negative guard does not isolate every temporal context window. Keeping the complete source recording in a single outer fold prevents those neighboring windows crossing the outer split.
- No validated generalization to other games, unseen sessions, viewers or platforms. Permutation importance is computed on training rows and is descriptive, not held-out evidence.
- The older standalone `imgset.py --train` experiment has its own evaluation and is not covered by the revised main scorer claims.

## Next steps

Curate recording/session provenance, remove near-duplicates, grow independent recording coverage, create an untouched test set, evaluate video-only versus mixed-still training, run grouped/nested threshold selection, calibrate scores, and study ranking against consented YouTube feedback. Preserve human editorial review throughout.
