# firm-to-nds — Agent Guide

Single-script Python tool that converts a `.firm` firmware file to `.nds` by prepending the
required header, for use on DSPico and compatible Nintendo DS/DSi/3DS-dev flashcards.

## Agent compatibility — Codex and Claude Code

This file is `AGENTS.md`: the **one** instruction file for every coding agent in this repo. Codex
reads it directly; Claude Code reads `CLAUDE.md`, which only imports this file (`@AGENTS.md`) and
holds what applies to Claude alone. **Edit rules here, never in `CLAUDE.md`** — two copies of a
rule drift apart on the first edit, and each agent then obeys a different one.

| Concern | Claude Code | Codex |
| --- | --- | --- |
| Instruction file | `CLAUDE.md` → imports `AGENTS.md` | `AGENTS.md` (root down to the working directory) |
| Invoke a skill | `Skill` tool, or `/<skill>` | mention it (`$<skill>`), or let it trigger from its description |
| Skills on disk | `~/.claude/skills` (links into `~/.agents/skills`) | `.agents/skills`, then `~/.agents/skills` |
| superpowers | `superpowers@claude-plugins-official` (`/plugin install`) | `superpowers@openai-curated` (install from `/plugins`; that id is its key in `~/.codex/config.toml`) |
| MCP servers | `claude mcp add -s user <name> -- <cmd>` | `codex mcp add <name> -- <cmd>` (`~/.codex/config.toml`) |
| File size | imports load whole | `project_doc_max_bytes`, **32 KiB by default** — raise it when this file is bigger, or the tail is silently dropped |

- **Install shared skills once, for both agents:** `npx skills add <owner/repo> -g --skill <name>`
  writes to `~/.agents/skills` and links it for Claude Code, so both run the same version.
- **Names in this file are capabilities, not one agent's syntax.** "Invoke the `X` skill" means the
  `Skill` tool in Claude Code and a skill mention in Codex. An MCP server named here is used when it
  is registered for the agent you are running in; its absence never blocks ordinary work.
- **Modes, model caps and Git rules bind both agents.** "lite mode", "normal mode" and "modo
  desatendido" mean the same in Codex; a cap written as "no model above Sonnet" means "no model
  above the mid tier" there.
- **Claude-only commands** (slash commands that are not skills) are skipped by Codex unless the
  same capability is installed as a skill in `~/.agents/skills`.

## Superpowers — use whenever applicable

Always prefer **superpowers** skills over ad-hoc approaches. If there's even a small chance a
skill applies, invoke it via the `Skill` tool before acting (including before clarifying
questions).

- **Process skills first** — `brainstorming` before creative/feature work, `systematic-debugging`
  before fixing bugs, `test-driven-development` before writing implementation.
- **Then implementation skills** — domain-specific skills guide execution.
- **Verify before claiming done** — `verification-before-completion` / `requesting-code-review`.

User instructions always take precedence over skills; skills override default behavior.

### Mode switch

- **"lite mode"** — fully disables superpowers: no skill is invoked, not even the applicability
  check, until **"normal mode"** is said.
- **"normal mode"** (default) — standard superpowers behavior, plus: when delegating coding work,
  dispatch at most 1 agent at a time, and never use a model above Sonnet (no Opus).
- **"modo desatendido"** (unattended mode) — the user is away and delegates autonomy: work
  without waiting for confirmations and decide yourself instead of asking. You MAY **`git push`
  the feature branches you create** and **open PRs via `gh`**. The hard limits still hold:
  **never merge anything** (no `git merge`, no fast-forward, no `gh pr merge`), **never push to
  `main`**/protected, never `--force`. Deliver branches + PRs for the user to merge. Reverts to
  defaults on **"normal mode"**.

Confirm the switch briefly when it happens.

## Stack

- **Python 3.6+**, standard library only. No dependencies, no build, no tests.

## Layout

- `firm_to_nds.py` — the whole tool.
- `header.bin` — header prepended by default; must sit beside the script.
- `header_dev.bin` — used with `--dev` (3DS dev consoles).

## Commands

```bash
python firm_to_nds.py [--dev] <input.firm> [output.nds]
# --dev  → use header_dev.bin instead of header.bin
```

## Agentic PR verification (MANDATORY on every PR)

**Every PR MUST be verified end-to-end before merge, and the verdict MUST be posted as a PR
comment** via `gh pr comment`. A headless agent (`claude -p`, local) drives the change and posts
the result; it **never merges** — it waits for you. Running the pass and posting the verdict
comment is **not optional**. It catches what a diff and a syntax check miss: a broken `--dev`
flag, a wrong output path, a corrupted header/firm concatenation.

