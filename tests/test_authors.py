"""Unit tests for the tt_gutenberg package.

Run from the project folder with:
    python -m unittest discover tests
"""

import unittest

import tt_gutenberg.authors as authors
from tt_gutenberg.authors import list_authors
from tt_gutenberg.transform import add_birth_century, translation_counts

import pandas as pd


class TestListAuthors(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load the data once and reuse it in every test (it's slow to load).
        cls.result = list_authors(by_languages=True, alias=True)

    def test_returns_a_list(self):
        self.assertIsInstance(self.result, list)

    def test_list_is_not_empty(self):
        self.assertGreater(len(self.result), 0)

    def test_contains_only_alias_strings(self):
        # No missing values (NaN) or numbers should sneak into the list.
        for alias in self.result:
            self.assertIsInstance(alias, str)

    def test_no_duplicate_aliases(self):
        self.assertEqual(len(self.result), len(set(self.result)))

    def test_most_translated_alias_is_first(self):
        self.assertIn(self.result[0], ["Grimm, Wilhelm Carl", "Grimm, Jacob Ludwig Carl"])


class TestTransformHelpers(unittest.TestCase):

    def test_translation_counts_sorts_most_to_fewest(self):
        toy = pd.DataFrame({
            "alias": ["A", "A", "A", "B", "C", "C"],
            "language": ["en", "fr", "de", "en", "en", "es"],
        })
        counts = translation_counts(toy)
        self.assertEqual(counts.index.tolist(), ["A", "C", "B"])
        self.assertEqual(counts.tolist(), [3, 2, 1])

    def test_translation_counts_drops_missing_aliases(self):
        toy = pd.DataFrame({
            "alias": ["A", None, None],
            "language": ["en", "fr", "de"],
        })
        self.assertEqual(translation_counts(toy).index.tolist(), ["A"])

    def test_birth_century(self):
        toy = pd.DataFrame({"birthdate": [1753.0, 1800.0, 1899.0]})
        self.assertEqual(add_birth_century(toy)["birth_century"].tolist(), [1700, 1800, 1800])

    def test_authors_module_uses_transform(self):
        # authors.py must reference a function from a different module.
        self.assertEqual(authors.author_languages.__module__, "tt_gutenberg.transform")


if __name__ == "__main__":
    unittest.main()
