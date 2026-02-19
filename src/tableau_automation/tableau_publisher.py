"""
Tableau Server Automation
Author: Gabriel Demetrios Lafis
Description: Automate Tableau Server operations using Python
"""

import os
from datetime import datetime
from typing import Dict, List

import pandas as pd


class TableauPublisher:
    """
    Automate Tableau Server publishing and data refresh operations.

    Note: This is a demonstration framework. In production, use:
    - tableauserverclient (TSC) for Tableau Server API
    - pantab for creating .hyper files
    """

    def __init__(self, server_url: str, username: str, password: str, site_id: str = ""):
        """
        Initialize Tableau Server connection.

        Parameters:
        -----------
        server_url : str
            Tableau Server URL
        username : str
            Username for authentication
        password : str
            Password for authentication (in production, use environment variables)
        site_id : str
            Site ID (empty string for default site)
        """
        self.server_url = server_url
        self.username = username
        self._password = password  # Store with underscore to indicate private
        self.site_id = site_id
        self.connected = False

        print(f"Tableau Publisher initialized for server: {server_url}")

    def connect(self):
        """
        Establish connection to Tableau Server.
        """
        print("Connecting to Tableau Server...")
        # In production: Use tableauserverclient.Server
        self.connected = True
        print("✓ Connected successfully")

    def disconnect(self):
        """
        Disconnect from Tableau Server.
        """
        if self.connected:
            print("Disconnecting from Tableau Server...")
            self.connected = False
            print("✓ Disconnected")

    def create_hyper_extract(self, df: pd.DataFrame, output_path: str, table_name: str = "Extract"):
        """
        Create a Tableau .hyper extract from a Pandas DataFrame.

        Parameters:
        -----------
        df : pd.DataFrame
            Data to be converted to .hyper format
        output_path : str
            Path where the .hyper file will be saved
        table_name : str
            Name of the table in the extract (used in production implementations)

        Returns:
        --------
        str : Path to the created file
        """
        if df is None or df.empty:
            raise ValueError("DataFrame cannot be None or empty")

        print(f"Creating Tableau .hyper extract: {output_path}")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {len(df.columns)}")
        print(f"  Table name: {table_name}")

        # In production: Use pantab.frame_to_hyper()
        # For demonstration, we'll save as CSV
        csv_path = output_path.replace(".hyper", ".csv")
        df.to_csv(csv_path, index=False)

        print(f"✓ Extract created: {csv_path}")
        return csv_path

    def publish_workbook(self, workbook_path: str, project_name: str, workbook_name: str = None):
        """
        Publish a Tableau workbook to Tableau Server.

        Parameters:
        -----------
        workbook_path : str
            Path to the .twb or .twbx file
        project_name : str
            Target project on Tableau Server
        workbook_name : str
            Name for the published workbook (optional)

        Returns:
        --------
        Dict : Information about the published workbook

        Raises:
        -------
        ConnectionError : If not connected to Tableau Server
        """
        if not self.connected:
            raise ConnectionError("Not connected to Tableau Server. Call connect() first.")

        wb_name = workbook_name or os.path.basename(workbook_path)

        print(f"Publishing workbook: {wb_name}")
        print(f"  File: {workbook_path}")
        print(f"  Project: {project_name}")

        # In production: Use server.workbooks.publish()
        print("✓ Workbook published successfully")

        return {
            "workbook_name": wb_name,
            "project": project_name,
            "published_at": datetime.now().isoformat(),
        }

    def publish_datasource(
        self, datasource_path: str, project_name: str, datasource_name: str = None
    ):
        """
        Publish a data source to Tableau Server.

        Parameters:
        -----------
        datasource_path : str
            Path to the .tds or .tdsx file
        project_name : str
            Target project on Tableau Server
        datasource_name : str
            Name for the published data source (optional)

        Returns:
        --------
        Dict : Information about the published data source

        Raises:
        -------
        ConnectionError : If not connected to Tableau Server
        """
        if not self.connected:
            raise ConnectionError("Not connected to Tableau Server. Call connect() first.")

        ds_name = datasource_name or os.path.basename(datasource_path)

        print(f"Publishing data source: {ds_name}")
        print(f"  File: {datasource_path}")
        print(f"  Project: {project_name}")

        # In production: Use server.datasources.publish()
        print("✓ Data source published successfully")

        return {
            "datasource_name": ds_name,
            "project": project_name,
            "published_at": datetime.now().isoformat(),
        }

    def refresh_extract(self, datasource_id: str):
        """
        Trigger a refresh of a published data source extract.

        Parameters:
        -----------
        datasource_id : str
            ID of the data source to refresh

        Returns:
        --------
        Dict : Information about the refresh operation

        Raises:
        -------
        ConnectionError : If not connected to Tableau Server
        """
        if not self.connected:
            raise ConnectionError("Not connected to Tableau Server. Call connect() first.")

        print(f"Refreshing extract for datasource: {datasource_id}")

        # In production: Use server.datasources.refresh()
        print("✓ Extract refresh triggered")

        return {
            "datasource_id": datasource_id,
            "refresh_triggered_at": datetime.now().isoformat(),
            "status": "pending",
        }

    def list_workbooks(self, project_name: str = None) -> List[Dict]:
        """
        List workbooks on Tableau Server.

        Parameters:
        -----------
        project_name : str
            Filter by project name (optional)

        Returns:
        --------
        List[Dict] : List of workbook information

        Raises:
        -------
        ConnectionError : If not connected to Tableau Server
        """
        if not self.connected:
            raise ConnectionError("Not connected to Tableau Server. Call connect() first.")

        filter_msg = f" in project: {project_name}" if project_name else ""
        print(f"Listing workbooks{filter_msg}...")

        # In production: Use server.workbooks.get()
        workbooks = [
            {"id": "wb1", "name": "Sales Dashboard", "project": "Analytics"},
            {"id": "wb2", "name": "Marketing Report", "project": "Marketing"},
        ]

        if project_name:
            workbooks = [wb for wb in workbooks if wb["project"] == project_name]

        print(f"✓ Found {len(workbooks)} workbook(s)")

        return workbooks


