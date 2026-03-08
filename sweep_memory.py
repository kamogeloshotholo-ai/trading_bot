from datetime import datetime


# Store sweeps detected today
sweep_memory = {}

current_day = datetime.now().day


def reset_sweep_memory():

    global sweep_memory
    global current_day

    now = datetime.now()

    if now.day != current_day:

        sweep_memory = {}
        current_day = now.day

        print("Sweep memory reset for new day")


def sweep_already_detected(symbol):

    if symbol in sweep_memory:
        return True

    return False


def store_sweep(symbol, sweep_info):
    """Remember a sweep setup so it isn't processed again during the day.

    The memory only needs to flag that a sweep occurred; additional data may
    be stored for debugging or further analysis.
    """

    sweep_memory[symbol] = sweep_info

    print(symbol, "sweep stored in memory:", sweep_info)