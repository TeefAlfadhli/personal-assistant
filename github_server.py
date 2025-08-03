from mcp.server.fastmcp import FastMCP
from functionality import  upload_to_github


mcp = FastMCP(
    name='PIPI',
    description='Enables Scheduling, Booking, and Management of appointments for a business, and everything else that can be done by a personal assistant'
)

 


@mcp.tool()
def mcp_upload_tool():
    return upload_to_github()

if __name__ == '__main__':
    mcp.run(transport="sse")