def example_pipeline():
    """
    Example of a complete Tableau automation pipeline.
    """
    print("=" * 60)
    print("TABLEAU AUTOMATION PIPELINE")
    print("=" * 60)
    print()

    # Initialize publisher
    publisher = TableauPublisher(
        server_url="https://tableau.example.com",
        username="admin",
        password = os.getenv("PASSWORD"),
        site_id="analytics",
    )

    # Connect to server
    publisher.connect()

    try:
        # Create sample data
        print("\n1. Creating sample data...")
        import numpy as np  # noqa: E402 — lazy import for demo only

        df = pd.DataFrame(
            {
                "Date": pd.date_range("2024-01-01", periods=100),
                "Sales": np.random.randint(1000, 10000, 100),
                "Region": np.random.choice(["North", "South", "East", "West"], 100),
            }
        )

        # Create Hyper extract
        print("\n2. Creating Tableau extract...")
        extract_path = publisher.create_hyper_extract(
            df, "/tmp/sales_data.hyper", table_name="Sales"
        )

        # Publish data source
        print("\n3. Publishing data source...")
        publisher.publish_datasource(
            extract_path, project_name="Analytics", datasource_name="Sales Data"
        )

        # List workbooks
        print("\n4. Listing workbooks...")
        workbooks = publisher.list_workbooks(project_name="Analytics")
        for wb in workbooks:
            print(f"  - {wb['name']} (ID: {wb['id']})")

        print("\n" + "=" * 60)
        print("✓ Pipeline completed successfully!")
        print("=" * 60)

    finally:
        # Disconnect
        publisher.disconnect()


if __name__ == "__main__":
    example_pipeline()
