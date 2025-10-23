import pandas as pd


def time_delta_to_str(td):
    if pd.isna(td):
        return None
    total_seconds = int(td.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    ms = td.microseconds // 1000
    return f"{minutes}:{seconds:02d}:{ms:03d}"
