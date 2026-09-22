"""Recording-disjoint evaluation and media tool discovery regressions."""
import json
from pathlib import Path
import sys

import numpy as np
import pytest
from sklearn.metrics import roc_auc_score, average_precision_score

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from pipeline import train
import tooling


def test_shared_recording_and_unknown_origins(tmp_path, monkeypatch):
    monkeypatch.setattr(train.C, 'MODEL_DIR', tmp_path)
    groups = ['a' * 12, 'frame:' + 'a' * 12, 'unknown:frame:odd', 'kill:clip']
    assert train._cv_groups(groups).tolist() == ['a' * 12, 'a' * 12, '', '']
    (tmp_path / 'provenance.json').write_text(json.dumps({
        'unknown:frame:odd': 'a' * 64, 'kill:clip': 'a' * 64}))
    assert set(train._cv_groups(groups)) == {'a' * 12}
    (tmp_path / 'provenance.json').write_text('{"kill:clip": "not-a-hash"}')
    with pytest.raises(ValueError, match='SHA-256'):
        train._cv_groups(groups)


class RecordingAwareModel:
    def fit(self, X, y):
        self.seen = set(X[:, 0])
        assert 999 not in self.seen  # unknown samples must not enter training
        return self

    def predict_proba(self, X):
        assert not self.seen.intersection(X[:, 0])
        assert 999 not in X[:, 0]
        return np.column_stack([1 - X[:, 1], X[:, 1]])


def test_fold_metrics_from_real_predictions_and_disjoint_origins(tmp_path, monkeypatch):
    monkeypatch.setattr(train.C, 'MODEL_DIR', tmp_path)
    monkeypatch.setattr(train, '_model', RecordingAwareModel)
    X = np.array([[1, .1], [1, .8], [2, .7], [2, .4], [3, .2], [3, .9], [999, .8]])
    y = np.array([0, 1, 0, 1, 0, 1, 1])
    g = np.array(['a'*12, 'frame:'+'a'*12, 'b'*12, 'frame:'+'b'*12,
                  'c'*12, 'frame:'+'c'*12, 'unknown:frame:odd'])
    r, p, labels = train._evaluate(X, y, g, np.arange(7))
    assert r['n_cv_groups'] == r['n_folds'] == 3
    assert r['n_excluded_unknown_origin'] == 1
    assert r['n_holdout'] == 6
    assert np.array_equal(labels, y[:6])
    assert r['roc_auc'] == pytest.approx(roc_auc_score(labels, p))
    assert r['avg_precision'] == pytest.approx(average_precision_score(labels, p))
    assert r['roc_auc_mean'] == pytest.approx(2/3)
    assert r['roc_auc_std'] == pytest.approx(np.std([1., 0., 1.]))
    assert all(f['test_pos'] == f['test_neg'] == 1 for f in r['folds'])
    assert r['evaluation_threshold'] == .5
    json.dumps(r, allow_nan=False)


def test_single_recording_does_not_fall_back_to_frame_split(tmp_path, monkeypatch):
    monkeypatch.setattr(train.C, 'MODEL_DIR', tmp_path)
    r, p, y = train._evaluate(np.zeros((40, 2)), np.tile([0, 1], 20),
                              np.array(['a'*12]*40), np.arange(40))
    assert p is y is None
    assert r['n_cv_groups'] == 1 and r['n_folds'] == 0


def test_single_class_folds_are_explicit(tmp_path, monkeypatch):
    monkeypatch.setattr(train.C, 'MODEL_DIR', tmp_path)
    r, p, y = train._evaluate(np.zeros((4, 2)), np.array([0, 0, 1, 1]),
                              np.array(['a', 'a', 'b', 'b']), np.arange(4))
    assert p is y is None
    assert all(f['status'].startswith('skipped') for f in r['folds'])
    assert r['roc_auc_mean'] is None
    json.dumps(r, allow_nan=False)


def test_tool_local_precedence_path_fallback_and_error(tmp_path, monkeypatch):
    monkeypatch.setattr(tooling.shutil, 'which', lambda name: '/external/' + name)
    (tmp_path / '_tools').mkdir()
    local = tmp_path / '_tools/ffmpeg.exe'
    local.touch()
    assert tooling.resolve_tool('ffmpeg', tmp_path) == local
    assert tooling.resolve_tool('ffprobe', tmp_path) == Path('/external/ffprobe')
    monkeypatch.setattr(tooling.shutil, 'which', lambda name: None)
    with pytest.raises(FileNotFoundError, match='PATH'):
        tooling.resolve_tool('ffprobe', tmp_path)
