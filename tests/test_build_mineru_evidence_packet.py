import json
import unittest

from scripts.build_mineru_evidence_packet import (
    PACKET_TOKEN_TARGET,
    approximate_tokens,
    fit_packet_to_target,
    markdown_equations,
    markdown_images,
    selected_sections,
)


class MineruEvidencePacketTests(unittest.TestCase):
    def test_selects_relevant_sections(self) -> None:
        markdown = """# Title
front matter
## Introduction
question
## Methods
method body
## Appendix
details
## Results
result body
"""
        self.assertEqual(
            [section["title"] for section in selected_sections(markdown)],
            ["Introduction", "Methods", "Results"],
        )

    def test_extracts_unique_equations_and_images(self) -> None:
        markdown = """
$$E = mc^2$$
$$E = mc^2$$
\\[F = ma\\]
![phase diagram](images/figure-1.jpg)
"""
        self.assertEqual(markdown_equations(markdown), ["E = mc^2", "F = ma"])
        self.assertEqual(
            markdown_images(markdown),
            [{"alt": "phase diagram", "path": "images/figure-1.jpg"}],
        )

    def test_approximate_tokens_rounds_up(self) -> None:
        self.assertEqual(approximate_tokens("12345"), 2)

    def test_fits_packet_by_trimming_long_section_tails(self) -> None:
        packet = {
            "fixed": "x" * (PACKET_TOKEN_TARGET * 4 - 1_000),
            "mineru_sections": [{"title": "Results", "text": "y" * 1_800}],
        }
        fit_packet_to_target(packet)
        self.assertLessEqual(
            approximate_tokens(json.dumps(packet)),
            PACKET_TOKEN_TARGET,
        )
        self.assertGreaterEqual(len(packet["mineru_sections"][0]["text"]), 600)


if __name__ == "__main__":
    unittest.main()
