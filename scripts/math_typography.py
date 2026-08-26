"""Conservative inline-math normalization for paper-card prose.

Authors should still write explicit ``\\(...\\)`` for ambiguous notation.  This
module is a rendering safety net for unmistakable expressions such as
``p_init``, ``h→0``, ``SE(3)``, and Unicode Greek symbols that otherwise inherit
the prose font instead of being typeset by MathJax.
"""

from __future__ import annotations

import re


GREEK_LATEX = {
    "α": r"\alpha", "β": r"\beta", "γ": r"\gamma", "δ": r"\delta",
    "ε": r"\epsilon", "ζ": r"\zeta", "η": r"\eta", "θ": r"\theta",
    "ι": r"\iota", "κ": r"\kappa", "λ": r"\lambda", "μ": r"\mu",
    "ν": r"\nu", "ξ": r"\xi", "π": r"\pi", "ρ": r"\rho",
    "σ": r"\sigma", "τ": r"\tau", "υ": r"\upsilon", "φ": r"\phi",
    "χ": r"\chi", "ψ": r"\psi", "ω": r"\omega",
    "Γ": r"\Gamma", "Δ": r"\Delta", "Θ": r"\Theta", "Λ": r"\Lambda",
    "Ξ": r"\Xi", "Π": r"\Pi", "Σ": r"\Sigma", "Φ": r"\Phi",
    "Ψ": r"\Psi", "Ω": r"\Omega",
}

OPERATOR_LATEX = {
    "→": r"\to ", "≈": r"\approx ", "≥": r"\ge ", "≤": r"\le ",
    "∈": r"\in ", "∼": r"\sim ", "±": r"\pm ", "≠": r"\ne ",
    "∞": r"\infty", "∇": r"\nabla ", "∂": r"\partial ", "√": r"\sqrt ",
}

PROTECTED_SPAN_RE = re.compile(
    r"(\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$[^$\n]+\$|https?://[^\s，。；]+|`[^`]+`)"
)

IDENTIFIER = (
    r"[A-Za-zΑ-Ωα-ω][A-Za-z0-9Α-Ωα-ω]*"
    r"(?:_[A-Za-z0-9{}]+|\^[A-Za-z0-9{}+\-]+)*"
)

ATOM = (
    rf"(?:{IDENTIFIER}(?:\([^()\s，。；]*\)|(?!\())"
    r"|[0-9]+(?:\.[0-9]+)?(?:\^[A-Za-z0-9{}+\-]+)?)"
)

AUTO_MATH_RE = re.compile(
    rf"(?<![\w\\])(?:"
    rf"{ATOM}(?:\s*(?:→|≈|≥|≤|=|∈|∼|±|≠)\s*{ATOM})+(?:d[A-Za-z])?"
    rf"|(?:SE|SO|SU|O|L)\([0-9A-Za-z]+\)"
    rf"|[A-Za-zΑ-Ωα-ω][A-Za-z0-9Α-Ωα-ω]*(?:_[A-Za-z0-9{{}}]+|\^[A-Za-z0-9{{}}+\-]+)+"
    rf"|[∇∂√]{IDENTIFIER}(?:\([^()\s，。；]*\))?"
    rf"|[A-Za-z][0-9]+"
    rf"|[Α-Ωα-ω](?:_[A-Za-z0-9{{}}]+|\^[A-Za-z0-9{{}}+\-]+)*"
    rf")(?![\w])"
)


def _latex_identifier_scripts(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        marker, value = match.group(1), match.group(2)
        if value.startswith("{"):
            return marker + value
        if value.isalpha() and len(value) > 1:
            return f"{marker}{{\\mathrm{{{value}}}}}"
        return f"{marker}{{{value}}}"

    return re.sub(r"([_^])([A-Za-z0-9]+|\{[^{}]+\})", repl, text)


def to_latex(text: str) -> str:
    """Convert unambiguous Unicode/operator notation to MathJax-safe TeX."""
    converted = text
    for source, target in GREEK_LATEX.items():
        converted = converted.replace(source, target)
    for source, target in OPERATOR_LATEX.items():
        converted = converted.replace(source, target)
    converted = _latex_identifier_scripts(converted)
    converted = re.sub(r"\b([A-Za-z])([0-9]+)\b", r"\1_{\2}", converted)
    converted = re.sub(
        r"\b(SE|SO|SU|O|L)(?=\()",
        lambda match: rf"\mathrm{{{match.group(1)}}}",
        converted,
    )
    converted = re.sub(
        r"\b([A-Z]{2,})(?=\s*(?:\\to|\\approx|\\ge|\\le|=|\\in|\\sim|\\pm|\\ne))",
        lambda match: rf"\mathrm{{{match.group(1)}}}",
        converted,
    )
    return re.sub(r"\s+", " ", converted).strip()


def normalize_inline_math_notation(text: str) -> str:
    """Wrap unmistakable bare notation in inline MathJax delimiters."""
    parts = PROTECTED_SPAN_RE.split(text)
    normalized: list[str] = []
    for part in parts:
        if not part:
            continue
        if PROTECTED_SPAN_RE.fullmatch(part):
            normalized.append(part)
            continue
        normalized.append(
            AUTO_MATH_RE.sub(lambda match: rf"\({to_latex(match.group(0))}\)", part)
        )
    return "".join(normalized)
