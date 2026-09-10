import pandas as pd

from src.pipeline import clean_data, validate_data


def test_clean_data_removes_extra_spaces():
    df = pd.DataFrame({
        "title": ["  Test Movie  "],
        "type": [" Movie "],
        "director": [None],
        "cast": [None],
        "country": [None],
        "date_added": [" January 1, 2020 "],
        "release_year": [2020],
        "rating": ["PG"],
        "duration": ["100 min"],
        "listed_in": ["Dramas"],
        "description": ["A test movie"]
    })

    cleaned = clean_data(df)

    assert cleaned.loc[0, "title"] == "Test Movie"
    assert cleaned.loc[0, "type"] == "Movie"


def test_clean_data_handles_missing_values():
    df = pd.DataFrame({
        "title": ["Test"],
        "type": ["Movie"],
        "director": [None],
        "cast": [None],
        "country": [None],
        "date_added": [None],
        "release_year": [2020],
        "rating": ["PG"],
        "duration": ["100 min"],
        "listed_in": ["Dramas"],
        "description": ["A test movie"]
    })

    cleaned = clean_data(df)

    assert cleaned.loc[0, "director"] == "Unknown"
    assert cleaned.loc[0, "cast"] == "Unknown"
    assert cleaned.loc[0, "country"] == "Unknown"


def test_clean_data_converts_dates():
    df = pd.DataFrame({
        "title": ["Test"],
        "type": ["Movie"],
        "director": ["Director"],
        "cast": ["Actor"],
        "country": ["France"],
        "date_added": ["January 1, 2020"],
        "release_year": [2020],
        "rating": ["PG"],
        "duration": ["100 min"],
        "listed_in": ["Dramas"],
        "description": ["A test movie"]
    })

    cleaned = clean_data(df)

    assert pd.api.types.is_datetime64_any_dtype(cleaned["date_added"])


def test_validate_data():
    df = pd.DataFrame({
        "title": ["Movie 1", "Movie 2"],
        "type": ["Movie", "TV Show"],
        "date_added": pd.to_datetime([
            "2020-01-01",
            "2021-01-01"
        ])
    })

    checks = validate_data(df)

    assert checks["Nombre de lignes"] == 2
    assert checks["Nombre de colonnes"] == 3
    assert checks["Doublons"] == 0
    assert checks["Dates invalides"] == 0
    assert checks["Ratings anormaux"] == 0


def test_clean_data_repairs_duration_in_rating():
    df = pd.DataFrame({
        "title": ["Test Movie"],
        "type": ["Movie"],
        "director": ["Director"],
        "cast": ["Actor"],
        "country": ["France"],
        "date_added": ["January 1, 2020"],
        "release_year": [2020],
        "rating": ["84 min"],
        "duration": [None],
        "listed_in": ["Dramas"],
        "description": ["A test movie"]
    })

    cleaned = clean_data(df)

    assert pd.isna(cleaned.loc[0, "rating"])
    assert cleaned.loc[0, "duration"] == "84 min"
