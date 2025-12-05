# Redis Session Service Sample

This sample demonstrates how to use Redis as a session storage backend for ADK agents using the community package.

## Prerequisites

- Python 3.9+ (Python 3.11+ recommended)
- Redis server running locally or remotely
- ADK and ADK Community installed

## Setup

### 1. Install Dependencies

```bash
pip install google-adk google-adk-community
```

### 2. Set Up Redis Server

#### Option A: Using Homebrew (macOS)

```bash
brew install redis
brew services start redis
```

#### Option B: Using Docker

```bash
docker run -d -p 6379:6379 redis:latest
```

#### Option C: Using apt (Ubuntu/Debian)

```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
```

Once Redis is running, verify the connection:

```bash
redis-cli ping
# Should return: PONG
```

### 3. Configure Environment Variables

Create a `.env` file in this directory:

```bash
# Required: Google API key for the agent
GOOGLE_API_KEY=your-google-api-key

# Required: Redis connection URI
REDIS_URI=redis://localhost:6379
```

**Note:** The default Redis URI assumes Redis is running locally on port 6379. Adjust if your Redis instance is running elsewhere.

## Usage

### Running the Sample

The simplest way to use this sample is to run the included `main.py`:

```bash
python main.py
```

The `main.py` file demonstrates how to:
- Connect to Redis using the `RedisSessionService`
- Create and manage sessions with a unique user ID and session ID
- Use the Runner to execute agent queries while persisting session state

### Using RedisSessionService in Your Code

```python
from google.adk_community.sessions import RedisSessionService
from google.adk.runners import Runner
from google.adk.errors.already_exists_error import AlreadyExistsError

# Create Redis session service
redis_uri = "redis://localhost:6379"
session_service = RedisSessionService(uri=redis_uri)

# Create a session
APP_NAME = "weather_assistant"
USER_ID = "user_123"
SESSION_ID = "session_01"

try:
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
except AlreadyExistsError:
    # Session already exists, which is fine
    pass

# Use with runner
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)

# Run agent queries
async for event in runner.run_async(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=content,
):
    if event.is_final_response():
        print(event.content.parts[0].text)
```

## Sample Structure

```
redis_session_service/
├── main.py                        # Sample using RedisSessionService
├── regis_service_agent/
│   ├── __init__.py                # Agent package initialization
│   └── agent.py                   # Simple weather assistant agent
├── .env                           # Environment variables (create this)
└── README.md                      # This file
```

## Sample Agent

The sample agent (`regis_service_agent/agent.py`) is a simple weather assistant that includes:
- A `get_weather` tool that returns weather information for cities
- Basic agent configuration using Gemini 2.0 Flash

This is a minimal example to demonstrate Redis session persistence without complexity.

## Sample Query

Run the script, and it will execute the query:
```
What's the weather like in San Francisco and Tokyo?
```

The agent will use the `get_weather` tool to retrieve information and respond. All conversation history is stored in Redis, so you can modify the script to add follow-up queries and see session persistence in action.

## Configuration Options

### Redis URI Format

The `REDIS_URI` environment variable supports various Redis connection formats:

- `redis://localhost:6379` - Local Redis instance (default)
- `redis://username:password@host:port` - Redis with authentication
- `rediss://host:port` - Redis with TLS/SSL
- `redis://host:port/db_number` - Specify Redis database number

### RedisSessionService Options

When creating the `RedisSessionService`, you can customize behavior:

```python
session_service = RedisSessionService(
    uri="redis://localhost:6379",
    # Additional configuration options can be added here
)
```

## Features

Redis Session Service provides:

- **Persistent session storage**: Conversation history survives application restarts
- **Multi-session support**: Handle multiple users and sessions simultaneously
- **Fast performance**: In-memory data structure store for quick access
- **Scalability**: Redis can be clustered for high-availability deployments
- **Simple setup**: Works with existing Redis infrastructure

## Troubleshooting

### Connection Issues

If you see connection errors:
1. Verify Redis is running: `redis-cli ping`
2. Check your `REDIS_URI` is correct
3. Ensure no firewall is blocking port 6379

### Session Already Exists

The sample handles `AlreadyExistsError` gracefully. If you want to start fresh:
```bash
redis-cli FLUSHDB
```

## Learn More

- [Redis Documentation](https://redis.io/docs/)
- [ADK Session Documentation](https://google.github.io/adk-docs)
- [ADK Community Repository](https://github.com/google/adk-python-community)
