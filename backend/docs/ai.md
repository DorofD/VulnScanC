# AI API

## Endpoints

### `GET /ai/summary`
Returns a summary of Llama nodes.

- **Auth**: Required.

### `POST /ai/chat`
Sends a chat completion request.

- **Auth**: Required.
- **Request Body**: `{"messages": [...], "use_rag": boolean}`

### `GET /ai/llama_nodes`
Retrieves all Llama nodes.

- **Auth**: Required (Admin role).

### `POST /ai/llama_nodes`
Manages Llama nodes.

- **Auth**: Required (Admin role).
- **Actions**:
  - `add`: `{"action": "add", "values": {...}}`
  - `change`: `{"action": "change", "node_type": "...", "id": ..., "fields_to_change": {...}}`
  - `delete`: `{"action": "delete", "node_type": "...", "id": ...}`
  - `set_active`: `{"action": "set_active", "node_type": "...", "node_uuid": "..."}`

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
- **Actions**:
  - `add`: Requires `file` upload (multipart/form-data).
  - `change`: `{"action": "change", "id": ..., "fields_to_change": {...}}`
  - `delete`: `{"action": "delete", "id": ...}`
