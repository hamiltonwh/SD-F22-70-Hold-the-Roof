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

    # Camera values
    UndistMatrix = np.array([[694.17008191, 0., 304.53123739],
                                 [0., 698.24565396, 195.44512563],
                                 [0., 0., 1.]])
    distCoeff = np.array([[-3.33453589e-01, -8.39226365e-02, 4.31567352e-03, 4.77064083e-04,
                               5.71389403e-01]])

    while True:
        _, img1 = cam_right.read()
        _, img2 = cam_left.read()

        img1und = cv.undistort(img1,cameraMatrix=UndistMatrix, distCoeffs=distCoeff)
        img2und = cv.undistort(img2,cameraMatrix=UndistMatrix, distCoeffs=distCoeff)

        img1und[240,:] = (0, 0, 255)
        img2und[240,:] = (0, 0, 255)

        cv.imshow("Image 1",np.hstack([img1und,img2und]))
        cv.waitKey(30)



if __name__ == "__main__":
    main()