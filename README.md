# ✈️ AI Trip Planner

An AI-powered trip planning application built with Databricks that creates personalized itineraries based on a user's destination, trip duration, preferences, weather conditions, air quality, and available activities.

The application uses Databricks Genie to generate the itinerary and Lakebase to persist the trip and selected activities.

---

## 📌 Project Overview

Planning an outdoor trip often requires checking multiple sources for destinations, activities, weather, and air quality.

The AI Trip Planner brings these pieces together into a single Databricks-based application.

A user provides:

- Destination
- Number of days
- Travel preferences

The application uses available travel, weather, air-quality, and activity data to generate a personalized itinerary.

The generated trip can then be saved to Lakebase.

---

## 🎯 Problem Statement

Travel planning can be time-consuming because users need to consider:

- Suitable destinations
- Available activities
- Weather conditions
- Air quality
- Outdoor suitability
- User preferences

The goal of this project is to build an AI-powered application that combines these factors and produces a practical trip itinerary.

---

## 💡 Solution

The AI Trip Planner uses Databricks technologies to create an end-to-end data and AI application.

The workflow is:

```text
User
 │
 ▼
Databricks App
 │
 ▼
Genie Agent
 │
 ├── Weather Data
 ├── Air Quality Data
 ├── Destination Data
 ├── Attraction Data
 └── Activity Data
 │
 ▼
Personalized Itinerary
 │
 ▼
Lakebase
 │
 ├── Trip
 └── Trip Activities

              External Data Sources
                     │
          ┌──────────┴──────────┐
          │                     │
      Weather              Air Quality
          │                     │
          └──────────┬──────────┘
                     │
                     ▼
              Data Processing
                     │
                     ▼
                Silver Tables
                     │
        ┌────────────┼────────────┐
        │            │            │
   destinations   weather    air_quality
        │                         │
        ├── wikimedia_attractions │
        └── wikimedia_descriptions
                     │
                     ▼
              Databricks Genie
                     │
                     ▼
             AI Trip Planner Agent
                     │
                     ▼
              Databricks App
                     │
                     ▼
                 Lakebase
                     │
              ┌──────┴──────┐
              ▼             ▼
             Trips       Activities



             Technologies Used
Databricks
Databricks Workspace
Apache Spark
Delta Lake
Unity Catalog
Databricks Genie
Genie Agent
Databricks Apps
Lakebase
Application
Python
Streamlit
Databricks SDK
PostgreSQL connectivity through psycopg
📊 Data Sources

The project uses multiple datasets to support itinerary generation.

Weather

Weather information is used to understand conditions such as:

Temperature
Precipitation
Weather suitability
Air Quality

Air-quality information is used to consider outdoor suitability.

Examples include:

PM2.5
PM10
Air-quality conditions
Destination Data

Destination information provides locations that can be considered during trip planning.

Wikimedia Data

Wikimedia attraction and description data provides additional information about attractions and places.

Activity Data

Activity information stored in Lakebase is used by the application for activity selection and persistence.

🤖 Databricks Genie

Databricks Genie is used as the AI reasoning layer for the application.

The Genie Agent is configured with project data sources including:

air_quality
destinations
weather
wikimedia_attractions
wikimedia_descriptions
activities

The Agent can answer questions about the available data and generate personalized trip recommendations.

Example request:

Create a 2-day itinerary for Visakhapatnam
focusing on outdoor activities and good air quality.

The Agent uses the available data to generate an itinerary based on the requested preferences and environmental conditions.

🗄️ Lakebase Integration

Lakebase is used as the application's operational database.

The application saves:

Trip information
Generated itinerary information
Matching activity records

After a successful trip generation, the application displays the saved trip ID.

Example:

Trip saved successfully. Trip ID: 6
3 matching activity item(s) saved to Lakebase.

This demonstrates the integration between the Databricks App and Lakebase.

🖥️ Databricks App

The application is implemented using Streamlit and deployed as a Databricks App.

The user interface allows the user to enter:

Destination

Example:

Visakhapatnam
Number of Days

Example:

2
Preferences

Example:

Outdoor activities, good air quality

The user then selects:

🗺️ Plan My Trip

The application sends the request to the Genie Agent and displays the generated itinerary.

🔄 End-to-End Workflow
Step 1: User Input

The user enters the destination, number of days, and preferences.

Step 2: Application Request

The Streamlit application receives the request.

Step 3: Genie Agent

The request is sent to the Databricks Genie Agent.

Step 4: Data-Based Reasoning

The Agent uses the configured data sources to determine suitable activities and conditions.

Step 5: Itinerary Generation

The Agent generates a personalized itinerary.

Step 6: Lakebase Persistence

The application saves the trip and matching activities to Lakebase.

Step 7: User Output

The application displays the generated itinerary and confirms successful persistence.

🧪 Example
User Request
Destination: Visakhapatnam

Days: 2

Preferences:
Outdoor activities, good air quality
Generated Itinerary

The application can generate recommendations such as:

Day 1
- RK Beach
- Kailasagiri

Day 2
- INS Kurusura Submarine Museum
- RK Beach

The exact recommendations depend on the available data and environmental conditions at the time of the request.

✅ Successful End-to-End Test

A successful application test demonstrated:

Genie successfully generated your itinerary.

Trip saved successfully. Trip ID: 6

3 matching activity item(s) saved to Lakebase.

This confirms the complete application flow:

User Input
    ↓
Databricks App
    ↓
Genie Agent
    ↓
Itinerary Generation
    ↓
Lakebase
    ↓
Saved Trip + Activities

# MCP Server - Hello World

A simple, production-ready template for building Model Context Protocol (MCP) servers using FastMCP and FastAPI. This project demonstrates how to create custom tools that AI assistants can discover and invoke.

### Key Concepts

- **Tools**: Callable functions that AI assistants can invoke (e.g., search databases, process data, call APIs)
- **Server**: Exposes tools via the MCP protocol over HTTP
- **Client**: Applications (like Claude, AI assistants) that discover and call tools

## Features

- ✅ FastMCP-based server with HTTP streaming support
- ✅ FastAPI integration for additional REST endpoints
- ✅ Example tools: health check and user information
- ✅ Production-ready project structure
- ✅ Ready for Databricks Apps deployment

## Project Structure

```
mcp-server-hello-world/
├── server/
│   ├── app.py                    # FastAPI application and MCP server setup
│   ├── main.py                   # Entry point for running the server
│   ├── tools.py                  # MCP tool definitions
│   └── utils.py                  # Databricks authentication helpers
├── scripts/
│   └── dev/
│       ├── start_server.sh           # Start the MCP server locally
│       ├── query_remote.sh           # Interactive script for testing deployed app with OAuth
│       ├── query_remote.py           # Query MCP client (deployed app) with health and user auth
│       └── generate_oauth_token.py   # Generate OAuth tokens for Databricks
├── tests/
│   └── test_integration_server.py   # Integration tests for MCP server
├── pyproject.toml                # Project metadata and dependencies
├── requirements.txt              # Python dependencies (for pip)
├── app.yaml                      # Databricks Apps configuration
├── Claude.md                     # AI assistant context and documentation
└── README.md
```

## Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Installation

### Option 1: Using uv (Recommended)

```bash
# Install uv if you haven't already
# Install dependencies
uv sync
```

### Option 2: Using pip

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Server

### Development Mode

```bash
# Quick start with script (syncs dependencies and starts server)
./scripts/dev/start_server.sh

