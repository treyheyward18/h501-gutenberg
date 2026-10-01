"""Functions that load and reshape the Gutenberg data."""

from pathlib import Path

import pandas as pd


def load_table(name):
    """Return one Gutenberg table (e.g. "authors") as a DataFrame.

    The first call downloads the CSV from TidyTuesday and saves a copy in a
    local data/ folder; later calls read that copy. (*.csv is in .gitignore,
    so the data never gets committed.)
    """
    base_url = (
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/"
        "main/data/2025/2025-06-03/"
    )
    local_file = Path("data") / f"gutenberg_{name}.csv"

    if local_file.exists():
        return pd.read_csv(local_file)

    df = pd.read_csv(base_url + f"gutenberg_{name}.csv")
    local_file.parent.mkdir(exist_ok=True)
    df.to_csv(local_file, index=False)
    return df


def author_languages():
    """Return one row per (book, language, author) combination.

    metadata links each book to its author; languages lists every language
    each book is available in; authors holds the alias and birthdate.
    """
    metadata = load_table("metadata")[["gutenberg_id", "gutenberg_author_id"]]
    languages = load_table("languages")[["gutenberg_id", "language"]]
    authors = load_table("authors")[["gutenberg_author_id", "author", "alias", "birthdate"]]

    books = metadata.merge(languages, on="gutenberg_id", how="inner")
    return books.merge(authors, on="gutenberg_author_id", how="inner")


def translation_counts(df, by_languages=True, alias=True):
    """Count translations per author (or per alias), most first.

    by_languages=True counts the distinct languages an author's works appear
    in; by_languages=False counts every (book, language) row instead.
    """
    key = "alias" if alias else "gutenberg_author_id"
    df = df.dropna(subset=[key])  # drop authors with no alias recorded

    if by_languages:
        counts = df.groupby(key)["language"].nunique()
    else:
        counts = df.groupby(key)["language"].count()

    return counts.sort_values(ascending=False)


def add_birth_century(df):
    """Add a birth_century column, e.g. 1753.0 -> 1700."""
    df = df.dropna(subset=["birthdate"]).copy()
    df["birth_century"] = (df["birthdate"] // 100 * 100).astype(int)
    return df
