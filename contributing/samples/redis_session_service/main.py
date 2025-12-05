# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example of using Redis for Session Service."""

import asyncio
import os

from google.adk.errors.already_exists_error import AlreadyExistsError
from google.adk.runners import Runner
from google.genai import types
from regis_service_agent.agent import root_agent

from google.adk_community.sessions import RedisSessionService

APP_NAME = "weather_assistant"
USER_ID = "user_123"
SESSION_ID = "session_01"


async def main():
    """Main function to run the agent asynchronously."""

    redis_uri = os.environ.get("REDIS_URI")
    if not redis_uri:
        raise ValueError(
            "REDIS_URI environment variable not set. See README.md for setup."
        )
    session_service = RedisSessionService(uri=redis_uri)
    try:
        await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
    except AlreadyExistsError:
        # Session already exists, which is fine for this example.
        pass

    runner = Runner(
        agent=root_agent, app_name=APP_NAME, session_service=session_service
    )

    query = "What's the weather like in San Francisco and Tokyo?"
    print(f"User Query -> {query}")
    content = types.Content(role="user", parts=[types.Part(text=query)])

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content,
    ):
        if event.is_final_response():
            print(f"Agent Response -> {event.content.parts[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
