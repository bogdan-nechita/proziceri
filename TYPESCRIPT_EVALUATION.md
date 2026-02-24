# TypeScript Adoption Evaluation

## Current State

The codebase is a small, static frontend project with ~160 lines of JavaScript
across 2 source files:

- `proziceri.js` (125 lines) — DOM interaction using jQuery
- `proziceri.logic.js` (31 lines) — pure logic for combining proverbs

There is no build system, no package.json, and no transpilation. Dependencies
(jQuery, PapaParse) are loaded via CDN `<script>` tags. The site is served as
plain static files.

## Recommendation: Not Worth Adopting

The cost-benefit ratio does not justify TypeScript for this project.

### Costs

- **Build toolchain overhead**: Would need to introduce package.json, a
  TypeScript compiler (tsc) or bundler (Vite/esbuild), and a tsconfig.json for
  a project that currently requires no build step at all.
- **Deployment model change**: The HTML loads scripts directly via `<script>`
  tags. A compilation step would need to be added before serving.
- **Type declaration dependencies**: jQuery and PapaParse would need
  `@types/jquery` and `@types/papaparse` packages.
- **Disproportionate infrastructure**: The build tooling would be heavier than
  the application code itself.

### Potential Benefits (Limited)

- Type checking on `constructDadaSaying` — already covered by JSDoc annotations
  and Jest tests.
- IDE autocomplete — marginal value for 2 small files.
- Catching type-related bugs — achievable with lighter-weight alternatives (see
  below).

### Better Alternatives

1. **`// @ts-check`** — Adding this directive to JS files enables TypeScript's
   type checker on plain JavaScript via the existing JSDoc annotations. Zero
   build step, zero config.
2. **ESLint** — Catches real bugs (unused variables, unreachable code, etc.)
   without changing the language or adding a build step.
3. **Expanding JSDoc** — The existing JSDoc in `proziceri.logic.js` already
   provides good type documentation. Extending it to `proziceri.js` would
   improve IDE support without any toolchain changes.

### When It Would Make Sense

TypeScript would become worthwhile if the project:
- Grew significantly in size (10+ modules, 1000+ lines)
- Introduced a build step for other reasons (bundling, minification)
- Added complex data structures or API integrations
- Had multiple contributors working on it concurrently
