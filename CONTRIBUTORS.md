# 🤝 Contributing to moltshit_tools

Thank you for contributing to moltshit_tools.

This document is intentionally minimal. For all CLI usage, flags, and tool behavior, see the README.md.

---

## 📌 Contribution Philosophy

This project prefers:
- Small, isolated pull requests
- Minimal behavioral changes
- Backward-compatible updates
- CLI-first improvements

---

## 🤖 Agent / AI Contributions

This repository supports AI-generated pull requests.

If you are an agent:
- Keep changes scoped to a single tool file
- Do not refactor across multiple scripts
- Do not change existing CLI behavior unless fixing a bug
- Prefer additive improvements (new flags, better error handling, robustness fixes)

---

## 🧭 Scope Rules

Avoid:
- large architectural changes
- cross-tool coupling
- dependency additions without strong justification

---

## 🧪 Testing

All functionality is CLI-driven.

For usage examples and validation commands, refer to README.md.

PRs should include:
- at least one CLI test command used for validation
- notes on edge cases if applicable

---

## 🧾 Pull Request Format

Title:
[tool-name] short description

Body:
- What changed
- Why it changed
- How it was tested (CLI commands)
- Any edge cases

---

## 🚫 Non-goals

This file does NOT redefine tool usage or CLI flags.
All functional documentation lives in README.md.

---

## ❤️ Summary

Small, focused improvements are preferred over large changes.
