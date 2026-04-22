# Directory Structure

### `src/components/`
Contains the UI component tree.
- **`Base/`**: Core layout components (e.g., Sidebar, Main layout wrapper).
- **`Features/`**: Domain-specific components (e.g., `Projects`, `Bitbake`, `DependencyTrack`, `AiChat`, `Users`).
- **`Common/`**: Reusable UI elements (e.g., `Button`, `Modal`, `Loader`, `Notification`).
- **`Views/`**: High-level components that represent specific routes/pages.

### `src/contexts/`
Implements the **Context API** for global state management.
- `AuthContext.js`: Manages user authentication state, roles, and tokens.
- `NotificationContext.js`: Manages global UI notifications.
- `SidebarStateContext.js`: Manages the visibility/state of the sidebar.
- `ColorSchemeContext.js`: Manages the active UI color theme.
- `TimedMessagesContext.js`: Manages temporary UI messages.

### `src/hooks/`
Custom React hooks that provide access to contexts and encapsulate logic.
- `useAuthContext.js`: Access to authentication state.
- `useNotificationContext.js`: Access to notification logic.
- `useSidebarStateContext.js`: Access to sidebar state.
- `useColorThemeContext.js`: Access to theme switching logic.

### `src/services/`
Abstraction layer for API communication. Each service corresponds to a specific backend resource/endpoint.
- `apiProjects.js`: Project management.
- `apiVulnerabilities.js`: Vulnerability data.
- `apiAi.js`: AI-related interactions.
- `apiAuth.js` / `authFetch.js`: Authentication and token management.
- ... and other domain-specific services.

### `src/color_themes/`
Contains CSS files defining different visual themes for the application.

### `src/svg_images/`
Centralized repository for application-wide SVG icons.
