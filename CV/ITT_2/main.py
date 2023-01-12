import cv2 as cv
import numpy as np
# oh word

def main():
    # Define the camera ports for the stereo vission
    camport1 = 1
    camport2 = 2

    cam_right = cv.VideoCapture(camport1)
    cam_left = cv.VideoCapture(camport2)
    _, img1 = cam_right.read()
    _, img2 = cam_left.read()
    width, height = img1.shape[1], img1.shape[0]


    while True:
        _, img1 = cam_right.read()
        print(width, height)
        cv.imshow("Image 1",img1)
        cv.waitKey(0)



if __name__ == "__main__":
    main()