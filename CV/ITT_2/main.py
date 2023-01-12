import cv2 as cv
import numpy as np
# oh word

def main():
    # Define the camera ports for the stereo vission
    camport1 = 1
    camport2 = 2

    cam1 = cv.VideoCapture(camport1)
    cam2 = cv.VideoCapture(camport2)
    _, img1 = cam1.read()
    _, img2 = cam2.read()
    width, height = img1.shape[1], img1.shape[0]


    while True:
        _, img1 = cam1.read()
        print(width, height)
        cv.imshow("Image 1",img1)
        cv.waitKey(0)



if __name__ == "__main__":
    main()