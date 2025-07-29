import asyncio
import os
import openai
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")

agent = Agent(
        name='PIPI',
        description='Enables Scheduling, Booking, and Management of appointments for a business, and everything else that can be done by a personal assistant',
    )

async def main():
    result = await Runner.run(
        start_agent=agent,
        input=input('Enter a message: '),
    )
    print(result)

if __name__ == '__main__':
    asyncio.run(main())



