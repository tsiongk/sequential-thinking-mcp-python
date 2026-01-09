# Sequential Thinking MCP Server (Python)

A Python MCP server for structured sequential thinking and reasoning. Built with the [Dedalus MCP framework](https://github.com/dedalus-labs/dedalus-mcp-python).

## Features

- **sequentialthinking** - Record a step in the thinking process
- **get_thinking_history** - Retrieve the full thinking history
- **clear_thinking_history** - Clear the thinking history and start fresh

## Installation

```bash
# Clone the repository
git clone https://github.com/dedalus-labs/sequential-thinking-mcp-python.git
cd sequential-thinking-mcp-python

# Install dependencies with uv
uv sync
```

## Usage

### Running the Server

```bash
uv run python src/main.py
```

The server will start on `http://localhost:3014/mcp`.

### Testing with the Client

```bash
uv run python src/client.py
```

## Tools

### sequentialthinking

Record a step in the thinking process with support for revisions and branching.

**Parameters:**
- `thought` (required): The current thinking step content
- `thought_number` (required): Current step number in the sequence
- `total_thoughts` (required): Estimated total number of steps
- `next_thought_needed` (required): Whether another step is needed
- `is_revision` (optional): Whether this revises a previous thought
- `revises_thought` (optional): Which thought number this revises
- `branch_from_thought` (optional): Start a new branch from this thought
- `branch_id` (optional): Identifier for the new branch

**Returns:** Formatted thinking step with metadata

### get_thinking_history

Retrieve the complete history of thinking steps.

**Parameters:** None

**Returns:** Full thinking history including all branches

### clear_thinking_history

Clear all thinking history and reset state.

**Parameters:** None

**Returns:** Confirmation of cleared history

## Use Cases

- Complex problem decomposition
- Step-by-step reasoning chains
- Exploring alternative solution paths via branching
- Revising earlier conclusions based on new insights

## License

MIT
