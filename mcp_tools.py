"""
Tools module for the MCP server.

This module defines all the tools (functions) that the MCP server exposes to clients.
Tools are the core functionality of an MCP server - they are callable functions that
AI assistants and other clients can invoke to perform specific actions.

Each tool should:

- Have a clear, descriptive name
- Include comprehensive docstrings (used by AI to understand when to call the tool)
- Return structured data (typically dict or list)
- Handle errors gracefully
"""

from server import utils
import os
import psycopg
from databricks.sdk import WorkspaceClient


def get_lakebase_connection():
    """Create an authenticated connection to Lakebase."""

    endpoint_name = os.getenv("ENDPOINT_NAME")
    host = os.getenv("PGHOST")
    port = os.getenv("PGPORT", "5432")
    database = os.getenv("PGDATABASE")
    user = os.getenv("PGUSER")
    sslmode = os.getenv("PGSSLMODE", "require")

    missing = []

    if not endpoint_name:
        missing.append("ENDPOINT_NAME")
    if not host:
        missing.append("PGHOST")
    if not database:
        missing.append("PGDATABASE")
    if not user:
        missing.append("PGUSER")

    if missing:
        raise RuntimeError(
            "Missing Lakebase configuration: " + ", ".join(missing)
        )

    workspace = WorkspaceClient()

    credential = workspace.postgres.generate_database_credential(
        endpoint=endpoint_name
    )

    return psycopg.connect(
        host=host,
        port=port,
        dbname=database,
        user=user,
        password=credential.token,
        sslmode=sslmode,
    )


def load_tools(mcp_server):
    @mcp_server.tool
    def health() -> dict:
        """
        Check the health of the MCP server and Databricks connection.

        This is a simple diagnostic tool that confirms the server is running properly.
        It's useful for:
        - Monitoring and health checks
        - Testing the MCP connection
        - Verifying the server is responsive

        Returns:
            dict: A dictionary containing:
                - status (str): The health status ("healthy" if operational)
                - message (str): A human-readable status message

        Example response:
            {
                "status": "healthy",
                "message": "Custom MCP Server is healthy and connected to Databricks Apps."
            }
        """
        return {
            "status": "healthy",
            "message": "Custom MCP Server is healthy and connected to Databricks Apps.",
        }

    @mcp_server.tool
    def get_current_user() -> dict:
        """
        Get information about the current authenticated user.

        This tool retrieves details about the user who is currently authenticated
        with the MCP server. When deployed as a Databricks App, this returns
        information about the end user making the request. When running locally,
        it returns information about the developer's Databricks identity.

        Useful for:
        - Personalizing responses based on the user
        - Authorization checks
        - Audit logging
        - User-specific operations

        Returns:
            dict: A dictionary containing:
                - display_name (str): The user's display name
                - user_name (str): The user's username/email
                - active (bool): Whether the user account is active

        Example response:
            {
                "display_name": "John Doe",
                "user_name": "john.doe@example.com",
                "active": true
            }

        Raises:
            Returns error dict if authentication fails or user info cannot be retrieved.
        """
        try:
            w = utils.get_user_authenticated_workspace_client()
            user = w.current_user.me()
            return {
                "display_name": user.display_name,
                "user_name": user.user_name,
                "active": user.active,
            }
        except Exception as e:
            return {"error": str(e), "message": "Failed to retrieve user information"}

    @mcp_server.tool
      
    def add_itinerary_item(
        trip_id: int,
        activity_id: int,
        activity_date: str,
        start_time: str = None,
        end_time: str = None,
        reason: str = None,
        notes: str = None,
    ) -> dict:
        """
        Add an activity to an existing trip itinerary in Lakebase.
        """

        conn = get_lakebase_connection()

        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO public.itinerary_items
                    (
                        trip_id,
                        activity_id,
                        activity_date,
                        start_time,
                        end_time,
                        status,
                        reason,
                        notes
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING itinerary_item_id
                    """,
                    (
                        trip_id,
                        activity_id,
                        activity_date,
                        start_time,
                        end_time,
                        "planned",
                        reason,
                        notes,
                    ),
                )

                itinerary_item_id = cur.fetchone()[0]

            conn.commit()

            return {
                "success": True,
                "itinerary_item_id": itinerary_item_id,
                "trip_id": trip_id,
                "activity_id": activity_id,
                "activity_date": activity_date,
                "status": "planned",
            }

        except Exception as e:
            conn.rollback()

            return {
                "success": False,
                "error": type(e).__name__ + ": " + str(e),
            }

        finally:
            conn.close()