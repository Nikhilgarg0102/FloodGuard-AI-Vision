def safe_release(level, inflow):
    """
    Rule-based release optimizer
    """
    if level > 95:
        return inflow * 0.8
    elif level > 85:
        return inflow * 0.5
    elif level > 70:
        return inflow * 0.2
    else:
        return 0

# models/optimizer.py

def safe_release(current_level, predicted_inflow, max_capacity=1000, min_level=200):
    """
    Calculate safe water release.
    
    Args:
        current_level (float): Current water level in reservoir.
        predicted_inflow (float): Predicted incoming water.
        max_capacity (float): Max reservoir capacity.
        min_level (float): Minimum safe water level.

    Returns:
        release (float): Safe release amount.
    """
    # Ensure water doesn't exceed max_capacity
    release = (current_level + predicted_inflow) - max_capacity
    if release < 0:
        release = 0

    # Ensure minimum water level is maintained
    if current_level - release < min_level:
        release = current_level - min_level

    return round(release, 2)
