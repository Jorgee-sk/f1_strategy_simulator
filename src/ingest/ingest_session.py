import os
import argparse
import fastf1
from src.utils.date_utils import time_delta_to_str


def ingest_session(
    year: int,
    grand_prix: str,
    session: str,
    output_dir: str = "../f1_strategy_simulator/src/data/",
):
    """
    Ingiere datos de una sesión completa de F1 usando FastF1.
    Devuelve un DataFrame con laps y features clave, y guarda en CSV.
    """
    if not all([year, grand_prix, session]):
        raise ValueError("Todos los parámetros son requeridos.")
    if year < 1950:
        raise ValueError("FastF1 no soporta años antes de 1950.")

    # Cargar sesión
    sess = fastf1.get_session(year, grand_prix, session)
    sess.load()  # Carga laps, telemetría, etc.

    # Extraer laps con features clave
    laps = sess.laps[
        [
            "Driver",
            "Team",
            "LapNumber",
            "LapTime",
            "Sector1Time",
            "Sector2Time",
            "Sector3Time",
            "Compound",
            "TyreLife",
            "TrackStatus",
            "SpeedI1",
            "SpeedI2",
            "SpeedFL",
            "SpeedST",
            "Position",
            "IsPersonalBest",
        ]
    ].copy()

    # Convertir tiempos a timedelta para consistencia (opcional, pero útil para cálculos)
    time_cols = ["LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]
    for col in time_cols:
        laps[col] = laps[col].apply(time_delta_to_str)

    # Guardar en CSV
    os.makedirs(output_dir, exist_ok=True)
    file_name = f"{year}_{grand_prix}_{session}_laps.csv"
    laps.to_csv(os.path.join(output_dir, file_name), index=False)
    print(f"Datos ingestados y guardados en {output_dir}{file_name}")

    return laps


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingiere datos de sesión F1.")
    parser.add_argument("--year", required=True, type=int, help="Year (ex. 2023)")
    parser.add_argument("--gp", required=True, type=str, help="Grand Prix (ex. Spain)")
    parser.add_argument("--session", required=True, type=str, help="Session (ex. FP3)")
    args = parser.parse_args()

    ingest_session(args.year, args.gp, args.session)
