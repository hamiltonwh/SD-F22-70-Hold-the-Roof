import cv2 as cv
# oh word

def main():
    camport1 = 1
    # camport2 = 2

    cam1 = cv.VideoCapture(camport1)
    _, img1 = cam1.read()
    width, height = img1.shape[1], img1.shape[0]


    while True:
        _, img1 = cam1.read()
        print(width, height)
        cv.imshow("Image 1",img1)
        cv.waitKey(0)



if __name__ == "__main__":
    main()