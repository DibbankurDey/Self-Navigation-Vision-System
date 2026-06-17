from Planning.decision_engine import make_decision

objects = [
    {
        "class": "car",
        "x1": 300,
        "x2": 500
    }
]

decision = make_decision(objects, 1280)

print(decision)