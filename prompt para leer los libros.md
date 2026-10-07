# Munger — reading the books

The PDFs are in the root of this repository. Read the four books listed
below completely, 100 pages at a time, and build one file, `munger.md`, with
everything a later prompt would need to bring Charlie Munger back: how he
decided, what he said in his own words, what he refused, what made him
suspicious, how he behaved. Not a summary. Evidence, with page numbers.

## What goes in munger.md — five sections, entries appended as you read

1. **DECISIONS** — every concrete case where he invested, rejected, waited,
   sold, changed his mind or admitted an error. Entry: the situation as the
   book presents it / what he did / the reason he gave / quote / book, page.
2. **RULES IN HIS WORDS** — principles he stated himself, verbatim. Not a
   paraphrase, not the author's version. Quote / context / book, page.
3. **REFUSALS** — what he would not do, would not estimate, would not touch,
   or called stupid. Quote / book, page.
4. **SIGNALS** — concrete things that made him suspicious of a business, a
   manager, a number or an adviser, and concrete things that made him trust.
   The sign / what it meant to him / quote / book, page.
5. **TEMPERAMENT IN ACTION** — how he behaved under loss, error, disagreement
   or pressure; how he treated people; what he found funny or contemptible.
   Only episodes, with quote and page. No adjectives of your own.

## Rules

- Every entry says who is speaking: **HIM** (his own words) / **REPORTED**
  (someone says he said or did it) / **AUTHOR** (the author's interpretation).
  Never blur these.
- Buffett is not Munger. Record Buffett only when the text ties Munger's own
  reasoning to it, and say so.
- Quote verbatim. Page = the `[PDF PAGE n]` marker in the .txt. Never invent
  a quote or a page.
- Do not summarize chapters. Do not explain Munger. Do not add conclusions.
- Record the mundane: a small decision with a reason beats a famous line.
- Same episode or same statement in a later book: add "also in: book, page"
  to the existing entry. Create a new entry only if the later book has his
  own words where the earlier one only reported them.
- Read every page of the block before writing. Before the first entry, state
  the first and last `[PDF PAGE n]` you actually read. Nothing is skipped.
- If you are not running as Sonnet, say so and stop before reading anything.

## Books, in this order

1. Damn Right! (Lowe) — biography. Most of section 1 lives here.
2. Poor Charlie's Almanack — his own talks. Most of sections 2 and 3.
3. The Complete Investor (Griffin) — his statements organized by topic.
   Expect many "also in"; record what is new.
4. All I Want to Know… (Bevelin 2016) — Buffett and Munger quoted side by
   side. Attribution matters most here.

Not read: Seeking Wisdom (Bevelin's own thinking, not Munger's words) and
Das Tao des Charlie Munger (translated quotes, no longer his words). Any
other file in the repository is not a source.

## Steps

**Step 0 — set up.** No reading of book content in this step.
(a) For each of the four books, produce `<book>.txt` next to the PDF, with a
    line `[PDF PAGE n]` at the start of every page. Use pdftotext if it is
    installed, otherwise Python with pypdf.
(b) Create `munger.md` with a header listing each book, its page count and
    its blocks (1–100, 101–200, …), the five empty sections, and the line
    `Covered: nothing yet`.
(c) Create a runner script for this machine (`run.sh`, or `run.ps1` on
    Windows): for every block of the four books, in book order, one line
    that prints the block, the model and the effort, then one line:
    `claude -p --model sonnet --effort high --permission-mode acceptEdits "<book>, pages a–b"`
(d) Report the page counts and the number of blocks, then stop.

**Step 1 — one block.** Given `"<book>, pages a–b"`: if the `Covered:` line
in `munger.md` already includes these pages, say so and stop without
reading. Otherwise read the block, append entries to the five sections,
update the `Covered:` line, and stop. Your last line: the block done, the
model and effort used, and the next block in order.

## How to run

1. `claude --model sonnet --effort low` → type `Step 0`.
2. `claude --model sonnet --effort high` → type `Damn Right!, pages 1–100`.
   Watch this one. Read its entries in `munger.md` before going on.
3. `bash run.sh` (or `.\run.ps1`). Every remaining block runs in a fresh
   session, Sonnet at high effort; blocks already covered are skipped; it
   stops by itself when the fourth book is done.
