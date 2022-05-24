import cv2
import os

from cv2 import VideoWriter_fourcc


def makeVideo(path):
    video_name = path + ".mp4"

    images = os.listdir(path)
    # sort the images in increasing numerical order
    images.sort(key=lambda x: int(x.split(".")[0]))

    images = [img for img in images if img.endswith(".png")]
    frame = cv2.imread(os.path.join(path, images[0]))
    height, width, layers = frame.shape

    #cv2.VideoWriter(output_filename, fourcc, fps, self._window_shape)
    video = cv2.VideoWriter(
        video_name, VideoWriter_fourcc(*'mp4v'), 10, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(path, image)))

    cv2.destroyAllWindows()
    video.release()


if __name__ == "__main__":
    makeVideo('D:/Desktop/CS/11 CS/6 SUMMATIVE/videos/videoTest')
