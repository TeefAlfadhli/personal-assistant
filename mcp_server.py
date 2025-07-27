try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    # Fallback or error message if FastMCP cannot be imported
    raise ImportError("Could not import FastMCP from mcp.server.fastmcp. Please ensure the module exists and is accessible.")

mcp = FastMCP(
    name='PIPI',
    description='Enables Scheduling, Booking, and Management of appointments for a business, and everything else that can be done by a personal assistant',
)
)


if __name__ == '__main__':
    mcp.run(transport='stdio')