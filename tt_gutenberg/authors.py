"""Author-level summaries built on the functions in transform.py."""

import matplotlib.pyplot as plt
import seaborn as sns

from tt_gutenberg.transform import (
    add_birth_century,
    author_languages,
    translation_counts,
)


def list_authors(by_languages=True, alias=True):
    """Return author aliases ordered from most to fewest translations."""
    df = author_languages()
    counts = translation_counts(df, by_languages=by_languages, alias=alias)
    return counts.index.tolist()


def plot_translations(over="birth_century"):
    """Bar plot of the average number of languages per author by birth century."""
    df = add_birth_century(author_languages())

    per_author = (
        df.groupby(["gutenberg_author_id", over])["language"]
        .nunique()
        .reset_index(name="n_languages")
    )

    ax = sns.barplot(data=per_author, x=over, y="n_languages", errorbar=("ci", 95))
    ax.set_xlabel("Birth century")
    ax.set_ylabel("Average number of languages")
    ax.set_title("Author translation count by birth century")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return ax
