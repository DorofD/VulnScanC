# Development Standards

### Component Pattern
- Components should be placed in a directory named after the component.
- Each component directory should contain the `.jsx` file and its corresponding `.css` file.
- For complex components, sub-components should be placed in a `SubComponent/` directory within the parent.

### Styling
- Use component-specific CSS files to avoid global scope pollution.
- For global styles and themes, use the `src/color_themes/` directory.

### API Calls
- Never perform raw `fetch` calls inside components.
- Always use the appropriate service from `src/services/`.
- Use `authFetch.js` for requests requiring authentication.