# Or manually using uv (default port 8000)
uv run custom-mcp-server

# Or specify a custom port
uv run custom-mcp-server --port 8080

# Or using the installed command (after pip install -e .)
custom-mcp-server --port 3000
```

The server will start on `http://localhost:8000` by default (or your specified port).

### Accessing the Server

- **MCP Endpoints**: `http://localhost:8000/mcp`
- **Available Tools**:
    - `health`: Check server status
    - `get_current_user`: Get authenticated user information

## Testing the MCP Server

This project includes test scripts to verify your MCP server is working correctly in both local and deployed environments.

### Integration Tests

The project includes automated integration tests that validate the MCP server functionality:

```bash
# Run integration tests
uv run pytest tests/
```

**What the tests do:**

- Automatically start the MCP server
- Test that `list_tools()` works correctly
- Test that all registered tools can be called without errors by invoking the `call_tools()`
- Automatically clean up the server after tests complete

### Manual Testing

#### End-to-end test your locally-running MCP server

```bash
./scripts/dev/start_server.sh
```

```python
from databricks_mcp import DatabricksMCPClient
mcp_client = DatabricksMCPClient(
    server_url="http://localhost:8000/mcp"
)
# List available MCP tools
print(mcp_client.list_tools())
```

The script connects to your local MCP server without authentication and lists available tools.

