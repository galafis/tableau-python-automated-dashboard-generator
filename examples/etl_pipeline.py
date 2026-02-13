"""
Example: Complete ETL Pipeline with Hyper Extract Creation

This example demonstrates a complete pipeline:
1. Extract data from a source
2. Transform the data
3. Create a Tableau Hyper extract
4. Publish the data source to Tableau Server
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tableau_automation import TableauPublisher


def extract_data():
    """Extract sample sales data."""
    print("1. Extracting data...")

    # Simulate data extraction (in production, this would be from a database)
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=90, freq="D")

    data = {
        "Date": dates,
        "Region": np.random.choice(["North", "South", "East", "West"], 90),
        "Product": np.random.choice(["Product A", "Product B", "Product C"], 90),
        "Sales": np.random.randint(1000, 10000, 90),
        "Units": np.random.randint(10, 100, 90),
    }

    df = pd.DataFrame(data)
    print(f"   ✓ Extracted {len(df)} rows")
    return df


def transform_data(df):
    """Transform and enrich the data."""
    print("\n2. Transforming data...")

    # Add calculated fields
    df["Revenue_Per_Unit"] = df["Sales"] / df["Units"]
    df["Month"] = df["Date"].dt.strftime("%Y-%m")
    df["Day_Of_Week"] = df["Date"].dt.day_name()

    # Add running total
    df = df.sort_values("Date")
    df["Cumulative_Sales"] = df.groupby("Region")["Sales"].cumsum()

    print(f"   ✓ Added {len(df.columns)} columns")
    return df


def main():
    """Run the complete ETL pipeline."""
    print("=" * 60)
    print("TABLEAU ETL PIPELINE")
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
        # ETL Process
        df = extract_data()
        df = transform_data(df)

        # Create Hyper extract
        print("\n3. Creating Tableau Hyper extract...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extract_path = f"/tmp/sales_data_{timestamp}.hyper"

        result_path = publisher.create_hyper_extract(
            df, extract_path, table_name="SalesData"
        )
        print(f"   ✓ Extract saved to: {result_path}")

        # Connect and publish
        print("\n4. Publishing to Tableau Server...")
        publisher.connect()

        result = publisher.publish_datasource(
            datasource_path=result_path,
            project_name="Analytics",
            datasource_name=f"Sales Data - {timestamp}",
        )

        print("\n" + "=" * 60)
        print("✓ Pipeline completed successfully!")
        print("=" * 60)
        print(f"  Data Source: {result['datasource_name']}")
        print(f"  Project: {result['project']}")
        print(f"  Published at: {result['published_at']}")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise

    finally:
        # Always disconnect
        publisher.disconnect()


if __name__ == "__main__":
    main()