- **Engine.** No browser, no server — this is a one-shot CLI. Verification means: run
  `firm_to_nds.py` end-to-end against a **throwaway sample input**, e.g.
  `dd if=/dev/urandom of=/tmp/sample.firm bs=1024 count=4` (or any small non-real dummy file),
  then `python firm_to_nds.py /tmp/sample.firm /tmp/sample.nds` and confirm the output exists,
  its size equals `header.bin` + input size, and its first bytes match `header.bin`; repeat with
  `--dev` against `header_dev.bin`. Also check `-h`/no-args prints help and exits non-zero.
  Never point it at real firmware dumps.
- **Two layers.** Deterministic checks (`python -m py_compile`) stay the hard merge gate; the
  agentic pass is advisory and never vetoes a merge on its own — but running it and posting the
  verdict comment is mandatory.
- **The verdict reads structure too.** Besides driving the conversion, it names what the diff does
  to the [Design principles](#design-principles--solid-applied-with-judgement): e.g. `convert()`
  growing another `if header_variant == ...` branch, or a speculative abstraction (a class, a
  plugin registry) added for a second header format that doesn't exist yet. Findings, not a veto —
  like the rest of the pass.
- **Hard limits.** The verdict awaits your close; the agent never merges.

## Design principles — SOLID, applied with judgement

SOLID is a list of **symptoms to look for**, not a pattern to apply. Every one of the five exists to
keep a change local: the useful question is *how many files does the next plausible change touch,
and how many of them do you have to understand first?* Applied by rote it produces the opposite —
an interface per class, a factory for one product — so here it is bounded by YAGNI: this is a
70-line script, and most of the table below is a checklist for *noticing drift* if the tool grows,
not a mandate to add seams today.

| Principle | Checkable smell | Usual fix |
| --- | --- | --- |
| **S — Single responsibility**: one reason to change | the description needs "and"; the file changes in PRs about unrelated features; a test mocks things unrelated to what it asserts | split along the reason to change — IO, decision, presentation |
| **O — Open/closed**: extend without editing | adding a case edits a growing `switch`/`if` chain in several places; one boolean flag per variant | a variants map, strategy, slot or registry — introduced at the second real case, not the first |
| **L — Liskov substitution**: subtypes keep the contract | an override throws "not supported"; callers check the concrete type before calling | narrow the base contract, or stop inheriting and compose |
| **I — Interface segregation**: clients see only what they use | a fake implements methods the test never calls; a whole object is passed to read two fields | split by client need; pass the fields, not the bag |
| **D — Dependency inversion**: policy does not import mechanism | domain logic imports `fetch`, an ORM, `Date.now()` or `fs` directly; a unit test needs a network or a database | depend on a port the caller owns (interface, function); wire the adapter at the edge |

### Where the seams go, in this repo

| Stack | Seams |
| --- | --- |
| Python | pure functions for decisions; IO at the edges (CLI entry point, adapters); a `Protocol` only when a second implementation or a test fake needs it |

`convert()` already follows this: it takes plain paths, does its own IO, and has no branching logic
worth extracting yet. `main()` is the edge — argument parsing (IO-adjacent) is kept out of
`convert()`.

### Where SOLID stops

- **No interface, abstract class or factory without one of:** a second real implementation, an IO
  boundary (network, database, filesystem, clock, randomness, OS), or a test that cannot be written
  without the seam. "We might swap it later" is not on the list — e.g. a second header *format*
  (not just a second `.bin` file, which `--dev` already handles) would justify one; today it
  wouldn't.
- **Reuse first beats speculative extension points:** add the parameter to the existing thing
  before inventing a plugin system for it.
- **Speculative abstraction is a review finding**, exactly like a violation: an interface with one
  implementation and no IO behind it gets inlined.
- **Refactor toward SOLID when a change hurts**, in the PR that felt the pain — not as a drive-by
  rewrite of code nobody is changing.

## Working rules

- **The header `.bin` files must ship with the script** — the tool reads them from its own
  directory.
- **Don't alter the header bytes** — they're the fixed prefix the flashcard expects.
- Keep it dependency-free and single-file; it's meant to be copy-and-run.
- **SOLID where it pays, not by rote** — split by reason to change, extend through variants or
  strategies instead of editing branches, and push IO behind ports at the edge. No abstraction
  without a second implementation, an IO boundary or a test seam. See
  [Design principles](#design-principles--solid-applied-with-judgement).

## Git & GitHub

- **Commits and branches OK** — create commits and new branches whenever it makes sense, without
  asking first.
- **Never push** (default) — no `git push` under any circumstance, and never `git push --force` /
  `--force-with-lease`. Leave pushing to the user. **Exception:** with **"modo desatendido"**
  active, you may push the feature branches you create (never `main`/protected, never force).
- **Never merge — no permission** — no `git merge`, no fast-forward integration, no `gh pr merge`,
  and no merging of any pull request, in every mode incl. **"modo desatendido"**. Leave every
  merge to the user.
- **GitHub via `gh`** — open PRs, issues, comments, and labels over branches already pushed.

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:

- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- For cross-module "how does X relate to Y" questions, prefer `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"` over grep — these traverse the graph's EXTRACTED + INFERRED edges instead of scanning files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)