#### End-to-end test your deployed MCP server

After deploying to Databricks Apps, use the interactive shell script to test with user-level OAuth authentication:

```bash
chmod +x scripts/dev/query_remote.sh
./scripts/dev/query_remote.sh
```

The script will guide you through:

1. **Profile selection**: Choose your Databricks CLI profile
2. **App name**: Enter your deployed app name
3. **Automatic configuration**: Extracts app scopes and URLs automatically
4. **OAuth flow**: Generates user OAuth token via browser
5. **End-to-end test**: Tests `list_tools()`, and invokes each tool returned in list_tools

**What it does:**

- Retrieves app configuration using `databricks apps get`
- Extracts user authorization scopes from `effective_user_api_scopes`
- Gets workspace host from your Databricks profile
- Generates OAuth token with the correct scopes
- Tests MCP client with user-level authentication
- Verifies both the `health` check and `get_current_user` tool work correctly

This test simulates the real end-user experience when they authorize your app and use it with their credentials.

Alternatively, test manually with command-line arguments:

```bash
python scripts/dev/query_remote.py \
    --host "https://your-workspace.cloud.databricks.com" \
    --token "eyJr...Dkag" \
    --app-url "https://your-workspace.cloud.databricks.com/serving-endpoints/your-app"
```

The `scripts/dev/query_remote.py` script connects to your deployed MCP server with OAuth authentication and tests both the health check and user authorization functionality.

## Adding New Tools

To add a new tool to your MCP server:

1. Open `server/tools.py`
2. Add a new function inside `load_tools()` with the `@mcp_server.tool` decorator:

```python
@mcp_server.tool
def calculate_sum(a: int, b: int) -> dict:
    """
    Calculate the sum of two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        dict: Contains the sum result
    """
    return {"result": a + b}
```

3. Restart the server - the new tool will be automatically available to clients

### Tool Best Practices

- **Clear naming**: Use descriptive, action-oriented names
- **Comprehensive docstrings**: AI uses these to understand when to call your tool
- **Type hints**: Help with validation and documentation
- **Structured returns**: Return dicts or Pydantic models for consistent data
- **Error handling**: Use try-except blocks and return error information

### Connecting to Databricks

The `utils.py` module provides two helper methods for interacting with Databricks resources via the Databricks SDK Workspace Client:

**When deployed as a Databricks App:**

