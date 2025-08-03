import asyncio
import os
from dotenv import load_dotenv
from agents import Runner, Agent
from agents.mcp import MCPServerStdio

load_dotenv()

async def main():
    server_params= {
        "command": "python",
        "args": ["mcp_server.py"]
    }

    async with MCPServerStdio(server_params) as mcp_server:
        agent = Agent(
            name="PIPI",
            instructions="You are an assistant that uses tools to help me with my tasks.",
            model="gpt-4.1",
            mcp_servers=[mcp_server]
        )

        result = await Runner.run(agent, "create a note with the title 'test' and the body 'this is a test note111'")

        print(result.final_output)
        
if __name__ == "__main__":
    asyncio.run(main())