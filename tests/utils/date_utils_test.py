# flake8: noqa: E402
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from datetime import timedelta
import pandas as pd

from src.utils.date_utils import time_delta_to_str

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
