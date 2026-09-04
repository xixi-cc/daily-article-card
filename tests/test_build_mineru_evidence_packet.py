import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.build_mineru_evidence_packet import (
    PACKET_TOKEN_TARGET,
    approximate_tokens,
    authoritative_pdf_pages,
    fit_packet_to_target,
    markdown_equations,
    markdown_images,
    selected_sections,
)
from scripts.build_fulltext_evidence_packets import first_matching_excerpt


class MineruEvidencePacketTests(unittest.TestCase):
    @patch("scripts.build_mineru_evidence_packet.subprocess.run")
    def test_uses_pdfinfo_and_page_bounded_text_extraction(self, run) -> None:
        run.side_effect = [
            subprocess.CompletedProcess([], 0, "Pages:           2\n", ""),
            subprocess.CompletedProcess([], 0, "first page\fembedded\f", ""),
            subprocess.CompletedProcess([], 0, "second page\f", ""),
        ]

        self.assertEqual(
            authoritative_pdf_pages(Path("paper.pdf")),
            ["first page\fembedded", "second page"],
        )
        self.assertEqual(run.call_count, 3)
        self.assertEqual(run.call_args_list[1].args[0][3:7], ["1", "-l", "1", "paper.pdf"])

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

    def test_heading_excerpt_skips_pathological_oversized_pdf_line(self) -> None:
        pages = ["x" * 2_000_000 + "\n2 METHODS\nThe method follows here."]

        excerpt = first_matching_excerpt(
            pages,
            (r"^\s*\d+\s+METHODS\s*$",),
        )

        self.assertIsNotNone(excerpt)
        self.assertEqual(excerpt["page"], 1)
        self.assertEqual(excerpt["matched"], "2 METHODS")
        self.assertIn("The method follows here.", excerpt["text"])


if __name__ == "__main__":
    unittest.main()
