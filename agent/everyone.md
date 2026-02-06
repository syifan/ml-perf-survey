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

- **Messages for you** — check `messages/{your_name}.md` for guidance
- **Open issues and their comments**
- **Open PRs**

---

## 3. GitHub Conventions

**All GitHub activity must be prefixed with your agent name in brackets.**

| Type | Format |
|------|--------|
| Issue title | `[AgentName] Description` |
| PR title | `[AgentName] Description` |
| Comments | `# [AgentName]` header |
| Commits | `[AgentName] Message` |
| Branch names | `agentname/description` |

---

## 4. Active Label

- **Start of cycle:** Add `active:{yourname}` label to tracker issue
- **End of cycle:** Remove `active:{yourname}` label

---

## 5. End of Cycle

Comment on tracker:
```
# [AgentName]

**Input:** (what you saw)

**Actions:** (what you did)
```

---

## 6. Tips

- **Complete all assigned tasks** in a single cycle.
- **Be concise** — get things done.
- **Pull before working.**
- **See something, say something** — if you find a problem, raise an issue.
