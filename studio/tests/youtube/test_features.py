from youtube.features import derived_metrics, growth_between, quality_score

RAW = {
    "views": 1300, "likes": 90, "comments": 10, "shares": 6,
    "subscribersGained": 22, "subscribersLost": 3, "engagedViews": 900,
    "averageViewPercentage": 62.5,
}


def test_derived_basic():
    d = derived_metrics(RAW)
    assert d["engaged_view_rate"] == 900 / 1300
    assert d["likes_per_1000_views"] == 90 / 1300 * 1000
    assert d["subs_per_1000_views"] == 22 / 1300 * 1000
    assert d["net_subs_per_1000_views"] == 19 / 1300 * 1000
    assert d["watch_percentage"] == 0.625


def test_derived_zero_views():
    d = derived_metrics({"views": 0, "likes": 5, "engagedViews": 0})
    assert d["likes_per_1000_views"] is None
    assert d["engaged_view_rate"] is None


def test_derived_missing_keys():
    d = derived_metrics({"views": 100})          # sem likes/comments/etc.
    assert d["likes_per_1000_views"] is None
    assert d["watch_percentage"] is None
    assert d["interactions_per_1000_views"] is None


def test_quality_score_range_and_weights():
    q = quality_score(RAW)
    assert 0.0 <= q["quality_score"] <= 1.0
    assert set(q["components"]) == {
        "retention", "engaged_view_rate", "engagement", "subscriber_conversion"}
    # pesos custom mudam o resultado
    q2 = quality_score(RAW, weights={"retention": 1, "engaged_view_rate": 0,
                                     "engagement": 0, "subscriber_conversion": 0})
    assert q2["quality_score"] == q["components"]["retention"]


def test_quality_score_all_missing():
    q = quality_score({"views": 0})
    assert q["quality_score"] is None
    assert q["missing"] == list(q["components"])


def test_growth_between():
    older = {"views": 800, "engaged_views": 500, "video_age_hours": 24}
    newer = {"views": 1350, "engaged_views": 900, "video_age_hours": 72}
    g = growth_between(older, newer)
    assert g["views_growth_rate"] == (1350 - 800) / 800
    assert g["views_per_hour"] == (1350 - 800) / 48
    assert round(g["engaged_views_growth_rate"], 3) == round(400 / 500, 3)


def test_growth_between_zero_base():
    g = growth_between({"views": 0, "video_age_hours": 1},
                       {"views": 10, "video_age_hours": 6})
    assert g["views_growth_rate"] is None      # base 0 -> sem fração
    assert g["views_per_hour"] == 2.0
