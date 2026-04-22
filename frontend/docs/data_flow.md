# Data Flow and State Management

1.  **Authentication**: The `AuthProvider` wraps the application. It initializes the user state (often from environment variables for local dev or from the backend for production) and provides `accessToken` and `userRole` via `AuthContext`.
2.  **Routing**: `App.jsx` defines the routing structure. `PrivateRoute` is used to protect sensitive routes (e.g., `/admin`, `/ai`, `/projects`) based on the `isAuthenticated` state.
3.  **API Interaction**: Components use custom hooks to trigger actions. These hooks (or the components themselves) call methods from the `services/` layer. The `services/` layer uses `fetch` (or `authFetch`) to communicate with the Flask backend.
4.  **Global UI State**: Components communicate with the UI (e.g., showing a toast notification) by calling methods provided by the `NotificationContext` via the `useNotificationContext` hook.
