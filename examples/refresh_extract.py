"""
Example: Refresh Data Source Extract

This example demonstrates how to trigger a data source extract refresh.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tableau_automation import TableauPublisher


def main():
    """Refresh a data source extract on Tableau Server."""
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

        # Refresh extract
        datasource_id = "your-datasource-id-here"
        print(f"\nRefreshing extract for datasource: {datasource_id}...")

        result = publisher.refresh_extract(datasource_id)

        print(f"\n✓ Success!")
        print(f"  Data Source ID: {result['datasource_id']}")
        print(f"  Status: {result['status']}")
        print(f"  Triggered at: {result['refresh_triggered_at']}")

    finally:
        # Always disconnect
        publisher.disconnect()


if __name__ == "__main__":
    main()
