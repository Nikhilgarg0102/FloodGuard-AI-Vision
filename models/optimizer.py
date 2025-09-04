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

