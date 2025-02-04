import cv2
import os

from cv2 import VideoWriter_fourcc


def makeVideo(path):
    """Creates a mp4 video at the given path at 15 frames per second
    path: path to the video"""

    # Code modified from https://stackoverflow.com/a/44948030
    video_name = path + ".mp4"

    images = os.listdir(path)

    if images != []:
        # sort the images in increasing numerical order
        images.sort(key=lambda x: int(x.split(".")[0]))

        # Ensures that the files end with .png
        images = [img for img in images if img.endswith(".png")]
        frame = cv2.imread(os.path.join(path, images[0]))
        height, width, layers = frame.shape

        #cv2.VideoWriter(output_filename, fourcc, fps, self._window_shape)
        video = cv2.VideoWriter(
            video_name, VideoWriter_fourcc(*'mp4v'), 15, (width, height))

        for image in images:
            video.write(cv2.imread(os.path.join(path, image)))

        cv2.destroyAllWindows()
        video.release()
