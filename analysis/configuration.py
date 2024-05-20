from params.program_params import Mode, ProgramParams

# Run this to set the parameters for analysis
def set_params():
    # Set program params
    ProgramParams.EXECUTION_MODE = Mode.GRAPH_REINFORCEMENT_LEARNING
    ProgramParams.MAX_IDLING_TIME = 300
    ProgramParams.DISCOUNT_RATE = 0.95
    ProgramParams.LS = 60
    ProgramParams.LEARNING_RATE = 0.01
    ProgramParams.IDLING_COST = 5
    ProgramParams.AMOUNT_OF_VEHICLES = 2000
    ProgramParams.RELOCATION_RADIUS = 10000
    ProgramParams.DIRECT_TRIP_DISCOUNT_FACTOR = 0.5
    ProgramParams.MAIN_AND_TARGET_NET_SYNC_ITERATIONS = 60

# Run this to get the parameter and its values for the comparison
def get_comparison_values() -> tuple[str, list]:
    # Change parameter here
    parameter = "IDLING_COST"
    values = [1, 3, 5, 10, 30]
    def cast(value):
        return float(value)
    return (parameter, list(map(cast, values)))