# flake8: noqa: E402
import os
import sys
from datetime import timedelta
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

# --- Añadir src al path antes de cualquier otro import ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# --- Resto de imports ---
from basic_lap_time import load_driver_laps, time_delta_to_str, validate_fast_f1_Request

# ---------- TESTS PARA time_delta_to_str ----------


def test_time_delta_to_str_normal_case():
    td = timedelta(minutes=1, seconds=19, microseconds=104000)
    result = time_delta_to_str(td)
    assert result == "1:19:104"


def test_time_delta_to_str_zero_time():
    td = timedelta(0)
    result = time_delta_to_str(td)
    assert result == "0:00:000"


def test_time_delta_to_str_none():
    result = time_delta_to_str(None)
    assert result is None


# ---------- TESTS PARA validate_fast_f1_Request ----------


def test_validate_fast_f1_request_valid():
    validate_fast_f1_Request(2020, "Spain", "FP1", "VER")


def test_validate_fast_f1_request_missing_param():
    with pytest.raises(Exception, match="Parameters must be filled"):
        validate_fast_f1_Request(None, "Spain", "FP1", "VER")


def test_validate_fast_f1_request_invalid_year():
    with pytest.raises(Exception, match="Api not supports values under 1950"):
        validate_fast_f1_Request(1949, "Spain", "FP1", "VER")


# ---------- TESTS PARA load_driver_laps ----------


@patch("basic_lap_time.fastf1.get_session")
@patch("basic_lap_time.pd.DataFrame.to_csv")
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
