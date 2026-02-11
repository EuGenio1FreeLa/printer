# SPEC: [Feature Name]

> Tactical Implementation Specification

**Based on**: `prd.md` from Research phase
**Date**: [YYYY-MM-DD]
**Status**: Ready for Implementation

---

## Files to Create

| File Path | Purpose |
|-----------|---------|
| `src/components/NewFeature.tsx` | Main component |
| `src/hooks/useNewFeature.ts` | Custom hook |
| `src/types/newFeature.ts` | Type definitions |

## Files to Modify

| File Path | What to Change |
|-----------|----------------|
| `src/App.tsx` | Add route for new feature |
| `src/api/index.ts` | Add new API method |

---

## Detailed Instructions

### 1. Create `src/types/newFeature.ts`

**Purpose**: Define TypeScript interfaces

**Contents**:
```typescript
export interface NewFeatureConfig {
  // Define properties
}

export interface NewFeatureState {
  // Define state shape
}
```

### 2. Create `src/hooks/useNewFeature.ts`

**Purpose**: Encapsulate feature logic

**Imports to add**:
```typescript
import { useState, useEffect } from 'react';
import type { NewFeatureConfig, NewFeatureState } from '../types/newFeature';
```

**Functions to create**:

```typescript
export function useNewFeature(config: NewFeatureConfig): NewFeatureState {
  // Implementation following pattern from prd.md
}
```

### 3. Create `src/components/NewFeature.tsx`

**Purpose**: UI component

**Follow pattern from**: `src/components/SimilarFeature.tsx:15-45`

**Structure**:
```typescript
import { useNewFeature } from '../hooks/useNewFeature';

export function NewFeature({ ...props }) {
  const state = useNewFeature(config);

  return (
    // JSX following existing component patterns
  );
}
```

### 4. Modify `src/App.tsx`

**Lines to change**: Around line 25-30

**Add import**:
```typescript
import { NewFeature } from './components/NewFeature';
```

**Add route** (after existing routes):
```typescript
<Route path="/new-feature" element={<NewFeature />} />
```

### 5. Modify `src/api/index.ts`

**Add function** (after line 50):
```typescript
export async function fetchNewFeatureData(): Promise<NewFeatureData> {
  // Implementation
}
```

---

## Implementation Order

1. Types first (no dependencies)
2. Hook (depends on types)
3. Component (depends on hook)
4. Route modification (depends on component)
5. API method (independent, can be parallel)

## Testing Requirements

### Unit Tests to Create

- [ ] `__tests__/hooks/useNewFeature.test.ts`
- [ ] `__tests__/components/NewFeature.test.tsx`

### Test Scenarios

1. Happy path: [Description]
2. Error state: [Description]
3. Edge case: [Description]

## Success Criteria

### Automated
- [ ] All tests pass: `npm test`
- [ ] TypeScript compiles: `npm run typecheck`
- [ ] Linting passes: `npm run lint`
- [ ] Build succeeds: `npm run build`

### Manual
- [ ] Feature renders correctly
- [ ] Interactions work as expected
- [ ] No console errors

---

*This SPEC was created during the Planning phase of SDD methodology.*
*Next step: Clear context and implement following this specification.*
