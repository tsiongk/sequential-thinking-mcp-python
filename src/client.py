# Copyright (c) 2025 Dedalus Labs, Inc. and its contributors
# SPDX-License-Identifier: MIT

"""Sample MCP client for testing the Sequential Thinking MCP server."""

import asyncio

from dedalus_mcp import MCPClient


SERVER_URL = "http://localhost:3014/mcp"


async def main() -> None:
    client = await MCPClient.connect(SERVER_URL)

    # List tools
    result = await client.list_tools()
    print(f"\nAvailable tools ({len(result.tools)}):\n")
    for t in result.tools:
        print(f"  {t.name}")
        if t.description:
            print(f"    {t.description[:80]}...")
        print()

    # Test sequentialthinking - simulate a thinking chain
    print("--- sequentialthinking ---")
    
    # Thought 1
    thought1 = await client.call_tool(
        "sequentialthinking",
        {
            "thought": "Let me analyze the problem: What is 15% of 80?",
            "next_thought_needed": True,
            "thought_number": 1,
            "total_thoughts": 3,
        },
    )
    print(thought1)
    print()

    # Thought 2
    thought2 = await client.call_tool(
        "sequentialthinking",
        {
            "thought": "To find 15% of 80, I multiply 80 by 0.15: 80 × 0.15 = 12",
            "next_thought_needed": True,
            "thought_number": 2,
            "total_thoughts": 3,
        },
    )
    print(thought2)
    print()

    # Thought 3 (final)
    thought3 = await client.call_tool(
        "sequentialthinking",
        {
            "thought": "The answer is 12. I can verify: 12/80 = 0.15 = 15%. Correct!",
            "next_thought_needed": False,
            "thought_number": 3,
            "total_thoughts": 3,
        },
    )
    print(thought3)
    print()

    # Get history
    print("--- get_thinking_history ---")
    history = await client.call_tool("get_thinking_history", {})
    print(history)
    print()

    # Clear history
    print("--- clear_thinking_history ---")
    clear = await client.call_tool("clear_thinking_history", {})
    print(clear)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
