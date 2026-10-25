def collision_warning(objects):

    for obj in objects:

        width = obj["x2"] - obj["x1"]

        # Large bounding box = object is close
        if width > 300:
            return "WARNING: COLLISION RISK"

    return "SAFE"