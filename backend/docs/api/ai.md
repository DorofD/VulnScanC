# AI API

## Endpoints

### `GET /ai/summary`
Returns a summary of Llama nodes.

- **Auth**: Required.

### `POST /ai/chat`
Sends a chat completion request.

- **Auth**: Required.
- **Request Body** (JSON):
  - `messages` (required): List of message objects (role and content).
  - `use_rag` (optional): boolean.

### `GET /ai/llama_nodes`
Retrieves all Llama nodes.

- **Auth**: Required (Admin role).

### `POST /ai/llama_nodes`
Manages Llama nodes.

- **Auth**: Required (Admin role).
- **Actions**:
  - `add`: `{"action": "add", "values": {"model_type": "chat" | "embedding", ...}}`
  - `change`: `{"action": "change", "node_type": "chat" | "embedding", "id": ..., "fields_to_change": {...}}`
    - *Note*: If `model_type` is changed in `fields_to_change`, the node is moved between tables.
  - `delete`: `{"action": "delete", "node_type": "chat" | "embedding", "id": ...}`
  - `set_active`: `{"action": "set_active", "node_type": "chat" | "embedding", "node_uuid": "..."}`

### `GET /ai/llama_chat_nodes`
Retrieves chat-specific Llama nodes.

- **Auth**: Required (Admin role).

### `POST /ai/llama_chat_nodes`
Manages chat Llama nodes.

- **Auth**: Required (Admin role).
- **Actions**: `add`, `change`, `delete`.

### `GET /ai/llama_embedding_nodes`
Retrieves embedding-specific Llama nodes.

- **Auth**: Required (Admin role).

### `POST /ai/llama_embedding_nodes`
Manages embedding Llama nodes.

- **Auth**: Required (Admin role).
- **Actions**: `add`, `change`, `delete`.

### `GET /ai/rag_documents`
Retrieves RAG documents.

- **Auth**: Required (Admin role).

### `POST /ai/rag_documents`
Manages RAG documents.

- **Auth**: Required (Admin role).
- **Content-Type**: `multipart/form-data` (for `add`) or `application/json` (for `change`/`delete`).
- **Actions**:
  - `add`: Requires `file` (PDF) and optionally `description` in `values` or form fields.
  - `change`: `{"action": "change", "id": ..., "fields_to_change": {...}}`
  - `delete`: `{"action": "delete", "id": ...}`

