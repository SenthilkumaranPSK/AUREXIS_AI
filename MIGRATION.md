# Migration Guide - Frontend Refactoring

## Overview

This document describes the breaking changes introduced in the frontend refactoring (branch: `fix/eslint-warnings-react-refresh`).

**Date:** April 27, 2026  
**Impact:** High - Major architectural changes  
**Affected:** Frontend only (React/TypeScript)

---

## Summary of Changes

### ✅ What Changed

1. **Single-Page Dashboard Architecture**
   - Consolidated 15+ separate page components into one unified `DashboardPage.tsx`
   - Route-based section rendering instead of separate page components
   - All dashboard sections now render within a single layout

2. **React Fast Refresh Fixes**
   - Extracted non-component exports from UI component files
   - Removed separate `.variants.ts` and `.utils.ts` files
   - Inlined variant definitions within component files

3. **Code Cleanup**
   - Removed 10,000+ lines of redundant/unused code
   - Deleted duplicate components and utilities
   - Consolidated constants and services

---

## Breaking Changes

### 🔴 Deleted Files

The following files have been **permanently removed**:

#### Pages (15 files)
```
frontend/src/pages/Dashboard/DashboardPage.tsx (OLD)
frontend/src/pages/AIInsights/AIInsightsPage.tsx
frontend/src/pages/Alerts/AlertsPage.tsx
frontend/src/pages/Chat/ChatPage.tsx
frontend/src/pages/ExpenseAnalysis/ExpenseAnalysisPage.tsx
frontend/src/pages/FinancialHealth/FinancialHealthPage.tsx
frontend/src/pages/Forecasting/ForecastingPage.tsx
frontend/src/pages/Goals/GoalsPage.tsx
frontend/src/pages/Investments/InvestmentsPage.tsx
frontend/src/pages/Profile/ProfilePage.tsx
frontend/src/pages/Reports/ReportsPage.tsx
frontend/src/pages/RiskAnalysis/RiskAnalysisPage.tsx
frontend/src/pages/ScenarioSimulation/ScenarioSimulationPage.tsx
frontend/src/pages/Security/SecurityPage.tsx
frontend/src/pages/Settings/SettingsPage.tsx
```

#### Services (7 files)
```
frontend/src/services/api.ts
frontend/src/services/authService.ts
frontend/src/services/chatService.ts
frontend/src/services/financialService.ts
frontend/src/services/forecastService.ts
frontend/src/services/reportService.ts
frontend/src/services/index.ts
```

#### Components (37 files)
```
frontend/src/components/cards/* (7 files)
frontend/src/components/charts/* (13 files)
frontend/src/components/common/* (3 files)
frontend/src/components/layout/DashboardLayout.tsx
frontend/src/components/layout/Header.tsx
frontend/src/components/layout/PageContainer.tsx
frontend/src/components/layout/Sidebar.tsx
```

#### Constants & Utilities (6 files)
```
frontend/src/constants/colors.ts
frontend/src/constants/index.ts
frontend/src/constants/navigation.ts
frontend/src/constants/routes.ts
frontend/src/utils/formatters.test.ts
frontend/src/test/setup.ts
```

#### UI Component Utilities (6 files)
```
frontend/src/components/ui/badge.variants.ts
frontend/src/components/ui/button.variants.ts
frontend/src/components/ui/form.utils.ts
frontend/src/components/ui/navigation-menu.utils.ts
frontend/src/components/ui/sidebar.utils.ts
frontend/src/components/ui/sonner.utils.ts
frontend/src/components/ui/toggle.variants.ts
```

---

## Migration Path

### For Developers

#### 1. Update Imports

**Before:**
```typescript
import { DashboardPage } from '@/pages/Dashboard/DashboardPage';
import { AlertsPage } from '@/pages/Alerts/AlertsPage';
import { api } from '@/services/api';
import { ROUTES } from '@/constants/routes';
```

**After:**
```typescript
import DashboardPage from '@/pages/DashboardPage';
// All sections are now part of DashboardPage
// Navigate using: /dashboard/alerts, /dashboard/health, etc.
```

#### 2. Update Routes

**Before:**
```typescript
<Route path="/dashboard" element={<DashboardPage />} />
<Route path="/alerts" element={<AlertsPage />} />
<Route path="/health" element={<FinancialHealthPage />} />
```

**After:**
```typescript
<Route path="/dashboard" element={<DashboardPage />} />
<Route path="/dashboard/*" element={<DashboardPage />} />
// All routes handled internally by DashboardPage
```

#### 3. Update Navigation

**Before:**
```typescript
navigate('/alerts');
navigate('/health');
navigate('/investments');
```

**After:**
```typescript
navigate('/dashboard/alerts');
navigate('/dashboard/health');
navigate('/dashboard/investments');
```

#### 4. UI Component Imports

**Before:**
```typescript
import { Button } from '@/components/ui/button';
import { buttonVariants } from '@/components/ui/button.variants';
```

**After:**
```typescript
import { Button, buttonVariants } from '@/components/ui/button';
// Variants are now exported from the same file
```

---

## Available Routes

The new `DashboardPage` supports the following routes:

| Route | Section | Description |
|-------|---------|-------------|
| `/dashboard` | Overview | Main dashboard with key metrics |
| `/dashboard/health` | Financial Health | Health score and analysis |
| `/dashboard/risk` | Risk Analysis | Risk assessment and DTI |
| `/dashboard/savings` | Savings | Savings rate and projections |
| `/dashboard/debt` | Debt Management | Debt overview and payoff plans |
| `/dashboard/investments` | Investments | Portfolio and holdings |
| `/dashboard/goals` | Goals | Financial goals tracking |
| `/dashboard/forecasting` | Forecasting | ML-based predictions |
| `/dashboard/simulation` | Scenario Simulation | What-if analysis |
| `/dashboard/alerts` | Alerts | Notifications and recommendations |
| `/dashboard/reports` | Reports | Financial reports |
| `/dashboard/settings` | Settings | User preferences |

---

## Testing Impact

### Deleted Tests
- `frontend/src/services/authService.test.ts`
- `frontend/src/utils/formatters.test.ts`
- `frontend/src/components/common/ErrorBoundary.test.tsx`
- `frontend/src/test/setup.ts`

### Required New Tests
- `DashboardPage.tsx` component tests
- Route-based section rendering tests
- Navigation flow tests

---

## Rollback Plan

If you need to rollback these changes:

```bash
# Checkout the commit before this refactoring
git checkout 01dab47^

# Or revert the merge commit
git revert <merge-commit-sha>
```

---

## Questions?

If you encounter issues or have questions about this migration:

1. Check this document first
2. Review the new `DashboardPage.tsx` implementation
3. Contact the development team

---

## Checklist for Developers

- [ ] Update all route references to use `/dashboard/*` pattern
- [ ] Update navigation calls to include `/dashboard` prefix
- [ ] Update UI component imports (remove `.variants` imports)
- [ ] Remove references to deleted service files
- [ ] Update tests to cover new DashboardPage
- [ ] Verify all functionality works in new architecture
- [ ] Update any documentation or README files

---

**Last Updated:** April 27, 2026
