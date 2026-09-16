# firm-to-nds — Claude Guide

Single-script Python tool that converts a `.firm` firmware file to `.nds` by prepending the
required header, for use on DSPico and compatible Nintendo DS/DSi/3DS-dev flashcards.

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
- **Hard limits.** The verdict awaits your close; the agent never merges.

## Working rules

- **The header `.bin` files must ship with the script** — the tool reads them from its own
  directory.
- **Don't alter the header bytes** — they're the fixed prefix the flashcard expects.
- Keep it dependency-free and single-file; it's meant to be copy-and-run.

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
