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

### Error Handling
- Use the `useTimedMessagesContext` to provide temporary feedback to the user.
- Use the `addMessage` function from the `useTimedMessagesContext` hook.
- The `addMessage` function accepts three arguments: `message` (string), `type` ('success', 'error', 'warning', 'info'), and `duration` (number in milliseconds).
- Example: `addMessage('Operation successful', 'success', 3000)`
- Example: `addMessage('Error: ' + err.message, 'error', 5000)`
- This method is preferred over `NotificationContext` as it automatically handles message expiration.
