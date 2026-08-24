# Simple English guide

Write for a reader who knows basic English but may not speak it at home.

## Core rules

1. Use common words.
2. Keep one main idea in each sentence.
3. Aim for 8–20 words per sentence. Never exceed 30 words.
4. Use active voice when it is clear who does the action.
5. Give a concrete example before adding detail.
6. Name the same thing in the same way each time.
7. Avoid idioms, slang, jokes, and culture-specific references.
8. Remove filler words that do not change the meaning.

## Keep terms consistent

- Choose one name for each technical idea before writing the deck.
- Use that exact name every time. Do not switch to a synonym for variety.
- Keep spelling and capitalization the same.
- At first use, write the full name and its short form: "Transport Layer Security (TLS)."
- After first use, use the same short form: "TLS."
- Use the same simple definition each time the term is clickable.
- List tempting alternate names in the `avoid` field of `terminology` so the build check can catch them.
- If two similar terms mean different things, explain the difference instead of treating them as synonyms.

Example:

Weak:

> The website server sends a certificate. The remote host then proves its identity. The web machine creates a key.

Better:

> The website server sends a certificate. The website server then proves its identity. It creates a key.

## Replace formal phrases

| Avoid | Prefer |
|---|---|
| utilize | use |
| facilitate | help |
| commence | start |
| terminate | stop or end |
| approximately | about |
| subsequently | later or then |
| prior to | before |
| in order to | to |
| due to the fact that | because |
| a large number of | many |
| at this point in time | now |
| with regard to | about |
| has the ability to | can |
| is able to | can |
| for the purpose of | to or for |
| in the event that | if |
| pertaining to | about |

## Explain technical terms

- Keep a technical term only if the learner will see it again in real sources or needs it for the topic.
- State the common-language meaning before adding details.
- Use one or two short sentences.
- Add a familiar example when it helps.
- Do not use unexplained technical words inside the definition.

Weak:

> Consensus is a fault-tolerant mechanism for achieving state-machine replication across distributed nodes.

Better:

> Consensus is a way for several computers to agree on one result. It can still work when some computers fail.

## Final reading check

Read only the title, summaries, and main points in order. Rewrite the deck if:

- a sentence must be read twice;
- two or more new terms appear in one sentence;
- a pronoun such as "it" or "they" has no clear subject;
- an example uses knowledge that a beginner may not have;
- a shorter common word would keep the same meaning;
- a definition is harder than the term it explains.
- the same idea has two names without a clear reason.
