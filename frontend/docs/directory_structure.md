# Directory Structure

### `src/components/`
Contains the UI component tree.
- **`Base/`**: Core layout components (e.g., `Base.jsx` — main layout wrapper).
- **Domain components** (directly under `src/components/`): `Projects/`, `Components/`, `Snapshots/`, `BduFstec/`, `Bitbake/`, `DependencyTrack/`, `Sarif/`, `AiBase/`, `AiChat/`, `AiSummary/`, `AiRagDocs/`, `AiLlamaNodes/`, `Admin/`, `Users/`, `Logs/`, `Login/`, `About/`, `MarkdownViewer/`, `Binary/`.
- **Shared components** (directly under `src/components/`): `Button/`, `Modal/`, `Loader/`, `Notification/`, `PrivateRoute/`, `Filter/`, `ColorSchemeSelector/`, `AcceptModal/`, `TimedMessages/`, `MarkdownViewer/`.
- **`Components/`**: The main Components page view, including sub-components in `SubComponents/` (e.g., `ComponentSection.jsx`, `VulnerabilitySection.jsx`, `ProjectSection.jsx`, `CommentModalContent.jsx`).

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
- `useTimedMessagesContext.js`: Access to temporary UI messages.
- `useVulnerabilities.js`: Manages vulnerability data fetching and filtering for components.
- `useComments.js`: Manages comment-related logic.
- `useComponents.js`: Manages component-related logic.
- `useProjects.js`: Manages project-related logic.

### `src/services/`
Abstraction layer for API communication. Each service corresponds to a specific backend resource/endpoint.
- `apiProjects.js`: Project management.
- `apiVulnerabilities.js`: Vulnerability data.
- `apiAi.js`: AI-related interactions.
- `apiLogin.js` / `authFetch.js`: Authentication and token management.
- `apiBduFstec.js`: BDU/FSTEC vulnerability data.
- `apiBitbake.js`: Bitbake integration.
- `apiDependencyTrack.js`: Dependency-Track integration.
- `apiSarif.js`: SARIF viewer data.
- `apiSnapshots.js`: Snapshot management.
- `apiUsers.js`: User management.
- `apiReports.js`: Report generation.
- `apiLicenses.js`: License management.
- `apiLlamaNodes.js`: Llama AI nodes.
- `apiRagDocuments.js`: RAG document management.
- `apiBinary.js`: Binary analysis.
- `apiComments.js`: Comment management.
- `apiComponents.js`: Component API.
- `apiLogin.js`: Login API.
- `apiLogs.js`: Log management.

### `src/color_themes/`
Contains CSS files defining different visual themes for the application.

### `src/svg_images/`
Centralized repository for application-wide SVG icons.
