import json
import os
from Body import Body

relPath = os.path.dirname(__file__)

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

def saveSimulation(fileName, runtime, frames):

    # check if fileName ends with .json
    if not fileName.endswith(".json"):
        fileName += ".json"

    if os.path.exists("simulations/"):
        simulation = {}
        simulation["runtime"] = runtime
        simulation["bodies"] = Body.getObjects()
        if frames != None:
            simulation["frames"] = frames
        with open(
            fileName, "w"
        ) as f:
            json.dump(simulation, f, indent=4)
    else:
        os.mkdir(relPath + "/simulations/")
        saveSimulation(fileName, runtime)

def loadSimulation(fileName):
    with open(fileName, "r") as f:
        simulation = json.load(f)
    Body.setObjects(simulation["bodies"])

    # check if the "video" key exists
    if "video" in simulation:
        return simulation["runtime"], simulation["video"]

    return simulation["runtime"]

def saveVideo(fileName, JSON):
    if os.path.exists("videos/"):
        os.mkdir(fileName)
        with open(JSON, "r") as f:
            simulation = json.load(f)

        simulation["video"] = fileName
        simulation["frames"] = 0
        with open(JSON, "w") as f:
            json.dump(simulation, f, indent=4)
    else:
        os.mkdir(relPath + "/videos/")
        saveVideo(fileName, JSON)