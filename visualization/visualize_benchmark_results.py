import os
import csv
from dataclasses import dataclass
from typing import List, Dict, Optional

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = "data_output/grl"


@dataclass
class RunRecord:
    path: str
    tag: str
    date: str
    kind: str  # train or test
    strategy: str  # normal or cond
    avg_tr_quota_mean: Optional[float]
    trips_served: Optional[int]
    total_saved_time_s: Optional[float]
    avg_saved_time_s: Optional[float]


def _find_run_dirs() -> List[str]:
    found = []
    # We expect new compact structure like grl/<daytype?>/<qt|full>/<tag>
    for root, dirs, files in os.walk(BASE_DIR):
        # A run dir must contain a 'data' subfolder
        if "data" in dirs:
            found.append(root)
    return found


def _parse_meta_from_path(path: str) -> Dict[str, str]:
    # Example: data_output/grl/weekday/qt/benchmark_cond_test_2023-07-10
    parts = path.split(os.sep)
    meta = {"strategy": "normal", "kind": "train", "date": ""}
    try:
        tag = parts[-1]
        meta["tag"] = tag
        meta["kind"] = "test" if "test" in tag else "train"
        meta["strategy"] = "cond" if "cond" in tag else "normal"
        meta["date"] = tag.split("_")[-1]
    except Exception:
        meta["tag"] = parts[-1]
    return meta


def _read_avg_time_reduction_quota(run_dir: str, date: str) -> Optional[float]:
    csv_file = os.path.join(run_dir, "data", f"average_time_reduction{date}.csv")
    if not os.path.isfile(csv_file):
        return None
    vals = []
    with open(csv_file, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                vals.append(float(row["quota_of_saved_time_for_all_served_orders"]))
            except Exception:
                pass
    if not vals:
        return None
    return sum(vals) / len(vals)


def _read_trips_served(run_dir: str, date: str) -> Optional[int]:
    csv_file = os.path.join(run_dir, "data", f"tripdata{date}.csv")
    if not os.path.isfile(csv_file):
        return None
    # Count rows (excluding header)
    with open(csv_file, mode="r") as f:
        return sum(1 for _ in f) - 1


def _read_saved_time_stats(run_dir: str, date: str) -> tuple[Optional[float], Optional[float]]:
    csv_file = os.path.join(run_dir, "data", f"tripdata{date}.csv")
    if not os.path.isfile(csv_file):
        return None, None
    total = 0.0
    n = 0
    with open(csv_file, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                tr = float(row["time_reduction"])  # seconds
                total += tr
                n += 1
            except Exception:
                pass
    if n == 0:
        return 0.0, None
    return total, total / n


def collect_results() -> pd.DataFrame:
    rows: List[RunRecord] = []
    for run_dir in _find_run_dirs():
        meta = _parse_meta_from_path(run_dir)
        date = meta.get("date", "")
        tag = meta.get("tag", os.path.basename(run_dir))
        ar_mean = _read_avg_time_reduction_quota(run_dir, date)
        served = _read_trips_served(run_dir, date)
        total_saved, avg_saved = _read_saved_time_stats(run_dir, date)
        rows.append(
            RunRecord(
                path=run_dir,
                tag=tag,
                date=date,
                kind=meta.get("kind", ""),
                strategy=meta.get("strategy", ""),
                avg_tr_quota_mean=ar_mean,
                trips_served=served,
                total_saved_time_s=total_saved,
                avg_saved_time_s=avg_saved,
            )
        )
    df = pd.DataFrame([r.__dict__ for r in rows])
    return df


def plot_results(df: pd.DataFrame, out_dir: str = "figures") -> None:
    os.makedirs(out_dir, exist_ok=True)
    # Filter test runs
    tdf = df[df["kind"] == "test"].copy()
    # Bar plot: average of avg_tr_quota_mean per strategy
    agg = (
        tdf.groupby("strategy")["avg_tr_quota_mean"].mean().reset_index()
    )
    plt.figure(figsize=(6, 4))
    sns.barplot(data=agg, x="strategy", y="avg_tr_quota_mean")
    plt.title("Mean average_time_reduction quota (test days)")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "benchmark_quota_mean.png"))
    plt.close()

    # Bar plot: trips served per strategy (sum across test days)
    agg_served = (
        tdf.groupby("strategy")["trips_served"].sum().reset_index()
    )
    plt.figure(figsize=(6, 4))
    sns.barplot(data=agg_served, x="strategy", y="trips_served")
    plt.title("Trips served (sum over test days)")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "benchmark_trips_served.png"))
    plt.close()

    # Bar plot: total saved time per strategy (sum seconds across test days)
    agg_saved = (
        tdf.groupby("strategy")["total_saved_time_s"].sum().reset_index()
    )
    plt.figure(figsize=(6, 4))
    sns.barplot(data=agg_saved, x="strategy", y="total_saved_time_s")
    plt.title("Total saved time (seconds, sum over test days)")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "benchmark_total_saved_time.png"))
    plt.close()

    # Table: show each test day’s metrics
    cols = [
        "tag",
        "date",
        "strategy",
        "avg_tr_quota_mean",
        "trips_served",
        "total_saved_time_s",
        "avg_saved_time_s",
    ]
    tdf[cols].to_csv(os.path.join(out_dir, "benchmark_test_runs.csv"), index=False)


if __name__ == "__main__":
    df = collect_results()
    print(df.sort_values(["kind", "strategy", "date"]))
    plot_results(df)
