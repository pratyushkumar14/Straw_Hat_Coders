def calculate_confidence(df, view):
    n = len(df)

    if view == "daily":
        return "High" if n >= 7 else "Medium" if n >= 3 else "Low"

    if view == "weekly":
        return "High" if n >= 4 else "Medium" if n >= 2 else "Low"

    if view == "yearly":
        return "High" if n >= 12 else "Medium" if n >= 6 else "Low"

    return "Low"
