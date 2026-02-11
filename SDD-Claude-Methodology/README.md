# SDD - Spec Driven Development for Claude Code

> **A comprehensive methodology for building high-quality software with AI agents by managing context windows effectively**

This folder contains the complete SDD (Spec Driven Development) methodology, combining the **Folloni Method** (3-phase approach) with the **HumanLayer Method** (advanced agent orchestration).

---

## Table of Contents

1. [The Core Problem](#the-core-problem)
2. [The Solution: SDD Methodology](#the-solution-sdd-methodology)
3. [Quick Start](#quick-start)
4. [Method 1: Folloni (Simple 3-Phase)](#method-1-folloni-simple-3-phase)
5. [Method 2: HumanLayer (Advanced)](#method-2-humanlayer-advanced)
6. [Folder Structure](#folder-structure)
7. [How to Use in Client Projects](#how-to-use-in-client-projects)
8. [Agent Types Reference](#agent-types-reference)
9. [Command Reference](#command-reference)

---

## The Core Problem

AI coding assistants like Claude have a **context window** (memory) that fills up during long sessions. When this happens:

- The AI starts "hallucinating" or making errors
- Code quality degrades
- The AI forgets earlier parts of the conversation
- Solutions become inconsistent

**The SDD methodology solves this by treating the process like a funnel:**

```
Research (filter useful info) → Planning (create detailed spec) → Implementation (execute spec)
```

Each phase produces a document, and you **clear the context between phases**. The next agent only reads that document, not the entire history.

---

## The Solution: SDD Methodology

### Key Principles

1. **Divide and Conquer**: Split work into Research → Planning → Implementation
2. **Memory Management**: Clear context between phases
3. **Documentation as Communication**: Each phase produces a document for the next
4. **Parallel Research**: Use sub-agents for concurrent investigation
5. **One-Shot Implementation**: With a clear spec, code right the first time

### The Workflow

```
┌─────────────────┐
│   Your Idea     │
└────────┬────────┘
         ▼
┌─────────────────┐
│   RESEARCHER    │ ──→ prd.md (or research doc)
└────────┬────────┘
         │ CLEAR CONTEXT
         ▼
┌─────────────────┐
│   ARCHITECT     │ ──→ spec.md (or plan doc)
└────────┬────────┘
         │ CLEAR CONTEXT
         ▼
┌─────────────────┐
│   DEVELOPER     │ ──→ Working Code
└─────────────────┘
```

---

## Quick Start

### For Simple Projects (Folloni Method)

1. Copy `folloni-sdd-method.md` to your project
2. Follow the 3-phase prompts
3. Use `/clear` between phases

### For Complex Projects (HumanLayer Method)

1. Copy the `.claude` folder structure to your project:
   ```
   your-project/
   └── .claude/
       ├── agents/           # Sub-agent definitions
       ├── commands/         # Slash commands
       └── settings.json     # Configuration
   ```
2. Use slash commands: `/research_codebase`, `/create_plan`, `/implement_plan`

---

## Method 1: Folloni (Simple 3-Phase)

**Best for**: Small to medium projects, quick implementations, solo developers

### Phase 1: The Researcher (Generate PRD)

**Goal**: Survey the codebase and internet, filter useful from useless.

```markdown
Act as a Senior Software Engineer focused on technical planning. I need to implement: [YOUR FEATURE DESCRIPTION].

Your task is to do deep research before we write any code. Follow these steps:

1. Internal Impact Analysis: Search our codebase to identify which files will be affected. List only relevant ones.

2. Pattern Search (DRY): Check for existing similar patterns (UI components, auth flows, DB connections) we can reuse.

3. External Context: If using external libraries (Stripe, NextAuth, etc.), read the latest official documentation.

4. Output: Create a file called prd.md with:
   • Objective Summary
   • Relevant Files list
   • Documentation excerpts
   • Code Snippets (internal or external)
   • Filter out useless information
```

**After Phase 1**: Run `/clear` or restart the session.

### Phase 2: The Architect (Generate Spec)

**Goal**: Create a tactical battle plan with zero ambiguity.

```markdown
Read the prd.md file from the previous phase. It contains all context about the feature.

Based on that document, create a detailed tactical implementation plan. Generate a file called spec.md.

The spec.md must explicitly contain:

1. Files to Create: Exact list with full paths
2. Files to Modify: Exact list of existing files to change
3. Detailed Instructions per File:
   • Which functions to create?
   • Which imports to add?
   • Which logic to change?
4. Pseudocode and Snippets from the PRD

Golden Rules:
• Avoid overengineering - choose the simplest solution
• Be tactical - leave no room for interpretation
• Modularization - don't mix responsibilities
```

**After Phase 2**: Run `/clear` or restart the session.

### Phase 3: The Developer (Implementation)

**Goal**: Write high-quality code in one shot.

```markdown
Read the spec.md file. This is your definitive implementation plan.

Since your context window is clean and focused only on this plan, use your maximum capacity to write high-quality code:

1. Rigorous Execution: Implement exactly what's described. Create and modify only listed files.

2. Consistency: Use the patterns and snippets from the plan. Don't get creative if the plan already defines how.

3. Simplicity: Don't add unnecessary complexity. Write clean, modular, maintainable code.

4. One Shot: Your goal is working code on the first try.

Begin coding.
```

---

## Method 2: HumanLayer (Advanced)

**Best for**: Large codebases, teams, complex features, production systems

### Core Commands

| Command | Description |
|---------|-------------|
| `/research_codebase` | Document existing code without judgment |
| `/create_plan` | Create detailed implementation plan |
| `/implement_plan` | Execute the plan phase by phase |
| `/validate_plan` | Verify implementation matches plan |
| `/commit` | Create git commits |
| `/describe_pr` | Generate PR descriptions |

### Specialized Agents

Located in `agents/` folder:

| Agent | Purpose |
|-------|---------|
| `codebase-locator` | Find WHERE files and components live |
| `codebase-analyzer` | Understand HOW code works |
| `codebase-pattern-finder` | Find similar implementations to model after |
| `thoughts-locator` | Discover existing documentation |
| `thoughts-analyzer` | Extract insights from documents |
| `web-search-researcher` | Research external documentation |

### Key Principles

1. **Agents are Documentarians, Not Critics**: They describe what exists, never suggest improvements
2. **Parallel Research**: Spawn multiple agents to research concurrently
3. **Read Files FULLY**: Never use partial reads
4. **Separate Success Criteria**: Automated (testable) vs Manual (human verification)
5. **No Open Questions**: Plans must be complete before implementation

### Example Workflow

```bash
# Step 1: Research the codebase
User: /research_codebase
User: How does the authentication system work?
# Agent produces: thoughts/shared/research/2025-01-17-authentication-flow.md

# CLEAR CONTEXT

# Step 2: Create implementation plan
User: /create_plan
User: Add OAuth2 support to the auth system
# Agent produces: thoughts/shared/plans/2025-01-17-oauth2-implementation.md

# CLEAR CONTEXT

# Step 3: Implement
User: /implement_plan thoughts/shared/plans/2025-01-17-oauth2-implementation.md
# Agent implements phase by phase
```

---

## Folder Structure

```
SDD-Claude-Methodology/
├── README.md                        # This file
├── folloni-sdd-method.md           # Simple 3-phase method (Portuguese)
├── settings.json                    # Claude settings
├── agents/                          # Sub-agent definitions
│   ├── codebase-analyzer.md
│   ├── codebase-locator.md
│   ├── codebase-pattern-finder.md
│   ├── thoughts-analyzer.md
│   ├── thoughts-locator.md
│   └── web-search-researcher.md
├── commands/                        # Slash command definitions
│   ├── create_plan.md              # Planning command
│   ├── research_codebase.md        # Research command
│   ├── implement_plan.md           # Implementation command
│   ├── validate_plan.md            # Validation command
│   ├── commit.md                   # Git commit helper
│   ├── describe_pr.md              # PR description generator
│   └── ... (27 total commands)
└── templates/                       # Document templates
```

---

## How to Use in Client Projects

### Option 1: Copy the .claude folder

```bash
# Copy to your client project
cp -r SDD-Claude-Methodology/agents your-project/.claude/agents
cp -r SDD-Claude-Methodology/commands your-project/.claude/commands
cp SDD-Claude-Methodology/settings.json your-project/.claude/
```

### Option 2: Create a thoughts/ directory structure

```bash
mkdir -p your-project/thoughts/shared/{plans,research,handoffs}
mkdir -p your-project/thoughts/local
```

### Option 3: Minimal Setup (Folloni Method Only)

Just copy `folloni-sdd-method.md` and follow the prompts manually.

### Adapting for Different Projects

1. **Modify agent paths**: Update directory references in agent files
2. **Adjust commands**: Remove HumanLayer-specific commands (linear.md, etc.)
3. **Customize templates**: Adapt plan templates to project needs

---

## Agent Types Reference

### codebase-locator
```
Purpose: Find files and components by keyword
Tools: Grep, Glob, LS
Use when: You need to find WHERE something is
```

### codebase-analyzer
```
Purpose: Understand HOW code works
Tools: Read, Grep, Glob, LS
Use when: You need detailed implementation analysis
```

### codebase-pattern-finder
```
Purpose: Find similar implementations
Tools: Grep, Glob, Read, LS
Use when: You want examples to model after
```

### thoughts-analyzer
```
Purpose: Extract insights from documentation
Tools: Read, Grep, Glob, LS
Use when: You need to understand historical decisions
```

### thoughts-locator
```
Purpose: Find existing documentation
Tools: Grep, Glob, LS
Use when: You need to discover what docs exist
```

### web-search-researcher
```
Purpose: Research external documentation
Tools: WebSearch, WebFetch, TodoWrite, Read
Use when: You need current web information
```

---

## Command Reference

### Core Planning Commands

| Command | Description |
|---------|-------------|
| `create_plan.md` | Create detailed implementation plans |
| `create_plan_generic.md` | Generic version without HumanLayer specifics |
| `create_plan_nt.md` | No-thoughts version (no thoughts/ directory) |
| `iterate_plan.md` | Update existing plans based on feedback |
| `validate_plan.md` | Verify implementation correctness |

### Research Commands

| Command | Description |
|---------|-------------|
| `research_codebase.md` | Comprehensive codebase documentation |
| `research_codebase_generic.md` | Generic version |
| `research_codebase_nt.md` | No-thoughts version |

### Implementation Commands

| Command | Description |
|---------|-------------|
| `implement_plan.md` | Execute plans phase by phase |
| `debug.md` | Investigate issues during testing |

### Git/PR Commands

| Command | Description |
|---------|-------------|
| `commit.md` | Create git commits without Claude attribution |
| `describe_pr.md` | Generate comprehensive PR descriptions |
| `local_review.md` | Set up local review environment |

### Session Management

| Command | Description |
|---------|-------------|
| `create_handoff.md` | Create handoff documents for context transfer |
| `resume_handoff.md` | Resume work from handoff documents |
| `oneshot.md` | Quick research and planning |

---

## Best Practices

### 1. Always Clear Context Between Phases
```
Phase 1 → /clear → Phase 2 → /clear → Phase 3
```

### 2. Read Files FULLY
Never use `limit` or `offset` parameters. Complete context is essential.

### 3. Spawn Parallel Research
```markdown
# Good: Multiple agents in parallel
- codebase-locator: Find auth files
- codebase-analyzer: Analyze auth flow
- thoughts-locator: Find auth documentation

# Bad: Sequential research
- First find files, then analyze...
```

### 4. Separate Success Criteria
```markdown
### Automated Verification:
- [ ] Tests pass: `npm test`
- [ ] Lint passes: `npm run lint`

### Manual Verification:
- [ ] UI works correctly
- [ ] Performance acceptable
```

### 5. No Open Questions in Plans
If you have questions, research them BEFORE writing the plan. Plans must be actionable without clarification.

---

## Credits

- **Folloni Method**: Spec Driven Development approach (Portuguese community)
- **HumanLayer Method**: [HumanLayer](https://github.com/humanlayer/humanlayer) - Human-in-the-loop for AI agents
- **Compiled by**: Matteus Eugenio for DevOps N8N Printer project

---

## License

This methodology documentation is compiled from open-source projects:
- HumanLayer: Apache 2.0 License
- Folloni Method: Community shared

Use freely in your projects.
