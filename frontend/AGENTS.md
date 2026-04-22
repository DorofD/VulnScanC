# Frontend Development Guide

## Tech Stack
- **Framework**: React
- **Bundler**: Webpack
- **Routing**: React Router DOM
- **State Management**: React Context API
- **Styling**: CSS

> [!WARNING]
> **Environment Compatibility**: This project is currently optimized for **Node.js v14.x**. Using newer versions of build tools (webpack, webpack-dev-server, etc.) will cause `SyntaxError` due to incompatible JavaScript syntax. Refer to [architecture_overview.md](./docs/architecture_overview.md) for the required versions.

## Architecture
For a detailed overview of the architecture, see the documentation in the [docs/](./docs/) directory:
- [Architecture Overview](./docs/architecture_overview.md)
- [Directory Structure](./docs/directory_structure.md)
- [Data Flow](./docs/data_flow.md)
- [Development Standards](./docs/development_standards.md)

## Development Commands

### Development
- **Run**: `npm run dev` (inside `frontend/`).

### Build
- **Build**: `npm run build` (inside `frontend/`).
- **Output**: Uses Webpack to output to `dist/`.

## Coding Standards

### Component Structure
- Components should be placed in a directory named after the component: `src/components/ComponentName/`.
- Include `ComponentName.jsx` and `ComponentName.css` in the directory.
- For complex components, use sub-directories for sub-components.

### State and Data
- **Global State**: Use the `src/contexts/` and `src/hooks/` for global state (Auth, Theme, Notifications, etc.).
- **API Calls**: Use the `src/services/` layer. **Do not** use `fetch` directly in components. Use `authFetch.js` for authenticated requests.

### Styling
- Use component-specific CSS files.
- Use the `src/color_themes/` for global theme management.

