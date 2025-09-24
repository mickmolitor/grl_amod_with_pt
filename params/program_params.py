from datetime import datetime
from enum import Enum
from program.interval.time import Time

class Mode(Enum):
    GRAPH_REINFORCEMENT_LEARNING = "grl"
    # Just solve the optimization problem without knowing state values
    BASELINE_PERFORMANCE = "bl"
    Q_LEARNING = "rl"
    DEEP_Q_LEARNING = "drl"

class DataSet(Enum):
    YELLOW_CAB = "yellow_cab"
    FOR_HIRE = "for_hire"

class ProgramParams:

    ######################################################################################################
    ############### Execution specific ###############
    EXECUTION_MODE = None

    SIMULATION_DATE = datetime(2023, 7, 10)

    # Toggle for using day-type-specific (weekday/weekend) weight files for GRL
    CONDITIONAL_WEIGHTS = False

    # Optional label appended to data output path to separate runs (e.g., benchmark tags)
    OUTPUT_TAG: str | None = None

    # Quick-test mode: reduce vehicles and orders for faster runs
    QUICK_TEST = True
    QUICK_TEST_VEHICLES = 100
    QUICK_TEST_ORDER_SAMPLING_RATE = 0.1  # 10%

    # Training switch: disable weight updates during evaluation runs
    TRAINING_ENABLED = True

    DATA_SET = DataSet.FOR_HIRE


    ######################################################################################################
    ############### Hyperparameters ###############
    DISCOUNT_RATE = 0.95
    LS = 60
    def DISCOUNT_FACTOR(duration_in_seconds: int) -> float:

        return ProgramParams.DISCOUNT_RATE ** (duration_in_seconds / ProgramParams.LS)

    LEARNING_RATE = 0.01


    ######################################################################################################
    ############### Operational parameters ###############

    IDLING_COST = 5

    AMOUNT_OF_VEHICLES = 100

    # Radius for relocation in meters
    RELOCATION_RADIUS = 10000

    # How much direct trips should be discounted in the optimization
    DIRECT_TRIP_DISCOUNT_FACTOR = 0.5

    # Time the vehicle needs to idle until it can relocate
    MAX_IDLING_TIME = 300

    ######################################################################################################
    ############### Deep Reinforcement Learning ###############

    # Number of iterations until the weights of main net are copied to target net
    MAIN_AND_TARGET_NET_SYNC_ITERATIONS = 60


    ######################################################################################################
    ############### Other environment values which are static ###############



    # Minimal trip time for routes to be eligible for combined routes in seconds
    L1 = 0

    # Maximum difference between route without vehicles time and route with vehicles time in seconds
    L2 = 1800
    
    GRID_INTERVAL_UPDATE_RATE = 1800
    

    ##########################################################################################################
    ############### Inilization of the public transport network ###############
    STATION_DURATION = 80  # Fahrzeit für eine Station
    TRANSFER_SAME_STATION = 300  # Setzen Sie hier den Wert für Umsteige_selbe_Station
    MAX_WALKING_DURATION = 600


    ######################################################################################################
    ############### Fix environment variables ###############
    # File paths to orders
    def ORDERS_FILE_PATH() :
        return f"data/{ProgramParams.DATA_SET.value}/orders_{ProgramParams.SIMULATION_DATE.strftime('%Y-%m-%d')}.csv"
    
    # Time it takes until the simulation updates in seconds
    SIMULATION_UPDATE_RATE = 60 #FIX

    # Medium waiting time
    def PUBLIC_TRANSPORT_WAITING_TIME(time: Time):
        rush_hours_morning = Time(6, 30, 0)
        middays = Time(9, 30, 0)
        rush_hours_afternoon = Time(15, 30, 0)
        evenings = Time(20, 0, 0)

        if time.is_before(rush_hours_morning):
            return 600  # late nights waiting duration
        if time.is_before(middays):
            return 150  # rush hours morning waiting duration
        if time.is_before(rush_hours_afternoon):
            return 300  # middays waiting duration
        if time.is_before(evenings):
            return 150  # rush hours afternoon waiting duration
        return 450  # evenings waiting duration
        # Source: https://www.introducingnewyork.com/subway
        # https://www.humiliationstudies.org/documents/NYsubwaymap.pdf
    
    # Time it takes for customers to enter or leave the public transport system in seconds
    PUBLIC_TRANSPORT_ENTRY_EXIT_TIME = 120  
    
    # Static vehicle speed in m/s -> assume these small busses driving in Berlin
    VEHICLE_SPEED = 6.33

    # Static walking speed in m/s
    WALKING_SPEED = 1

    # If algorithm should do relocation
    def FEATURE_RELOCATION_ENABLED() -> bool:
        return ProgramParams.EXECUTION_MODE == Mode.GRAPH_REINFORCEMENT_LEARNING
    
    # Pick-up distance threshold (how far away a vehicle consider new orders) in meter
    # Equal to 5 minutes
    PICK_UP_DISTANCE_THRESHOLD = 1900  # 950 meters in Feng et al. (2022)

    # Duration how long orders can be matched with vehicles in seconds
    ORDER_EXPIRY_DURATION = 120

    def DATA_OUTPUT_FILE_PATH() -> str:
        mode = ProgramParams.EXECUTION_MODE.value
        # In the front since it was added later
        mit = "_" if ProgramParams.MAX_IDLING_TIME == 300 else ProgramParams.MAX_IDLING_TIME
        dr = "_" if ProgramParams.DISCOUNT_RATE == 0.95 else ProgramParams.DISCOUNT_RATE
        ls = "_" if ProgramParams.LS == 60 else ProgramParams.LS
        lr = "_" if ProgramParams.LEARNING_RATE == 0.01 else ProgramParams.LEARNING_RATE
        idling_cost = "_" if ProgramParams.IDLING_COST == 5 else ProgramParams.IDLING_COST
        aov = "_" if ProgramParams.AMOUNT_OF_VEHICLES == 2000 else ProgramParams.AMOUNT_OF_VEHICLES
        re_radius = "_" if ProgramParams.RELOCATION_RADIUS == 10000 else ProgramParams.RELOCATION_RADIUS
        direct_discount = "_" if ProgramParams.DIRECT_TRIP_DISCOUNT_FACTOR == 0.5 else ProgramParams.DIRECT_TRIP_DISCOUNT_FACTOR
        main_target_sync = "_" if ProgramParams.MAIN_AND_TARGET_NET_SYNC_ITERATIONS == 60 else ProgramParams.MAIN_AND_TARGET_NET_SYNC_ITERATIONS
        base = f"{mode}/{mit}/{dr}/{ls}/{lr}/{idling_cost}/{aov}/{re_radius}/{direct_discount}/{main_target_sync}"
        # Append optional output tag to keep runs separate
        if ProgramParams.OUTPUT_TAG:
            base = f"{base}/{ProgramParams.OUTPUT_TAG}"
        return base

    # Helpers for day type
    def IS_WEEKEND() -> bool:
        # Monday=0 ... Sunday=6
        return ProgramParams.SIMULATION_DATE.weekday() >= 5

    def DAY_TYPE_DIR() -> str:
        return "weekend" if ProgramParams.IS_WEEKEND() else "weekday"

    def set_member(member: str, value):
        if member == "EXECUTION_MODE":
            ProgramParams.EXECUTION_MODE = Mode(value)
        elif member == "MAX_IDLING_TIME":
            ProgramParams.MAX_IDLING_TIME = int(value)
        elif member == "DISCOUNT_RATE":
            ProgramParams.DISCOUNT_RATE = float(value)
        elif member == "LS":
            ProgramParams.LS = float(value)
        elif member == "LEARNING_RATE":
            ProgramParams.LEARNING_RATE = float(value)
        elif member == "IDLING_COST":
            ProgramParams.IDLING_COST = float(value)
        elif member == "AMOUNT_OF_VEHICLES":
            ProgramParams.AMOUNT_OF_VEHICLES = int(value)
        elif member == "RELOCATION_RADIUS":
            ProgramParams.RELOCATION_RADIUS = int(value)
        elif member == "DIRECT_TRIP_DISCOUNT_FACTOR":
            ProgramParams.DIRECT_TRIP_DISCOUNT_FACTOR = float(value)
        elif member == "MAIN_AND_TARGET_NET_SYNC_ITERATIONS":
            ProgramParams.MAIN_AND_TARGET_NET_SYNC_ITERATIONS = int(value)
        elif member == "CONDITIONAL_WEIGHTS":
            ProgramParams.CONDITIONAL_WEIGHTS = bool(value)
        elif member == "QUICK_TEST":
            ProgramParams.QUICK_TEST = bool(value)
        elif member == "QUICK_TEST_VEHICLES":
            ProgramParams.QUICK_TEST_VEHICLES = int(value)
        elif member == "QUICK_TEST_ORDER_SAMPLING_RATE":
            ProgramParams.QUICK_TEST_ORDER_SAMPLING_RATE = float(value)
        elif member == "TRAINING_ENABLED":
            ProgramParams.TRAINING_ENABLED = bool(value)
        else:
            raise Exception(f"No parameter found with name {member}")