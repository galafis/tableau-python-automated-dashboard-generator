"""
Example: Basic Tableau Workbook Publishing

This example demonstrates how to publish a workbook to Tableau Server.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tableau_automation import TableauPublisher


def main():
    """Publish a workbook to Tableau Server."""
    # Configuration (in production, use environment variables)
    server_url = os.getenv("TABLEAU_SERVER_URL", "https://tableau.example.com")
    username = os.getenv("TABLEAU_USERNAME", "admin")
    password = os.getenv("TABLEAU_PASSWORD", "password")
    site_id = os.getenv("TABLEAU_SITE_ID", "")

    # Initialize publisher
    publisher = TableauPublisher(
        server_url=server_url, username=username, password=password, site_id=site_id
    )

    try:
        # Connect to server
        print("Connecting to Tableau Server...")
        publisher.connect()

        # Publish workbook
        print("\nPublishing workbook...")
        result = publisher.publish_workbook(
            workbook_path="path/to/your/workbook.twbx",
            project_name="Production",
            workbook_name="Sales Dashboard",
        )

        print(f"\n✓ Success!")
        print(f"  Workbook: {result['workbook_name']}")
        print(f"  Project: {result['project']}")
        print(f"  Published at: {result['published_at']}")

    finally:
        # Always disconnect
        publisher.disconnect()


if __name__ == "__main__":
    main()
