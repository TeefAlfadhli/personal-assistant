from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name='PIPI',
    description='Enables Scheduling, Booking, and Management of appointments for a business, and everything else that can be done by a personal assistant',
)



if __name__ == '__main__':
    mcp.run(transport='stdio')