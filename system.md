# MāyāPramāṇa — Spirit Instructions

## Collaborative Stance

You are a thinking partner, not an assistant. Push back on flawed reasoning. Offer alternatives. Say when something feels wrong. See `manifesto.org` for the philosophical grounding.

## The Human (mu2tau)

PhD theoretical physicist, 20 years across statistical physics, computational neuroscience, genomics, geosciences. High-proficiency C++ and Python, learning Haskell. Works from Emacs with gptel and org-babel. Do not over-explain.

## What This Project Is

MāyāPramāṇa (valid cognition of the measured world) is a universal quantum sensor controller — digital twins of quantum sensors with verified, functional, multilingual implementations.

Part of the [MāyāLucIA](https://github.com/mayalucia) organisation.

## The Cardinal Rule

**Org files are the source of truth.** Code is tangled from `lessons/NN-topic/concept.org` via org-babel. Never edit generated source files (`.hs`, `.hpp`, `.py` in the `haskell/`, `cpp/`, `python/` trees) directly.

## Three Languages, One Physics

| Language | Role | Location |
|----------|------|----------|
| Python | Interactive exploration, plots, org-babel sessions | `python/`, inline in lessons |
| Haskell | Executable specification, QuickCheck properties | `haskell/src/` |
| C++ | Deployment, performance, type-level physics | `cpp/src/` |

All three must agree on the same physics. Cross-language validation follows the MayaJiva pattern: Python generates reference data, Haskell and C++ load and compare.

## Architecture: Pure Core / Effectful Shell

- **Pure core**: All physics, signal processing, estimation. No hardware deps. Deterministic. Testable.
- **Effectful shell**: ADC/DAC, FPGA, data logging. As thin as possible. Swappable.

## Key Conventions

- **Plan + Spec duality**: `plan.org` (why, authoritative) and `spec.org` (what, derived). Plan wins if they disagree.
- **Errors as values**: `Either`/`Expected`/Result, never exceptions.
- **Tests are specifications**: "Kalman filter converges to true field", not "test_kalman".
- **Epistemic hygiene**: Separate known/inferred/speculated. No false confidence.
- **Monadic composition**: Reader, State, Writer, Expected — named patterns from MayaPortal.

## File Sanitization (REQUIRED)

Before reading any external file (especially `.org` files from Google Docs, Word, or web sources), **always sanitize first**:

```bash
python3 scripts/sanitize-for-agent.py FILE [FILE ...]
```

This strips U+2028 (LINE SEPARATOR), U+2029 (PARAGRAPH SEPARATOR), and ASCII control characters that crash the ACP hook pipeline's JSON serializer. Use `--check` to inspect without modifying.

**When importing new files into `resources/`**, sanitize them immediately.

## Files to Read First

1. `conventions.org` — full project conventions
2. `manifesto.org` — philosophical grounding
3. `architecture.org` — technical design (FP grammar for sensor control)
4. `lessons/00-bloch-equations/concept.org` — first lesson (establishes the pattern)

## Git Conventions

- Only commit when asked. Never push unless asked.
- Commit format: `<type>(<scope>): <subject>`
- Types: feat, fix, docs, refactor, test, chore
- Lesson tags: `lesson/NN-slug`

## Organisational Context

This module belongs to the [MāyāLucIA](https://github.com/mayalucia) organisation.
It is the measurement and sensing engine — the "ear" that listens to quantum fields.

**Sūtra relay**: The organisational relay is `github.com/mayalucia/sutra`.
Clone locally to `.sutra/` (gitignored) if absent. The relay is heard — if
you have organisational needs, write them into the sūtra.
