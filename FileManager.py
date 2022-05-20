import json
import os
from Body import Body

def startSettings():
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            settings = json.load(f)
    else:
        settings = {}
        settings["step"] = 5
        settings["xlim"] = [0, 1e10]
        settings["ylim"] = [0, 1e10]
        settings["objects"] = 500
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4)

    return (
        settings["interval"],
        settings["step"],
        settings["xlim"],
        settings["ylim"],
        settings["objects"],
    )


def saveSimulation(fileName, runtime):
    simulation = {}
    simulation["runtime"] = runtime
    simulation["bodies"] = Body.getObjects()
    with open(
        os.path.dirname(__file__) + "/simulations/" + fileName + ".json", "w"
    ) as f:
        json.dump(simulation, f, indent=4)
