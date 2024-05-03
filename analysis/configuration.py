from params.program_params import Mode, ProgramParams

# Run this to set the parameters for analysis
def set_params():
    # Set program params
    ProgramParams.EXECUTION_MODE = Mode.GRAPH_REINFORCEMENT_LEARNING
    ProgramParams.DISCOUNT_RATE = 0.95
    ProgramParams.LS = 60
    ProgramParams.LEARNING_RATE = 0.01
    ProgramParams.IDLING_COST = 5
    ProgramParams.AMOUNT_OF_VEHICLES = 2000
    ProgramParams.RELOCATION_RADIUS = 10000
    ProgramParams.MAIN_AND_TARGET_NET_SYNC_ITERATIONS = 60