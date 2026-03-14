import os
import sys
import time
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pipeline import run_pipeline

INPUT_FOLDER = "incoming_data"
OUTPUT_FOLDER = "processed_data"

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def process_file(file_path):

    df = run_pipeline(file_path)

    df["week"] = df["timestamp"].dt.to_period("W").apply(lambda r: r.start_time)

    for week, group in df.groupby("week"):

        week_str = week.strftime("%Y-%m-%d")

        output_file = os.path.join(
            OUTPUT_FOLDER,
            f"processed_week_{week_str}.csv"
        )

        group.to_csv(output_file, index=False)


def watch_folder():

    processed = set()

    while True:

        for file in os.listdir(INPUT_FOLDER):

            if file.endswith(".csv"):

                path = os.path.join(INPUT_FOLDER, file)

                if path not in processed:

                    process_file(path)
                    processed.add(path)

        time.sleep(5)


if __name__ == "__main__":
    watch_folder()