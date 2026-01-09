# Copyright (c) 2025 Dedalus Labs, Inc. and its contributors
# SPDX-License-Identifier: MIT

"""Sequential Thinking operations for MCP server.

A tool for dynamic and reflective problem-solving through thoughts.
No API key required.
"""

from typing import Any

from pydantic import BaseModel

from dedalus_mcp import tool


# --- Thought History (module-level state) ------------------------------------

_thought_history: list[dict[str, Any]] = []
_branches: dict[str, list[dict[str, Any]]] = {}


# --- Response Models ---------------------------------------------------------


class ThinkingResult(BaseModel):
    """Sequential thinking result."""

    success: bool
    data: Any = None
    error: str | None = None


# --- Helper ------------------------------------------------------------------


def _format_thought(thought_data: dict[str, Any]) -> str:
    """Format a thought for display."""
    thought_num = thought_data["thought_number"]
    total = thought_data["total_thoughts"]
    thought = thought_data["thought"]
    is_revision = thought_data.get("is_revision", False)
    revises = thought_data.get("revises_thought")
    branch_from = thought_data.get("branch_from_thought")
    branch_id = thought_data.get("branch_id")

    if is_revision:
        prefix = "🔄 Revision"
        context = f" (revising thought {revises})"
    elif branch_from:
        prefix = "🌿 Branch"
        context = f" (from thought {branch_from}, ID: {branch_id})"
    else:
        prefix = "💭 Thought"
        context = ""

    return f"{prefix} {thought_num}/{total}{context}: {thought}"


# --- Sequential Thinking Tool ------------------------------------------------


@tool(
    description="""A detailed tool for dynamic and reflective problem-solving through thoughts.
This tool helps analyze problems through a flexible thinking process that can adapt and evolve.
Each thought can build on, question, or revise previous insights as understanding deepens.

When to use this tool:
- Breaking down complex problems into steps
- Planning and design with room for revision
- Analysis that might need course correction
- Problems where the full scope might not be clear initially
- Problems that require a multi-step solution
- Tasks that need to maintain context over multiple steps
- Situations where irrelevant information needs to be filtered out

Key features:
- You can adjust total_thoughts up or down as you progress
- You can question or revise previous thoughts
- You can add more thoughts even after reaching what seemed like the end
- You can express uncertainty and explore alternative approaches
- Not every thought needs to build linearly - you can branch or backtrack
- Generates a solution hypothesis
- Verifies the hypothesis based on the Chain of Thought steps
- Repeats the process until satisfied
- Provides a correct answer

Parameters explained:
- thought: Your current thinking step
- next_thought_needed: True if you need more thinking
- thought_number: Current number in sequence
- total_thoughts: Current estimate of thoughts needed (can be adjusted)
- is_revision: Boolean indicating if this thought revises previous thinking
- revises_thought: If is_revision is true, which thought number is being reconsidered
- branch_from_thought: If branching, which thought number is the branching point
- branch_id: Identifier for the current branch (if any)
- needs_more_thoughts: If reaching end but realizing more thoughts needed"""
)
async def sequentialthinking(
    thought: str,
    next_thought_needed: bool,
    thought_number: int,
    total_thoughts: int,
    is_revision: bool = False,
    revises_thought: int | None = None,
    branch_from_thought: int | None = None,
    branch_id: str | None = None,
    needs_more_thoughts: bool = False,
) -> ThinkingResult:
    """Process a thought in the sequential thinking chain.

    Args:
        thought: Your current thinking step.
        next_thought_needed: Whether another thought step is needed.
        thought_number: Current thought number (starts at 1).
        total_thoughts: Estimated total thoughts needed.
        is_revision: Whether this revises previous thinking.
        revises_thought: Which thought is being reconsidered.
        branch_from_thought: Branching point thought number.
        branch_id: Branch identifier.
        needs_more_thoughts: If more thoughts are needed.

    Returns:
        ThinkingResult with thought processing status.
    """
    global _thought_history, _branches

    try:
        # Validate inputs
        if not thought or not isinstance(thought, str):
            return ThinkingResult(success=False, error="Invalid thought: must be a non-empty string")
        if thought_number < 1:
            return ThinkingResult(success=False, error="Invalid thought_number: must be >= 1")
        if total_thoughts < 1:
            return ThinkingResult(success=False, error="Invalid total_thoughts: must be >= 1")

        # Adjust total if needed
        if thought_number > total_thoughts:
            total_thoughts = thought_number

        # Create thought data
        thought_data = {
            "thought": thought,
            "thought_number": thought_number,
            "total_thoughts": total_thoughts,
            "next_thought_needed": next_thought_needed,
            "is_revision": is_revision,
            "revises_thought": revises_thought,
            "branch_from_thought": branch_from_thought,
            "branch_id": branch_id,
            "needs_more_thoughts": needs_more_thoughts,
        }

        # Store in history
        _thought_history.append(thought_data)

        # Handle branching
        if branch_from_thought and branch_id:
            if branch_id not in _branches:
                _branches[branch_id] = []
            _branches[branch_id].append(thought_data)

        # Format and log thought
        formatted = _format_thought(thought_data)
        print(formatted)  # Server-side logging

        return ThinkingResult(
            success=True,
            data={
                "thought_number": thought_number,
                "total_thoughts": total_thoughts,
                "next_thought_needed": next_thought_needed,
                "branches": list(_branches.keys()),
                "thought_history_length": len(_thought_history),
                "formatted_thought": formatted,
            },
        )
    except Exception as e:
        return ThinkingResult(success=False, error=str(e))


@tool(
    description="Get the current thought history and branch information for the sequential thinking session."
)
async def get_thinking_history() -> ThinkingResult:
    """Get the current thought history.

    Returns:
        ThinkingResult with thought history and branches.
    """
    return ThinkingResult(
        success=True,
        data={
            "thought_count": len(_thought_history),
            "branches": list(_branches.keys()),
            "history": _thought_history[-10:],  # Last 10 thoughts
        },
    )


@tool(
    description="Clear the thought history and start a fresh sequential thinking session."
)
async def clear_thinking_history() -> ThinkingResult:
    """Clear the thought history.

    Returns:
        ThinkingResult confirming the history was cleared.
    """
    global _thought_history, _branches
    _thought_history = []
    _branches = {}
    
    return ThinkingResult(
        success=True,
        data={"message": "Thought history cleared."},
    )


# --- Export ------------------------------------------------------------------

thinking_tools = [
    sequentialthinking,
    get_thinking_history,
    clear_thinking_history,
]
