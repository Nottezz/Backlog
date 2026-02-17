
def format_seconds_for_email(seconds: int) -> str:
    """
    Converts a number of seconds into a human-readable string for emails.

    Examples:
        3600  -> "1 hour"
        5400  -> "1 hour 30 min"
        2700  -> "45 min"
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    if hours > 0 and minutes == 0:
        return f"{hours} hour{'s' if hours > 1 else ''}"
    elif hours > 0 and minutes > 0:
        return f"{hours} hour{'s' if hours > 1 else ''} {minutes} min"
    else:
        return f"{minutes} min"
