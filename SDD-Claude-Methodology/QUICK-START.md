# Quick Start Guide - SDD Methodology

## Option 1: Full Setup (Recommended)

Copy this entire folder structure to your project:

```bash
# From your client project root
cp -r /path/to/SDD-Claude-Methodology/.claude ./

# Or create the structure manually:
mkdir -p .claude/agents .claude/commands
cp /path/to/SDD-Claude-Methodology/agents/* .claude/agents/
cp /path/to/SDD-Claude-Methodology/commands/* .claude/commands/
cp /path/to/SDD-Claude-Methodology/settings.json .claude/
```

## Option 2: Minimal Setup (Folloni Method Only)

Just use these 3 prompts in sequence, clearing context between each:

### Prompt 1: Research Phase
```
Act as a Senior Software Engineer focused on technical planning. I need to implement: [DESCRIBE YOUR FEATURE].

Do deep research before we write any code:
1. Search our codebase for affected files
2. Find existing patterns we can reuse
3. Read documentation for any external libraries needed

Output a prd.md file with:
- Objective Summary
- Relevant Files list
- Documentation excerpts
- Code Snippets to follow
```

**→ After this: `/clear` or start new session**

### Prompt 2: Planning Phase
```
Read prd.md and create a detailed spec.md with:
1. Files to Create (exact paths)
2. Files to Modify (exact list)
3. Instructions per file (functions, imports, logic)
4. Code snippets from PRD

Be tactical - leave no room for interpretation.
```

**→ After this: `/clear` or start new session**

### Prompt 3: Implementation Phase
```
Read spec.md and implement exactly what's described.
- Follow the patterns in the spec
- Don't add unnecessary complexity
- Goal: working code on first try

Begin coding.
```

## Option 3: Generic Commands (No HumanLayer Dependencies)

Use these command files which have no external dependencies:

- `commands/create_plan_generic.md` - Planning without thoughts/ directory
- `commands/research_codebase_generic.md` - Research without thoughts/
- `commands/create_plan_nt.md` - No-thoughts version

## Directory Structure for Advanced Usage

Create this structure in your project for full functionality:

```
your-project/
├── .claude/
│   ├── agents/          # Copy from SDD-Claude-Methodology/agents/
│   ├── commands/        # Copy from SDD-Claude-Methodology/commands/
│   └── settings.json    # Copy from SDD-Claude-Methodology/
└── thoughts/
    ├── shared/
    │   ├── plans/       # Implementation plans go here
    │   ├── research/    # Research documents go here
    │   └── handoffs/    # Context handoff documents
    └── local/           # Personal notes (not shared)
```

## Key Commands Reference

| Command | What It Does |
|---------|--------------|
| `/research_codebase` | Document how existing code works |
| `/create_plan` | Create implementation plan |
| `/implement_plan [path]` | Execute a plan phase by phase |
| `/validate_plan` | Verify implementation is correct |
| `/commit` | Create git commits |

## Essential Tips

1. **Always clear context between phases** - This is the key to the methodology
2. **Read files FULLY** - Never use partial reads
3. **Spawn parallel research** - Use multiple agents for concurrent investigation
4. **Separate success criteria** - Automated (testable) vs Manual (human verification)
5. **No open questions in plans** - Research everything before finalizing

## Example Session

```bash
# Session 1: Research
User: /research_codebase
User: How does user authentication work?
Claude: [Produces research document]
# END SESSION

# Session 2: Plan
User: /create_plan
User: Add 2FA to authentication. Reference: thoughts/shared/research/auth-flow.md
Claude: [Produces implementation plan]
# END SESSION

# Session 3: Implement
User: /implement_plan thoughts/shared/plans/2025-01-17-add-2fa.md
Claude: [Implements phase by phase]
```

## Troubleshooting

### "Command not found"
Make sure `.claude/commands/` folder exists and contains the .md files.

### "Agent not found"
Make sure `.claude/agents/` folder exists and contains the agent definitions.

### Context getting too long
You're probably not clearing between phases. Use `/clear` or start a new session.

### Implementation has errors
Your spec wasn't detailed enough. Go back to planning phase with more research.
