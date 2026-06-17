def estimate_distance(obj):

    width = obj["x2"] - obj["x1"]

    if width > 300:
        return "Near"

    elif width > 150:
        return "Medium"

    else:
        return "Far"