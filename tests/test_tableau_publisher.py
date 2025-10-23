"""
Unit tests for TableauPublisher class
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest

# Add src to path (must be before importing tableau_automation)
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tableau_automation.tableau_publisher import TableauPublisher  # noqa: E402


class TestTableauPublisher:
    """Test cases for TableauPublisher class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.server_url = "https://tableau.test.com"
        self.username = "test_user"
        self.password = "test_password"
        self.site_id = "test_site"

    def test_initialization(self):
        """Test TableauPublisher initialization."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
            site_id=self.site_id,
        )

        assert publisher.server_url == self.server_url
        assert publisher.username == self.username
        assert publisher.site_id == self.site_id
        assert publisher.connected is False
        assert hasattr(publisher, "_password")

    def test_initialization_default_site_id(self):
        """Test TableauPublisher initialization with default site_id."""
        publisher = TableauPublisher(
            server_url=self.server_url, username=self.username, password=self.password
        )

        assert publisher.site_id == ""

    def test_connect(self):
        """Test connection to Tableau Server."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )

        publisher.connect()
        assert publisher.connected is True

    def test_disconnect(self):
        """Test disconnection from Tableau Server."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )

        publisher.connect()
        assert publisher.connected is True

        publisher.disconnect()
        assert publisher.connected is False

    def test_disconnect_when_not_connected(self):
        """Test disconnect does nothing when not connected."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )

        # Should not raise any error
        publisher.disconnect()
        assert publisher.connected is False

    def test_create_hyper_extract(self, tmp_path):
        """Test creating a Hyper extract from DataFrame."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )

        # Create sample DataFrame
        df = pd.DataFrame(
            {"Date": pd.date_range("2024-01-01", periods=10), "Value": range(10)}
        )

        output_path = str(tmp_path / "test_extract.hyper")
        result_path = publisher.create_hyper_extract(df, output_path, table_name="TestTable")

        # Check that CSV was created
        expected_csv_path = output_path.replace(".hyper", ".csv")
        assert result_path == expected_csv_path
        assert os.path.exists(expected_csv_path)

        # Verify CSV content
        loaded_df = pd.read_csv(expected_csv_path)
        assert len(loaded_df) == 10

    def test_create_hyper_extract_empty_dataframe(self):
        """Test creating extract with empty DataFrame raises error."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )

        df = pd.DataFrame()

        with pytest.raises(ValueError, match="DataFrame cannot be None or empty"):
            publisher.create_hyper_extract(df, "/tmp/test.hyper")

    def test_create_hyper_extract_none_dataframe(self):
        """Test creating extract with None DataFrame raises error."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )

        with pytest.raises(ValueError, match="DataFrame cannot be None or empty"):
            publisher.create_hyper_extract(None, "/tmp/test.hyper")

    def test_publish_workbook_not_connected(self):
        """Test publish_workbook raises error when not connected."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )

        with pytest.raises(ConnectionError, match="Not connected to Tableau Server"):
            publisher.publish_workbook("/path/to/workbook.twbx", "TestProject")

    def test_publish_workbook_connected(self):
        """Test publishing a workbook when connected."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )
        publisher.connect()

        result = publisher.publish_workbook(
            "/path/to/workbook.twbx", "TestProject", workbook_name="TestWorkbook"
        )

        assert result["workbook_name"] == "TestWorkbook"
        assert result["project"] == "TestProject"
        assert "published_at" in result
        # Verify it's a valid ISO timestamp
        datetime.fromisoformat(result["published_at"])

    def test_publish_workbook_with_default_name(self):
        """Test publishing a workbook with default name."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )
        publisher.connect()

        result = publisher.publish_workbook("/path/to/my_workbook.twbx", "TestProject")

        assert result["workbook_name"] == "my_workbook.twbx"

    def test_publish_datasource_not_connected(self):
        """Test publish_datasource raises error when not connected."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )

        with pytest.raises(ConnectionError, match="Not connected to Tableau Server"):
            publisher.publish_datasource("/path/to/datasource.tdsx", "TestProject")

    def test_publish_datasource_connected(self):
        """Test publishing a datasource when connected."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )
        publisher.connect()

        result = publisher.publish_datasource(
            "/path/to/datasource.tdsx", "TestProject", datasource_name="TestDataSource"
        )

        assert result["datasource_name"] == "TestDataSource"
        assert result["project"] == "TestProject"
        assert "published_at" in result

    def test_refresh_extract_not_connected(self):
        """Test refresh_extract raises error when not connected."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )

        with pytest.raises(ConnectionError, match="Not connected to Tableau Server"):
            publisher.refresh_extract("datasource-123")

    def test_refresh_extract_connected(self):
        """Test refreshing an extract when connected."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )
        publisher.connect()

        result = publisher.refresh_extract("datasource-123")

        assert result["datasource_id"] == "datasource-123"
        assert result["status"] == "pending"
        assert "refresh_triggered_at" in result

    def test_list_workbooks_not_connected(self):
        """Test list_workbooks raises error when not connected."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )

        with pytest.raises(ConnectionError, match="Not connected to Tableau Server"):
            publisher.list_workbooks()

    def test_list_workbooks_all(self):
        """Test listing all workbooks."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )
        publisher.connect()

        workbooks = publisher.list_workbooks()

        assert isinstance(workbooks, list)
        assert len(workbooks) == 2
        assert workbooks[0]["name"] == "Sales Dashboard"
        assert workbooks[1]["name"] == "Marketing Report"

    def test_list_workbooks_filtered_by_project(self):
        """Test listing workbooks filtered by project."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )
        publisher.connect()

        workbooks = publisher.list_workbooks(project_name="Analytics")

        assert len(workbooks) == 1
        assert workbooks[0]["name"] == "Sales Dashboard"
        assert workbooks[0]["project"] == "Analytics"

    def test_list_workbooks_no_match(self):
        """Test listing workbooks with no matching project."""
        publisher = TableauPublisher(
            server_url=self.server_url,
            username=self.username,
            password=self.password,
        )
        publisher.connect()

        workbooks = publisher.list_workbooks(project_name="NonExistent")

        assert len(workbooks) == 0
