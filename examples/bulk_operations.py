"""
Example: Bulk Operations - Refresh All Extracts in a Project

This example demonstrates how to perform bulk operations across multiple
data sources, such as refreshing all extracts in a specific project.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tableau_automation import TableauPublisher


def refresh_all_extracts(publisher, project_name):
    """
    Refresh all data source extracts in a project.

    Note: This is a demonstration. In production, you would:
    1. List all datasources using server.datasources.get()
    2. Filter by project
    3. Refresh each extract
    """
    print(f"\nRefreshing all extracts in project: {project_name}")
    print("-" * 60)

    # In production, get actual datasources from Tableau Server
    # For demo, using mock data
    mock_datasources = [
        {"id": "ds-001", "name": "Sales Data", "project": project_name},
        {"id": "ds-002", "name": "Inventory Data", "project": project_name},
        {"id": "ds-003", "name": "Customer Data", "project": project_name},
    ]

    print(f"Found {len(mock_datasources)} data sources")

    success_count = 0
    failed_count = 0

    for ds in mock_datasources:
        try:
            print(f"\n  Refreshing: {ds['name']} (ID: {ds['id']})")
            result = publisher.refresh_extract(ds["id"])
            print(f"    ✓ Success - Status: {result['status']}")
            success_count += 1
        except Exception as e:
            print(f"    ✗ Failed - Error: {e}")
            failed_count += 1

    print("\n" + "-" * 60)
    print(f"Summary:")
    print(f"  ✓ Successful: {success_count}")
    print(f"  ✗ Failed: {failed_count}")
    print(f"  Total: {len(mock_datasources)}")


def list_all_workbooks(publisher, project_name=None):
    """List all workbooks, optionally filtered by project."""
    print("\nListing workbooks...")
    print("-" * 60)

    workbooks = publisher.list_workbooks(project_name=project_name)

    if workbooks:
        print(f"Found {len(workbooks)} workbook(s):\n")
        for wb in workbooks:
            print(f"  - {wb['name']}")
            print(f"    ID: {wb['id']}")
            print(f"    Project: {wb['project']}")
            print()
    else:
        print("No workbooks found")


def main():
    """Demonstrate bulk operations."""
    print("=" * 60)
    print("TABLEAU BULK OPERATIONS")
    print("=" * 60)

    # Configuration
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
        publisher.connect()

        # Operation 1: List all workbooks
        list_all_workbooks(publisher)

        # Operation 2: List workbooks in specific project
        list_all_workbooks(publisher, project_name="Analytics")

        # Operation 3: Bulk refresh extracts
        refresh_all_extracts(publisher, project_name="Analytics")

        print("\n" + "=" * 60)
        print("✓ Bulk operations completed!")
        print("=" * 60)

    finally:
        publisher.disconnect()


if __name__ == "__main__":
    main()
