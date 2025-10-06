import argparse

import fastf1
import pandas as pd


def time_delta_to_str(td):
    if pd.isna(td):
        return None
    total_seconds = int(td.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    ms = td.microseconds // 1000
    return f"{minutes}:{seconds:02d}:{ms:03d}"


def load_driver_laps(year: int, gp: str, session_name: str, driver_alias: str):

    validate_fast_f1_Request(year, gp, session_name, driver_alias)

    session = fastf1.get_session(year, gp, session_name)

    session.load()

    laps = session.laps.pick_drivers(driver_alias)
    df_laps_driver = (
        laps[["Driver", "LapTime", "LapNumber"]].reset_index().drop("index", axis=1)
    )
    df_laps_driver["LapTime"] = df_laps_driver["LapTime"].apply(time_delta_to_str)
    df_laps_driver.to_csv(
        f"../src/data/lapTimeDataTest_{driver_alias}.csv", index=False
    )


def validate_fast_f1_Request(year: int, gp: str, session_name: str, driver_alias: str):
    if gp is None or year is None or session_name is None or driver_alias is None:
        raise Exception("Parameters must be filled")
    elif year < 1950:
        raise Exception("Api not supports values under 1950")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Entry 4 parameters to get lap time")
    parser.add_argument("--year", required=True, type=int)  # 2018
    parser.add_argument("--gp", required=True, type=str)  # Spain
    parser.add_argument("--session", required=True, type=str)  # FP3
    parser.add_argument("--dalias", required=True, type=str)  # ALO

    args = parser.parse_args()

    load_driver_laps(args.year, args.gp, args.session, args.dalias)
