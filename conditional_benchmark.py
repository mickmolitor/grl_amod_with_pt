import csv
import os
import shutil
from datetime import datetime

from params.program_params import ProgramParams, Mode
from program.execution import execute_graph_reinforcement_learning
from program.state.state import State
from program.order.orders import Orders
from program.vehicle.vehicles import Vehicles
from program.state.state_value_networks import StateValueNetworks


# Simple benchmark runner comparing normal vs. conditional day-type weights
# Metric: mean of DataCollector's average_time_reduction CSV across the day


def _backup_file(src: str) -> str:
    backup = f"{src}.bak"
    if os.path.exists(src):
        shutil.copyfile(src, backup)
    return backup


def _restore_file(src: str, backup: str) -> None:
    if os.path.exists(backup):
        shutil.copyfile(backup, src)
        os.remove(backup)


def _reset_singletons_memory() -> None:
    # Reset frequently mutated singletons/state
    State.reset()
    Orders.reset()
    Vehicles.raze_vehicles()
    # Reset RL state networks instance to force re-init on next run
    try:
        # Accessing a private member here intentionally to reset singleton
        StateValueNetworks._state_value_networks = None  # type: ignore[attr-defined]
    except Exception:
        pass


def _read_avg_time_reduction_mean(output_path: str, sim_date: datetime) -> float:
    csv_file = os.path.join(
        output_path,
        "data",
        f"average_time_reduction{sim_date.strftime('%Y-%m-%d')}.csv",
    )
    if not os.path.isfile(csv_file):
        return float("nan")
    values = []
    with open(csv_file, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                values.append(float(row["quota_of_saved_time_for_all_served_orders"]))
            except Exception:
                continue
    if not values:
        return float("nan")
    return sum(values) / len(values)


def _run_once(cond_weights: bool, tag: str) -> float:
    # Configure run
    ProgramParams.EXECUTION_MODE = Mode.GRAPH_REINFORCEMENT_LEARNING
    ProgramParams.CONDITIONAL_WEIGHTS = cond_weights
    ProgramParams.OUTPUT_TAG = tag

    # Keep initial vehicle positions identical across runs
    vehicles_csv = "input_data/vehicles.csv"
    backup = _backup_file(vehicles_csv)

    # Reset memory singletons
    _reset_singletons_memory()

    # Execute
    execute_graph_reinforcement_learning()

    # Read metric
    output_path = os.path.join("data_output", ProgramParams.DATA_OUTPUT_FILE_PATH())
    mean_value = _read_avg_time_reduction_mean(output_path, ProgramParams.SIMULATION_DATE)

    # Restore vehicles to initial state for next run
    _restore_file(vehicles_csv, backup)
    Vehicles.raze_vehicles()  # ensure re-read from restored file on next run

    return mean_value


if __name__ == "__main__":
    # Always run GRL in this benchmark
    ProgramParams.EXECUTION_MODE = Mode.GRAPH_REINFORCEMENT_LEARNING

    # Enable quick-test mode
    ProgramParams.QUICK_TEST = True
    ProgramParams.TRAINING_ENABLED = True

    # Choose compact training/testing set: 2 weekdays + 2 weekend days for training, then 1 weekday + 1 weekend for test
    # Adjust dates as needed to match available CSVs in data/<dataset>/
    train_days = [
        datetime(2023, 7, 3),  # Monday
        datetime(2023, 7, 4),  # Tuesday
        datetime(2023, 7, 8),  # Saturday
        datetime(2023, 7, 9),  # Sunday
    ]
    test_days = [
        datetime(2023, 7, 10),  # Monday
        datetime(2023, 7, 1),   # Saturday
    ]

    results = {}

    for cond in [False, True]:
        tag_prefix = "cond" if cond else "normal"
        ProgramParams.CONDITIONAL_WEIGHTS = cond

        # Reset networks before starting this condition's training
        StateValueNetworks._state_value_networks = None  # type: ignore[attr-defined]

        # TRAINING PHASE
        ProgramParams.TRAINING_ENABLED = True
        for d in train_days:
            ProgramParams.SIMULATION_DATE = d
            ProgramParams.OUTPUT_TAG = f"benchmark_{tag_prefix}_train_{d.strftime('%Y-%m-%d')}"
            _reset_singletons_memory()
            execute_graph_reinforcement_learning()

        # TEST PHASE
        ProgramParams.TRAINING_ENABLED = False
        means = []
        for d in test_days:
            ProgramParams.SIMULATION_DATE = d
            ProgramParams.OUTPUT_TAG = f"benchmark_{tag_prefix}_test_{d.strftime('%Y-%m-%d')}"
            _reset_singletons_memory()
            execute_graph_reinforcement_learning()
            output_path = os.path.join("data_output", ProgramParams.DATA_OUTPUT_FILE_PATH())
            means.append(_read_avg_time_reduction_mean(output_path, d))

        avg_of_means = sum([m for m in means if m == m]) / max(1, len([m for m in means if m == m]))  # exclude NaNs
        results[tag_prefix] = avg_of_means

    print("Quick-test benchmark (mean average_time_reduction quota across test days):")
    print(f"  Normal:      {results.get('normal')}")
    print(f"  Conditional: {results.get('cond')}")
    try:
        delta = results.get('cond') - results.get('normal')
        print(f"  Delta:       {delta}")
    except Exception:
        pass
