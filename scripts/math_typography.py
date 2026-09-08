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
    r"(\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|\$[^$\n]+\$|https?://[^\s，。；]+|`[^`]+`|[A-Za-z][A-Za-z0-9]+(?:_[A-Za-z0-9]+){2,})"
)

IDENTIFIER = (
    r"[A-Za-zΑ-Ωα-ω][A-Za-z0-9Α-Ωα-ω]*"
    r"(?:_(?:\{[^{}]+\}|[A-Za-z0-9]+)|\^(?:\{[^{}]+\}|[A-Za-z0-9+\-]+))*"
)

ATOM = (
    rf"(?:{IDENTIFIER}(?:\([^()\s，。；]*\)|(?!\())"
    r"|[0-9]+(?:\.[0-9]+)?(?:\^[A-Za-z0-9{}+\-]+)?)"
)

AUTO_MATH_RE = re.compile(
    rf"(?<![\w\\])(?:"
    rf"{ATOM}(?:\s*(?:→|≈|≥|≤|=|∈|∼|±|≠)\s*{ATOM})+(?:d[A-Za-z])?"
    rf"|(?:SE|SO|SU|O|L)\([0-9A-Za-z]+\)"
    rf"|[A-Za-zΑ-Ωα-ω][A-Za-z0-9Α-Ωα-ω]*(?:_\{{[^{{}}]+\}}|_[A-Za-z0-9]+|\^\{{[^{{}}]+\}}|\^[A-Za-z0-9+\-]+)+"
    rf"|[∇∂√]{IDENTIFIER}(?:\([^()\s，。；]*\))?"
    rf"|[A-Za-z][0-9]+"
    rf"|[TXYZQNMLKCDHJxyzthfgupqrknmd]"
    rf"|[Α-Ωα-ω](?:_\{{[^{{}}]+\}}|_[A-Za-z0-9]+|\^\{{[^{{}}]+\}}|\^[A-Za-z0-9+\-]+)*"
    rf")(?![\w])"
)


def _latex_identifier_scripts(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        marker, value = match.group(1), match.group(2)
        if value.startswith("{"):
            return marker + value
        # Unbraced TeX scripts bind one atom. Keep descriptive lowercase
        # subscripts, but do not swallow the next multiplied variable.
        if marker == '^' and value.isalpha() and len(value) > 1:
            return marker + '{' + value[0] + '}' + value[1:]
        m = re.match(r'(\d+)([A-Za-z].*)$|([a-z]+)([A-Z].*)$', value)
        if m:
            first, rest = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
            return marker + '{' + first + '}' + rest
        if value.isalpha() and len(value) > 1:
            return f"{marker}{{\\mathrm{{{value}}}}}"
        return f"{marker}{{{value}}}"

    return re.sub(r"([_^])([A-Za-z0-9]+|\{[^{}]+\})", repl, text)


def to_latex(text: str) -> str:
    """Convert unambiguous Unicode/operator notation to MathJax-safe TeX."""
    converted = text
    for source, target in GREEK_LATEX.items():
        converted = converted.replace(source, target + " " if re.search(re.escape(source) + r"[A-Za-z]", converted) else target)
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


def wrap_legacy_math(text: str) -> str:
    # Old imported cards use ordinary parentheses as math delimiters. Balance
    # nested function calls first, so a subscript cannot be wrapped halfway.
    output = []
    cursor = 0
    while cursor < len(text):
        if text[cursor] != "(":
            output.append(text[cursor]); cursor += 1; continue
        end, depth = cursor + 1, 1
        while end < len(text) and depth:
            if text[end] == "(": depth += 1
            elif text[end] == ")": depth -= 1
            end += 1
        if depth:
            output.append(text[cursor:]); break
        # Adjacent function names keep their argument parentheses. Existing
        # expression matching handles these; they are not prose delimiters.
        if cursor and re.match(r"[A-Za-z0-9_Α-Ωα-ω]", text[cursor-1]):
            output.append(text[cursor:end]); cursor = end; continue
        content = text[cursor + 1:end - 1]
        unmistakable = re.search(r"\\[A-Za-z]+|[_^]|[Α-Ωα-ω]|[=≈≤≥∈∇]", content)
        if unmistakable and not re.search(r"[\u3400-\u9fff]", content):
            output.append(r"\(" + to_latex(content) + r"\)")
        else:
            output.append(text[cursor:end])
        cursor = end
    return "".join(output)


def normalize_inline_math_notation(text: str) -> str:
    """Keep explicit TeX intact; normalize only unmistakable legacy notation."""
    # These legacy rows contain complete aligned equations without delimiters.
    if text.startswith("关键关系："):
        relation = text[len("关键关系："):].strip()
        if not PROTECTED_SPAN_RE.fullmatch(relation):
            if "&" in relation or r"\\" in relation:
                return "关键关系：\n" + r"\[\begin{aligned}" + relation + r"\end{aligned}\]"
            return "关键关系：" + r"\(" + relation + r"\)"
    parts = PROTECTED_SPAN_RE.split(text)
    normalized = []
    for part in parts:
        if not part: continue
        if PROTECTED_SPAN_RE.fullmatch(part):
            normalized.append(part); continue
        part = wrap_legacy_math(part)
        for piece in PROTECTED_SPAN_RE.split(part):
            if not piece: continue
            if PROTECTED_SPAN_RE.fullmatch(piece):
                normalized.append(piece)
            else:
                normalized.append(AUTO_MATH_RE.sub(lambda m: r"\(" + to_latex(m.group()) + r"\)", piece))
    return "".join(normalized)
