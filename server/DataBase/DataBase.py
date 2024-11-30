import pickle
import os
from .Car import Car


def read_db() -> list[Car]:
    if not os.path.exists("cars"):
        with open("cars", "wb"):
            pass
        return []
    if os.path.getsize("cars") == 0:
        return []
    with open("cars", "rb") as f:
        return pickle.loads(f.read())

def write_to_db(car:Car):
    db = read_db()
    for db_car in db:
        if db_car.number == car.number:
            db.remove(db_car)
    db.append(car)
    with open("cars", "wb") as f:
        f.write(pickle.dumps(db))

