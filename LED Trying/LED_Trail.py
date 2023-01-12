import cv2 as cv

# Get the pattern dictionary for 4x4 markers, with ids 0 through 99.
# arucoDict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_100)
# arucoDict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_7X7_100)
arucoDict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_7X7_100)

# Optionally show all markers in the dictionary.
for id in range(0, 100):
    img = cv.aruco.drawMarker(dictionary=arucoDict, id=id, sidePixels=200)
    cv.imshow("img", img)
    cv.waitKey(0)