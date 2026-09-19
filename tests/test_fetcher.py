from unittest.mock import patch, MagicMock
from f1_data_fetcher import get_historical_driver_standings

@patch("f1_data_fetcher.requests.get")
def test_get_historical_driver_standings_success(mock_get):
    """Verify get_historical_driver_standings correctly parses nested Ergast JSON into formatted output."""
    # 1. Structure the mock JSON exactly as Ergast returns it
    mock_payload = {
        "MRData": {
            "StandingsTable": {
                "season": "2023",
                "StandingsLists": [
                    {
                        "DriverStandings": [
                            {
                                "position": "1",
                                "points": "575",
                                "wins": "19",
                                "Driver": {
                                    "givenName": "Max",
                                    "familyName": "Verstappen"
                                },
                                "Constructors": [{"name": "Red Bull"}]
                            }
                        ]
                    }
                ]
            }
        }
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_payload
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # 2. Call your actual function with a test year
    result = get_historical_driver_standings(2023)

    # 3. Assertions proving real business logic execution
    mock_get.assert_called_once()
    assert "Verstappen" in result
    assert "Red Bull" in result
    assert "575" in result


@patch("f1_data_fetcher.requests.get")
def test_get_historical_driver_standings_handles_http_error(mock_get):
    """Verify error branch returns formatted error string instead of crashing."""
    mock_get.side_effect = Exception("API Connection Timeout")

    result = get_historical_driver_standings(2023)

    assert "Error fetching 2023 F1 standings" in result
    assert "API Connection Timeout" in result