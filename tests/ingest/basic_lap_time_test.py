# flake8: noqa: E402
import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from unittest.mock import MagicMock, patch
import pytest

# --- Resto de imports ---
from src.ingest.basic_lap_time import load_driver_laps, validate_fast_f1_Request

# ---------- TESTS PARA validate_fast_f1_Request ----------


def test_validate_fast_f1_request_valid():
    """Test that validate_fast_f1_Request accepts valid parameters without raising."""
    validate_fast_f1_Request(2020, "Spain", "FP1", "VER")


def test_validate_fast_f1_request_missing_param():
    """Test that validate_fast_f1_Request raises an exception for missing parameters."""
    with pytest.raises(Exception, match="Parameters must be filled"):
        validate_fast_f1_Request(None, "Spain", "FP1", "VER")


def test_validate_fast_f1_request_all_missing_params():
    """Test that validate_fast_f1_Request raises an exception when all parameters are None."""
    with pytest.raises(Exception, match="Parameters must be filled"):
        validate_fast_f1_Request(None, None, None, None)


def test_validate_fast_f1_request_invalid_year():
    """Test that validate_fast_f1_Request raises an exception for years before 1950."""
    with pytest.raises(Exception, match="Api not supports values under 1950"):
        validate_fast_f1_Request(1949, "Spain", "FP1", "VER")


# ---------- TESTS PARA load_driver_laps ----------


@pytest.fixture
def test_load_driver_laps(mock_to_csv, mock_get_session):
    # --- Preparar mocks ---
    # Simula un objeto "laps" con columnas necesarias
    mock_laps = pd.DataFrame(
        {
            "Driver": ["ALO", "ALO"],
            "LapTime": [
                pd.to_timedelta("0 days 00:01:19.104000"),
                pd.to_timedelta("0 days 00:01:20.050000"),
            ],
            "LapNumber": [1, 2],
        }
    )

    mock_session = MagicMock()
    mock_session.laps.pick_drivers.return_value = mock_laps
    mock_get_session.return_value = mock_session

    # --- Ejecutar función ---
    load_driver_laps(2021, "Spain", "FP1", "ALO")

    # --- Verificaciones ---
    mock_get_session.assert_called_once_with(2021, "Spain", "FP1")
    mock_to_csv.assert_called_once()

    # Capturamos el DataFrame pasado a to_csv
    args, kwargs = mock_to_csv.call_args
    assert "lapTimeDataTest_ALO.csv" in args[0]
    assert not kwargs.get("index", True)  # index=False
