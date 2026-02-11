# [Feature Name] Implementation Plan

## Overview

[Brief description of what we're implementing and why]

## Current State Analysis

[What exists now, what's missing, key constraints discovered]

### Key Discoveries:
- [Important finding with file:line reference]
- [Pattern to follow]
- [Constraint to work within]

## Desired End State

[A Specification of the desired end state after this plan is complete, and how to verify it]

## What We're NOT Doing

[Explicitly list out-of-scope items to prevent scope creep]

- Not implementing X
- Not changing Y
- Out of scope: Z

## Implementation Approach

[High-level strategy and reasoning]

---

## Phase 1: [Descriptive Name]

### Overview
[What this phase accomplishes]

### Changes Required:

#### 1. [Component/File Group]
**File**: `path/to/file.ext`
**Changes**: [Summary of changes]

```language
// Specific code to add/modify
```

### Success Criteria:

#### Automated Verification:
- [ ] Tests pass: `npm test` / `make test`
- [ ] Type checking passes: `npm run typecheck`
- [ ] Linting passes: `npm run lint`
- [ ] Build succeeds: `npm run build`

#### Manual Verification:
- [ ] Feature works as expected in UI
- [ ] Performance is acceptable
- [ ] No regressions in related features

**Implementation Note**: After completing this phase and all automated verification passes, pause for manual confirmation before proceeding.

---

## Phase 2: [Descriptive Name]

### Overview
[What this phase accomplishes]

### Changes Required:

#### 1. [Component/File Group]
**File**: `path/to/file.ext`
**Changes**: [Summary of changes]

### Success Criteria:

#### Automated Verification:
- [ ] [Test command]
- [ ] [Lint command]

#### Manual Verification:
- [ ] [Human verification step]

---

## Testing Strategy

### Unit Tests:
- [What to test]
- [Key edge cases]

### Integration Tests:
- [End-to-end scenarios]

### Manual Testing Steps:
1. [Specific step to verify feature]
2. [Another verification step]
3. [Edge case to test manually]

## Performance Considerations

[Any performance implications or optimizations needed]

## Migration Notes

[If applicable, how to handle existing data/systems]

## References

- Original ticket: [link or path]
- Related research: [path to research doc]
- Similar implementation: [file:line reference]
