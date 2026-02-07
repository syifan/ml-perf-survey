# Everyone — Shared Rules for All Agents

Read this file before executing any task.

---

## Core Goal

**Complete the project with passing standard quality, with minimum human involvement.** Work autonomously. Make decisions. Solve problems. Only escalate when absolutely necessary.

---

## 1. Safety Rules

**Before ANY action**, verify you are in the correct repository.

**If repo doesn't match, ABORT immediately.**

When in doubt, **STOP and report the discrepancy**.

---

## 2. Context to Read

Before starting work, gather context from:

- **Your workspace** — read all files in `agent/workspace/{your_name}/` (includes evaluations from Apollo)
- **Open issues and their comments**
- **Open PRs**

---

## 3. Your Workspace

Each agent has a personal workspace at `agent/workspace/{your_name}/`.

**At the end of each cycle**, write a brief `note.md` with:
- Context for your future self
- Lessons learned
- How to do better next time

**Rules:**
- Keep it short (a few bullet points)
- Replace previous note each cycle (don't accumulate)
- **Always commit workspace changes to main branch** (not feature branches)
- This is for YOU — help yourself be more effective

---

## 4. GitHub Conventions

**All GitHub activity must be prefixed with your agent name in brackets.**

| Type | Format |
|------|--------|
| Issue title | `[AgentName] Description` |
| PR title | `[AgentName] Description` |
| Comments | `# [AgentName]` header |
| Commits | `[AgentName] Message` |
| Branch names | `agentname/description` |

---

## 5. Active Label

- **Start of cycle:** Add `active:{yourname}` label to tracker issue
- **End of cycle:** Remove `active:{yourname}` label

---

## 6. End of Cycle

Comment on tracker:
```
# [AgentName]

**Input:** (what you saw)

**Actions:** (what you did)
```

---

## 7. Tips

- **Complete all assigned tasks** in a single cycle.
- **Be concise** — get things done.
- **Pull before working.**
- **See something, say something** — if you find a problem, raise an issue.
