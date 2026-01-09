# Copyright (c) 2025 Dedalus Labs, Inc. and its contributors
# SPDX-License-Identifier: MIT

from dedalus_mcp import MCPServer
from dedalus_mcp.server import TransportSecuritySettings

from thinking import thinking_tools


# --- Server ------------------------------------------------------------------

server = MCPServer(
    name="sequential-thinking-mcp",
    http_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    streamable_http_stateless=True,
)


async def main() -> None:
    server.collect(*thinking_tools)
    await server.serve(port=8080)
