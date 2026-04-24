---
title: 'Fix ESLint React Fast Refresh Warnings in UI Components'
type: 'refactor'
created: '2026-04-24'
status: 'in-progress'
baseline_commit: '42103a2c3438ecd2b50a240e6219545d314661e3'
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Seven UI component files export both React components and non-component values (variant functions, type definitions), which breaks React Fast Refresh during development. When these files change, the entire module reloads instead of hot-reloading just the component, slowing down the development experience.

**Approach:** Extract non-component exports (variant functions created with `cva`, type definitions, and utility functions) into separate files, then import them back into the component files. This ensures each component file only exports React components, enabling proper Fast Refresh behavior.

## Boundaries & Constraints

**Always:**
- Maintain exact same public API — all existing imports must continue to work
- Preserve all TypeScript types and their exports
- Keep files in the same directory structure
- Follow existing naming conventions (kebab-case for files)
- Maintain all functionality and styling

**Ask First:**
- N/A — this is a pure refactor with no behavioral changes

**Never:**
- Change component behavior or styling
- Modify the public API or break existing imports
- Add new dependencies or change build configuration
- Touch files outside `frontend/src/components/ui/`

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Import component | `import { Badge } from '@/components/ui/badge'` | Component imports successfully | N/A |
| Import variants | `import { badgeVariants } from '@/components/ui/badge'` | Variants import successfully | N/A |
| Hot reload | Edit component file during dev | Fast Refresh updates component without full reload | N/A |
| TypeScript types | Use exported types like `BadgeProps` | Types work correctly in consuming code | N/A |

</frozen-after-approval>

## Code Map

- `frontend/src/components/ui/badge.tsx` -- Exports Badge component + badgeVariants (needs split)
- `frontend/src/components/ui/button.tsx` -- Exports Button component + buttonVariants (needs split)
- `frontend/src/components/ui/form.tsx` -- Exports Form components + useFormField hook (needs split)
- `frontend/src/components/ui/navigation-menu.tsx` -- Exports NavigationMenu components + utility (needs split)
- `frontend/src/components/ui/sidebar.tsx` -- Exports Sidebar components + utility (needs split)
- `frontend/src/components/ui/sonner.tsx` -- Exports Toaster component + utility (needs split)
- `frontend/src/components/ui/toggle.tsx` -- Exports Toggle component + toggleVariants (needs split)

## Tasks & Acceptance

**Execution:**
- [x] `frontend/src/components/ui/badge.variants.ts` -- Create new file exporting badgeVariants and BadgeProps type -- Separates non-component exports
- [x] `frontend/src/components/ui/badge.tsx` -- Import variants from new file, keep only Badge component export -- Enables Fast Refresh
- [x] `frontend/src/components/ui/button.variants.ts` -- Create new file exporting buttonVariants and ButtonProps type -- Separates non-component exports
- [x] `frontend/src/components/ui/button.tsx` -- Import variants from new file, keep only Button component export -- Enables Fast Refresh
- [x] `frontend/src/components/ui/form.utils.ts` -- Create new file exporting useFormField hook and context utilities -- Separates non-component exports
- [x] `frontend/src/components/ui/form.tsx` -- Import utilities from new file, keep only Form component exports -- Enables Fast Refresh
- [x] `frontend/src/components/ui/navigation-menu.utils.ts` -- Create new file exporting navigationMenuTriggerStyle -- Separates non-component exports
- [x] `frontend/src/components/ui/navigation-menu.tsx` -- Import utilities from new file, keep only component exports -- Enables Fast Refresh
- [x] `frontend/src/components/ui/sidebar.utils.ts` -- Create new file exporting useSidebar hook, constants, and sidebarMenuButtonVariants -- Separates non-component exports
- [x] `frontend/src/components/ui/sidebar.tsx` -- Import utilities from new file, keep only component exports -- Enables Fast Refresh
- [x] `frontend/src/components/ui/sonner.utils.ts` -- Create new file exporting toast utility -- Separates non-component exports
- [x] `frontend/src/components/ui/sonner.tsx` -- Import utilities from new file, keep only Toaster component export -- Enables Fast Refresh
- [x] `frontend/src/components/ui/toggle.variants.ts` -- Create new file exporting toggleVariants -- Separates non-component exports
- [x] `frontend/src/components/ui/toggle.tsx` -- Import variants from new file, keep only Toggle component export -- Enables Fast Refresh

**Acceptance Criteria:**
- Given the frontend dev server is running, when I edit any of the 7 component files, then Fast Refresh updates the component without full page reload
- Given existing code imports these components, when I run the build, then all imports resolve correctly with no TypeScript errors
- Given I run `npm run lint`, when the linter checks these files, then zero "react-refresh/only-export-components" warnings appear
- Given the application is running, when I interact with these UI components, then they function identically to before the refactor

## Spec Change Log

## Design Notes

**Pattern to follow:**

For each file, create a sibling file with `.variants.ts` or `.utils.ts` suffix containing:
- All `cva()` variant definitions
- All exported TypeScript interfaces/types
- All utility functions and hooks

Then update the component file to:
- Import the variants/utilities from the new file
- Export only React components
- Re-export the variants/types for backward compatibility

**Example transformation:**

Before (badge.tsx):
```typescript
export const badgeVariants = cva(/* ... */);
export interface BadgeProps extends VariantProps<typeof badgeVariants> {}
function Badge({ ... }) { /* ... */ }
export { Badge, badgeVariants };
```

After (badge.variants.ts):
```typescript
export const badgeVariants = cva(/* ... */);
export interface BadgeProps extends VariantProps<typeof badgeVariants> {}
```

After (badge.tsx):
```typescript
import { badgeVariants, type BadgeProps } from './badge.variants';
function Badge({ ... }) { /* ... */ }
export { Badge, badgeVariants, type BadgeProps };
```

## Verification

**Commands:**
- `npm run lint` -- expected: 0 errors, 0 warnings (down from 7 warnings)
- `npm run build` -- expected: successful build with no TypeScript errors
- `npm run dev` -- expected: dev server starts successfully

**Manual checks (if no CLI):**
- Start dev server, edit one of the 7 component files, verify Fast Refresh works (no full page reload)
- Check that all existing imports in the codebase still resolve correctly
