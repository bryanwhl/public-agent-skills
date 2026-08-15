# Interactive deck specification

## Required learning arc

Use these roles, combining adjacent roles when that improves flow:

1. Why this topic matters
2. The one-sentence model
3. Essential vocabulary
4. System or concept map
5. How it works, step by step
6. A concrete worked example
7. Tradeoffs, limits, and misconceptions
8. A knowledge check or reflection prompt
9. Summary and next steps
10. Sources and methodology

## Progressive disclosure

- Keep each main section scannable without opening anything.
- Use native `<details><summary>` elements for deeper explanations, edge cases, derivations, and optional examples.
- Mark jargon with `<button class="term" data-definition="...">term</button>` so the template's definition panel explains it on click, Enter, or Space.
- Define a term in plain language in one or two sentences. Add a compact example when useful.
- Do not hide information required to follow the core narrative.

## Visual design

- Use a restrained palette, generous whitespace, and one dominant visual hierarchy.
- Prefer diagrams made with semantic HTML and CSS. Use SVG only when it materially improves understanding.
- Avoid decorative charts, stock imagery, gradients that reduce legibility, and walls of cards.
- Keep line length near 65–75 characters and body text at least 16px.
- Ensure the deck remains useful when printed or JavaScript is disabled; interactive depth may become inline via `<details>`.

## Navigation and accessibility

- Provide a sticky progress/navigation bar with meaningful section labels.
- Support previous/next controls and left/right arrow keys when focus is not inside an interactive control.
- Preserve native scrolling and anchor links.
- Put focus into the definition panel when it opens and return focus to the triggering term when it closes.
- Include `aria-live` for progress changes only if announcements are concise.
- Honor `prefers-reduced-motion`.

## Citation design

- Add compact linked citation markers beside the claims they support.
- Use descriptive source labels and direct HTTPS links in the final source section.
- Include publisher and publication/update date when available, plus the research access date.
- Avoid raw URL dumps, orphaned footnotes, and citations that are only visible on hover.

## Completion checklist

- A beginner can state the purpose, vocabulary, mental model, mechanism, example, and tradeoffs.
- Every specialist term in the main path is defined or deliberately replaced with plain language.
- Important claims are cited and source links match the claims.
- All controls work with mouse and keyboard.
- Layout works around 390px and 1440px widths.
- No placeholder text, broken anchors, remote runtime dependency, or console error remains.