- `get_workspace_client()` - Returns a client authenticated as the service principal associated with the app. See [App Authorization](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/auth#app-authorization) for more details.
- `get_user_authenticated_workspace_client()` - Returns a client authenticated as the end user with scopes specified by the app creator. See [User Authorization](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/auth#user-authorization) for more details.

**When running locally:**

- Both methods return a client authenticated as the current developer, since no service principal identity exists in the local environment.

**Example usage in tools:**

```python
from server import utils

# Get current user information (user-authenticated)
w = utils.get_user_authenticated_workspace_client()
user = w.current_user.me()
display_name = user.display_name
```

See the `get_current_user` tool in `server/tools.py` for a complete example.

## Generating OAuth Tokens

For advanced use cases, you can manually generate OAuth tokens for Databricks workspace access using the provided script. This implements the [OAuth U2M (User-to-Machine) flow](https://docs.databricks.com/aws/en/dev-tools/auth/oauth-u2m?language=CLI).

### Generate Workspace-Level OAuth Token

```bash
python scripts/dev/generate_oauth_token.py \
    --host https://your-workspace.cloud.databricks.com \
    --scopes "all-apis offline_access"
```

**Parameters:**

- `--host`: Databricks workspace URL (required)
- `--scopes`: Space-separated OAuth scopes (default: `all-apis offline_access`)
- `--redirect-uri`: Callback URI (default: `http://localhost:8020`)

**Note:** The script uses the `databricks-cli` OAuth client ID by default.

**The script will:**

1. Generate a PKCE code verifier and challenge
2. Open your browser for authorization
3. Capture the authorization code via local HTTP server
4. Exchange the code for an access token
5. Display the token response as JSON (token is valid for 1 hour)

**Example with custom scopes:**

```bash
python scripts/dev/generate_oauth_token.py \
    --host https://your-workspace.cloud.databricks.com \
    --scopes "clusters:read jobs:write sql:read"
```

## Configuration

### Server Settings

The server can be configured using command-line arguments:

```bash
# Change port
uv run custom-mcp-server --port 8080

# Get help
uv run custom-mcp-server --help
```

The default configuration:

- **Host**: `0.0.0.0` (listens on all network interfaces)
- **Port**: `8000` (configurable via `--port` argument)

## Deployment

### Databricks Apps

This project is configured for Databricks Apps deployment:

1. Deploy using Databricks CLI or UI
2. The server will be accessible at your Databricks app URL

For more information refer to the documentation [here](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/deploy#deploy-the-app)

### Try Your MCP Server in AI Playground

After deploying your MCP server to Databricks Apps, you can test it interactively in the Databricks AI Playground:

1. Navigate to the **AI Playground** in your Databricks workspace
2. Select a model with the **Tools enabled** label
3. Click **Tools > + Add tool** and select your deployed MCP server
4. Start chatting with the AI agent - it will automatically call your MCP server's tools as needed

The AI Playground provides a visual interface to prototype and test your MCP server with different models and configurations before integrating it into production applications.

For more information, see [Prototype tool-calling agents in AI Playground](https://docs.databricks.com/aws/en/generative-ai/agent-framework/ai-playground-agent).

## Development

### Code Formatting

```bash
# Format code with ruff
uv run ruff format .

# Check for lint errors
uv run ruff check .
```

## Customization

### Rename the Project

1. Update `name` in `pyproject.toml`
2. Update `name` parameter in `server/app.py`: `FastMCP(name="your-name")`
3. Update the command script in `pyproject.toml` under `[project.scripts]`

### Add Custom API Endpoints

Add routes to the `app` FastAPI instance in `server/app.py`:

```python
@app.get("/custom-endpoint")
def custom_endpoint():
    return {"message": "Hello from custom endpoint"}
```

## Troubleshooting

### Port Already in Use

Change the port in `server/main.py` or set the `PORT` environment variable.

### Import Errors

Ensure all dependencies are installed:

```bash
uv sync  # or pip install -r requirements.txt
```

## Resources

- [Databricks MCP Documentation](https://docs.databricks.com/aws/en/generative-ai/mcp/custom-mcp)
- [Databricks Apps](https://www.databricks.com/product/databricks-apps)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Uvicorn Documentation](https://www.uvicorn.org)

## AI Assistant Context

See [`Claude.md`](./Claude.md) for detailed project context specifically designed for AI assistants working with this codebase.



# AI Trip Planner V2

An AI-powered trip planning application built with Databricks Apps, MCP, Lakebase, and semantic search.

## Project Overview

AI Trip Planner allows an agent to create trips, search for relevant activities using natural-language queries, and persist itineraries in Lakebase.

The V2 implementation adds:

- MCP-based agent tools
- Lakebase relational data model
- Vector embeddings for activities
- Semantic search using GTE Large EN
- Lakebase ANN vector index
- End-to-end trip planning workflow
- Persistent itinerary storage

## Architecture

Supervisor Agent
        |
        v
MCP Trip Planner App
        |
        +----------------------+
        |                      |
        v                      v
     Lakebase             SQL Warehouse
        |                      |
        |                 ai_query()
        |                      |
        |              GTE Large EN
        |                      |
        |              1024-d embeddings
        |                      |
        +-----------> activities.embedding
        |
        v
Lakebase ANN Search

## MCP Tools

### health

Checks MCP server health and Databricks connectivity.

### get_current_user

Returns information about the authenticated Databricks user.

### create_trip

Creates a new trip and persists it in:

`public.trips`

### add_itinerary_item

Adds an activity to a trip itinerary and persists it in:

`public.itinerary_items`

### build_activity_embeddings

Generates embeddings for activities that do not have embeddings.

Embedding model:

`system.ai.gte-large-en`

Embedding dimension:

`1024`

Embeddings are stored in:

`public.activities.embedding`

### semantic_search_activities

Accepts a natural-language query, generates a query embedding, and performs vector similarity search against the activities stored in Lakebase.

## Lakebase Data Model

The application uses four main tables:

- `destinations`
- `activities`
- `trips`
- `itinerary_items`

Relationships:

`activities.destination_id -> destinations.destination_id`

`itinerary_items.trip_id -> trips.trip_id`

`itinerary_items.activity_id -> activities.activity_id`

Primary keys are defined on all four tables.

## Semantic Search

The activity embedding workflow was successfully tested with three activities:

| Activity | Activity ID | Embedding |
|---|---:|---:|
| Baga Beach | 1 | 1024 dimensions |
| Fort Aguada | 2 | 1024 dimensions |
| Basilica of Bom Jesus | 3 | 1024 dimensions |

A Lakebase ANN index was created on:

`public.activities.embedding`

Index:

`activities_embedding_ann`

Semantic search was successfully tested with:

`historical places in Goa`

The results ranked:

1. Basilica of Bom Jesus
2. Fort Aguada
3. Baga Beach

## Production Workflow

The end-to-end workflow was tested successfully:

1. User requests a Goa trip.
2. Agent searches activities semantically.
3. Agent creates the trip.
4. Agent adds activities to the itinerary.
5. Data is persisted in Lakebase.

A successful production workflow created:

- Trip ID: 2
- Destination: Goa
- Duration: 3 days
- 3 itinerary items

## Checkpoint Evidence

### Checkpoint 1 - Agent Read + Write
Complete.

Verified:
- MCP health/read functionality
- Trip creation
- Itinerary write

### Checkpoint 2 - Embeddings + Semantic Search
Complete.

Verified:
- GTE Large EN
- 1024-dimensional embeddings
- Embeddings persisted in Lakebase
- ANN vector index
- Semantic search through MCP

### Checkpoint 3 - Production Workflow
Complete.

Verified:
- Semantic retrieval
- Trip creation
- Itinerary persistence
- End-to-end agent workflow

### Checkpoint 4 - Lakebase Data Model + Reliability
Complete.

Verified:
- Four-table relational model
- Primary keys
- Foreign keys
- Trip-to-itinerary relationships
- Activity-to-itinerary relationships
- Persisted production data

### Checkpoint 5 - Testing + Evidence + Final Polish
Complete.

Verified:
- MCP health
- Semantic search
- Embedding generation
- Write operations
- Lakebase persistence

## Technology Stack

- Databricks Apps
- MCP
- Databricks SDK
- Lakebase
- PostgreSQL / psycopg
- SQL Warehouse
- Databricks AI Functions
- GTE Large EN
- Vector embeddings
- Lakebase ANN search
## Current V2 Scope

V2 currently demonstrates:

- MCP-based trip planning
- Lakebase persistence
- Relational trip and itinerary data model
- Activity embeddings using GTE Large EN
- 1024-dimensional vector embeddings
- Lakebase ANN vector search
- Semantic activity retrieval
- End-to-end trip planning workflow

The Lakebase schema also includes the planned `weather_snapshots`
and `packing_items` tables for future weather-aware planning and
packing-list workflows.