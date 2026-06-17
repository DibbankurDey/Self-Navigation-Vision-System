def make_decision(objects, image_width):

    center_x = image_width // 2

    for obj in objects:

        object_center = (obj["x1"] + obj["x2"]) // 2

        if abs(object_center - center_x) < 150:
            return "STOP"

        elif object_center < center_x:
            return "MOVE RIGHT"

        else:
            return "MOVE LEFT"

    return "MOVE FORWARD"