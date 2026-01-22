import datetime

def get_greeting():
    """
    Determines the greeting based on the current system time.
    Returns:
        str: The greeting message (e.g., "Good Morning", "Good Afternoon", etc.)
    """
    current_hour = datetime.datetime.now().hour

    if 5 <= current_hour < 12:
        return "Good Morning"
    elif 12 <= current_hour < 17:
        return "Good Afternoon"
    elif 17 <= current_hour < 21:
        return "Good Evening"
    else:
        return "Good Night"
