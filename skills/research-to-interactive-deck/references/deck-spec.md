# Interactive deck specification

## Required learning arc

Use these roles, combining adjacent roles when that improves flow:

1. Why this topic matters
2. The main idea in one sentence
3. Key words
4. A map of the main parts
5. How it works, step by step
6. A concrete worked example
7. Benefits, limits, and common mistakes
8. A short learning check
9. Summary and next steps
10. Sources and how the research was done

## Simple English

- Write for a beginner who may not be fluent in English.
- Use common words and short sentences. Put one main idea in each sentence.
- Prefer active voice: "The server sends the file," not "The file is sent by the server."
- Use a concrete example before an abstract rule.
- Avoid idioms, jokes, cultural references, and metaphors that need extra explanation.
- Avoid stacked nouns such as "enterprise data access policy framework." Rewrite them as a short phrase or sentence.
- Keep technical terms only when they help the learner. Explain each one with words that are easier than the term itself.
- Do not define one hard term with another hard term.
- Read [simple-english.md](simple-english.md) for the full writing check and preferred replacements.

## Progressive disclosure

- Keep each main section scannable without opening anything.
- Use native `<details><summary>` elements for deeper explanations, edge cases, derivations, and optional examples.
- Mark jargon with `<button class="term" data-definition="...">term</button>` so the template's definition panel explains it on click, Enter, or Space.
- Define a term in plain language in one or two sentences. Add a compact example when useful.
- Do not hide information required to follow the core narrative.

## Visual design

- Use a small color set, plenty of empty space, and clear heading sizes.
- Prefer diagrams made with clear HTML and CSS. Use SVG only when it makes an idea easier to understand.
- Avoid decorative charts, stock imagery, gradients that reduce legibility, and walls of cards.
- Keep line length near 65–75 characters and body text at least 16px.
- Ensure the deck remains useful when printed or JavaScript is disabled; interactive depth may become inline via `<details>`.

## Navigation and accessibility

- Provide a sticky navigation bar with short, clear section labels.
- Support previous/next controls and left/right arrow keys when focus is not inside an interactive control.
- Preserve native scrolling and anchor links.
- Put focus into the definition panel when it opens and return focus to the triggering term when it closes.
- Include `aria-live` for progress changes only if announcements are concise.
- Honor `prefers-reduced-motion`.

## Citation design

- Add small linked source numbers beside the claims they support.
- Use descriptive source labels and direct HTTPS links in the final source section.
- Include publisher and publication/update date when available, plus the research access date.
- Avoid lists of bare URLs, source numbers with no matching source, and citations that appear only on hover.

## Completion checklist

- A beginner can state the purpose, key words, basic model, how it works, one example, and its benefits and limits.
- Every specialist term in the main path is defined or deliberately replaced with plain language.
- Most sentences contain 8–20 words, and no learner-facing sentence contains more than 30 words.
- Common inflated phrases have been replaced with short, direct words.
- Important claims are cited and source links match the claims.
- All controls work with mouse and keyboard.
- Layout works around 390px and 1440px widths.
- No placeholder text, broken anchors, remote runtime dependency, or console error remains.
