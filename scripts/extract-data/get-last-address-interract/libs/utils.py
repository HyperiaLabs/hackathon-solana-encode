from datetime import datetime
from tqdm import tqdm


class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # Regular colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"  # Added gray color


def log(*args, color=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = " ".join(map(str, args))

    if color:
        colored_message = f"{color}{message}{Color.RESET}"
        tqdm.write(f"[{timestamp}] {colored_message}")
    else:
        tqdm.write(f"[{timestamp}] {message}")
