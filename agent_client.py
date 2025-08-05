import asyncio
import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.mcp import MCPServerStdio, MCPServerSse

load_dotenv()

DB_PATH = "database.db"

def save_to_db(user_input, agent_response):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO conversations (user_input, agent_response, timestamp) VALUES (?, ?, ?)",
        (user_input, agent_response, timestamp)
    )
    conn.commit()
    conn.close()

def load_past_conversations():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_input, agent_response FROM conversations ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows

async def main():
    stdio_server_params = {"command": "python", "args": ["mcp_server.py"]}
    sse_server_params = {"url": "http://127.0.0.1:8000/sse"}

    async with MCPServerStdio(stdio_server_params) as stdio_server, MCPServerSse(sse_server_params) as sse_server:
        agent = Agent(
            name="PIPI",
            instructions="You are an assistant that remembers conversations across sessions.",
            model="gpt-4.1",
            mcp_servers=[stdio_server, sse_server]
        )

        # 🧠 Load memory from previous conversations
        conversation_history = load_past_conversations()

        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            # Add memory context to the prompt
            full_prompt = "\n".join([f"You: {u}\nPIPI: {a}" for u, a in conversation_history])
            full_prompt += f"\nYou: {user_input}"

            result = await Runner.run(agent, full_prompt)
            agent_response = result.final_output
            print("🧠 PIPI:", agent_response)

            conversation_history.append((user_input, agent_response))
            save_to_db(user_input, agent_response)

if __name__ == "__main__":
    asyncio.run(main())