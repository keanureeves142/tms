from datetime import timedelta

def adjust_end_time(end_time):
    """
    Adjusts the end time if it falls within a restricted zone (7 AM to 9 PM).
    Pushes the end time to the next available 9 PM if within the restricted zone.
    """
    if 7 <= end_time.hour < 21:
        # Push end time to the next 9 PM
        end_time = end_time.replace(hour=21, minute=0, second=0, microsecond=0)
    return end_time
