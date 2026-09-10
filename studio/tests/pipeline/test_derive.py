"""``derive.augment``: as features que o scorer realmente vê.

22 sinais base -> + (max, média) em janela ~±1,5 s para 18 deles
              -> + 10 ``*_spike`` (valor menos a média de ~±4 s, piso 0)
              -> + ``idle_flag`` + ``walk_flag``.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from pipeline import derive, features  # noqa: E402

NAMES = list(features.FEATURE_NAMES)
FPS = 3.0


def _mk(n=150, **cols):
    """(times, X) com todas as 17 colunas em 0.1 e overrides por nome."""
    t = np.arange(n) / FPS
    X = np.full((n, len(NAMES)), 0.1, np.float32)
    for name, val in cols.items():
        X[:, NAMES.index(name)] = val
    return t.astype(np.float32), X


def test_augment_feature_count_matches_the_recipe():
    t, X = _mk()
    Xa, names = derive.augment(t, X, NAMES, FPS)
    expected = (len(NAMES)
                + 2 * len([c for c in derive.WINDOW_COLS if c in NAMES])
                + len([c for c in derive.SPIKE_COLS if c in NAMES])
                + 2)  # idle_flag, walk_flag
    assert Xa.shape == (len(t), expected)
    assert len(names) == expected == len(set(names))
    assert names[:len(NAMES)] == NAMES  # base preservada e na ordem


def test_expected_derived_names_present():
    t, X = _mk()
    _, names = derive.augment(t, X, NAMES, FPS)
    for n in ("motion_wmax", "motion_wmean", "flash_frac_spike",
              "person_area_sum_spike", "center_motion_spike",
              "hit_center_spike", "hit_center_wmax",
              "enemy_area_spike", "enemy_count_spike", "friendly_green_wmax",
              "idle_flag", "walk_flag"):
        assert n in names, n
    assert "brightness_spike" not in names and "edge_density_spike" not in names


def test_spike_is_zero_on_a_flat_signal():
    t, X = _mk(red_frac=0.3)  # constante
    Xa, names = derive.augment(t, X, NAMES, FPS)
    assert np.allclose(Xa[:, names.index("red_frac_spike")], 0.0, atol=1e-6)


def test_spike_lights_up_on_a_local_burst():
    t, X = _mk(n=180, flash_frac=0.0)
    X[90:96, NAMES.index("flash_frac")] = 0.8  # ~2 s de flash
    Xa, names = derive.augment(t, X, NAMES, FPS)
    sp = Xa[:, names.index("flash_frac_spike")]
    assert sp[92] > 0.3
    assert sp[10] == 0.0 and sp[170] == 0.0


def test_walk_flag_fires_on_steady_motion_without_combat_spikes():
    # metade parada, metade "andando": movimento global sobe, sem flash nem agudos.
    t, X = _mk(n=160, flash_frac=0.0, audio_hi=0.0)
    mcol = NAMES.index("motion")
    X[:80, mcol] = 0.01
    X[80:, mcol] = 0.20
    Xa, names = derive.augment(t, X, NAMES, FPS)
    walk = Xa[:, names.index("walk_flag")]
    assert walk[110:].mean() > 0.8   # trecho de caminhada
    assert walk[:40].mean() < 0.2    # trecho parado


def test_walk_flag_stays_low_when_combat_spikes_are_present():
    t, X = _mk(n=160, flash_frac=0.0, audio_hi=0.0)
    mcol = NAMES.index("motion")
    X[:80, mcol] = 0.01
    X[80:, mcol] = 0.20
    # tiroteio junto do movimento: flash e agudos pulsando na segunda metade
    X[80:, NAMES.index("flash_frac")] = 0.5
    X[80:, NAMES.index("audio_hi")] = 0.5
    Xa, names = derive.augment(t, X, NAMES, FPS)
    walk = Xa[:, names.index("walk_flag")]
    assert walk.mean() < 0.2


def test_idle_flag_separates_menu_from_action():
    t, X = _mk(center_motion=0.001, audio_rms=0.001)
    Xa, names = derive.augment(t, X, NAMES, FPS)
    assert Xa[:, names.index("idle_flag")].mean() > 0.9

    t, X = _mk(center_motion=0.4, audio_rms=0.2)
    Xa, names = derive.augment(t, X, NAMES, FPS)
    assert Xa[:, names.index("idle_flag")].mean() == 0.0


def test_empty_matrix_is_passthrough():
    Xa, names = derive.augment(np.array([]), np.zeros((0, len(NAMES)), np.float32), NAMES, FPS)
    assert Xa.shape[0] == 0 and names == NAMES


def test_all_nan_column_survives_augment():
    # cache antigo: coluna nova entra como NaN e não quebra o derive
    t, X = _mk()
    X[:, NAMES.index("hit_center")] = np.nan
    Xa, names = derive.augment(t, X, NAMES, FPS)
    assert np.isnan(Xa[:, names.index("hit_center")]).all()
    assert np.isnan(Xa[:, names.index("hit_center_wmax")]).all()
    assert not np.isnan(Xa[:, names.index("motion")]).any()
