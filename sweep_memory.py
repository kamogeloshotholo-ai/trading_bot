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


def store_sweep(symbol, direction):

    sweep_memory[symbol] = direction

    print(symbol, "sweep stored in memory:", direction)