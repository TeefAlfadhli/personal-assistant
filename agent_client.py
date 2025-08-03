import asyncio
import os
from dotenv import load_dotenv
from agents import Runner, Agent
from agents.mcp import MCPServerStdio, MCPServerSse

load_dotenv()

async def main():
    stdio_server_params = {
        "command": "python",
        "args": ["mcp_server.py"]
    }
    sse_server_params = {"url": "http://127.0.0.1:8000/sse"}  
    # First start stdio server
    async with MCPServerStdio(stdio_server_params) as stdio_server:
        # Then start SSE server separately inside
        async with MCPServerSse(sse_server_params) as sse_server:
            agent = Agent(
                name="PIPI",
                instructions="You are an assistant that uses tools to help me with my tasks.",
                model="gpt-4.1",
                mcp_servers=[stdio_server, sse_server]
            )

            task = input("What would you like me to do? ")
            result = await Runner.run(agent, task)
            print("🧠 Final Result:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())