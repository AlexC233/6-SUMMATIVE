import json
import os
from Body import Body

relPath = os.path.dirname(__file__)


def startSettings():
    """Load the settings file and return the settings"""
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


def saveSimulation(fileName, runtime, frames, videoFolder):
    """Save the simulation to a file
    fileName: name of the file to save to
    runtime: the runtime of the simulation
    frames: the number of frames in the simulation
    videoFolder: the folder of the video"""
    # check if fileName ends with .json
    if not fileName.endswith(".json"):
        fileName += ".json"

    if os.path.exists("simulations/"):
        simulation = {}
        simulation["runtime"] = runtime
        simulation["bodies"] = Body.getObjects()
        # If certain parameters are provided, they will be stored as well
        if frames != None:
            simulation["frames"] = frames
        if videoFolder != None:
            simulation["video"] = videoFolder

        with open(
            fileName, "w"
        ) as f:
            json.dump(simulation, f, indent=4)
    else:
        # If the simulations folder does not exist, it will be created
        os.mkdir(relPath + "/simulations/")
        saveSimulation(fileName, runtime)


def loadSimulation(fileName):
    """Load the simulation from a file
    fileName: name of the file to load from"""
    with open(fileName, "r") as f:
        simulation = json.load(f)
    Body.setObjects(simulation["bodies"])

    # check if the "video" key exists, and if it does, information regarding the video will be loaded
    if "video" in simulation:
        return simulation["runtime"], simulation["video"], simulation["frames"]

    # Otherwise, only the runtime will be returned
    return simulation["runtime"]


def saveVideo(fileName, JSON):
    """Save the video to a file
    fileName: name of the file to save to
    JSON: the JSON file to save"""
    # check if fileName ends with .json
    if not JSON.endswith(".json"):
        JSON += ".json"

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
