# flake8: noqa: E402
import os
import sys
import pytest
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from unittest.mock import patch, MagicMock
from src.utils.date_utils import time_delta_to_str
from src.ingest.ingest_session import ingest_session


@pytest.fixture
def mock_session():
    mock_sess = MagicMock()
    mock_laps = pd.DataFrame(
        {
            "Driver": ["ALO", "HAM"],
            "Team": ["McLaren", "Mercedes"],
            "LapNumber": [1, 2],
            "LapTime": [
                pd.Timedelta(minutes=1, seconds=18, milliseconds=847),
                pd.Timedelta(minutes=1, seconds=19, milliseconds=123),
            ],
            "Sector1Time": [
                pd.Timedelta(seconds=22, milliseconds=153),
                pd.Timedelta(seconds=22, milliseconds=200),
            ],
            "Sector2Time": [
                pd.Timedelta(seconds=29, milliseconds=438),
                pd.Timedelta(seconds=29, milliseconds=500),
            ],
            "Sector3Time": [
                pd.Timedelta(seconds=27, milliseconds=256),
                pd.Timedelta(seconds=27, milliseconds=300),
            ],
            "Compound": ["SUPERSOFT", "SOFT"],
            "TyreLife": [4.0, 5.0],
            "TrackStatus": [1, 1],
            "SpeedI1": [286.0, 287.0],
            "SpeedI2": [302.0, 303.0],
            "SpeedFL": [282.0, 283.0],
            "SpeedST": [312.0, 313.0],
            "Position": [np.nan, np.nan],
            "IsPersonalBest": [True, False],
        }
    )
    mock_sess.laps = mock_laps
    mock_sess.load = MagicMock()
    return mock_sess


# Test para validación de parámetros requeridos
def test_ingest_session_missing_params():
    with pytest.raises(ValueError, match="Todos los parámetros son requeridos."):
        ingest_session(0, "", "")


# Test para validación de año mínimo
def test_ingest_session_invalid_year():
    with pytest.raises(ValueError, match="FastF1 no soporta años antes de 1950."):
        ingest_session(1949, "Spain", "FP3")


@patch("fastf1.get_session")
def test_ingest_session_success(mock_get_session, mock_session, tmp_path):
    # Configura el mock para devolver la sesión mockeada
    mock_get_session.return_value = mock_session

    # Directorio temporal para output
    output_dir = str(tmp_path) + "/"

    # Llama a la función
    result = ingest_session(2018, "Spain", "FP3", output_dir=output_dir)

    # Verifica que se llamó a load()
    mock_session.load.assert_called_once()

    # Verifica que el DataFrame devuelto es el esperado
    expected_laps = mock_session.laps.copy()
    time_cols = ["LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]
    for col in time_cols:
        expected_laps[col] = expected_laps[col].apply(time_delta_to_str)

    pd.testing.assert_frame_equal(result, expected_laps)

    # Verifica que el archivo CSV se guardó correctamente
    file_name = "2018_Spain_FP3_laps.csv"
    saved_file = os.path.join(output_dir, file_name)
    assert os.path.exists(saved_file)

    # Lee el CSV guardado y compara, ignorando diferencias de dtype
    saved_df = pd.read_csv(saved_file)
    pd.testing.assert_frame_equal(
        saved_df, expected_laps.reset_index(drop=True), check_dtype=False
    )


# Test para conversión de tiempos
def test_time_conversion_applied(mock_session):
    laps = mock_session.laps.copy()

    time_cols = ["LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]
    for col in time_cols:
        laps[col] = laps[col].apply(time_delta_to_str)

    assert laps["LapTime"].iloc[0] == "1:18:847"
    assert laps["LapTime"].iloc[1] == "1:19:123"


# Test para creación de directorio si no existe
@patch("fastf1.get_session")
def test_output_dir_creation(mock_get_session, mock_session, tmp_path):
    mock_get_session.return_value = mock_session

    non_existent_dir = str(tmp_path / "new_dir") + "/"
    assert not os.path.exists(non_existent_dir)

    ingest_session(2018, "Spain", "FP3", output_dir=non_existent_dir)

    assert os.path.exists(non_existent_dir)
