import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Listing code goes here, properly indented
            tools_response = await session.list_tools()
            print("Available tools:")
            for tool in tools_response.tools:
                print(f" - {tool.name}: {tool.description}")

            resources_response = await session.list_resources()
            print("\nAvailable resources:")
            for res in resources_response.resources:
                print(f" - {res.uri}: {res.description}")

            prompts_response = await session.list_prompts()
            print("\nAvailable prompts:")
            for p in prompts_response.prompts:
                print(f" - {p.name}: {p.description}")

            # More client-server interactions...
            # TODO: Add client-server interactions

if __name__ == "__main__":
    asyncio.run(main())