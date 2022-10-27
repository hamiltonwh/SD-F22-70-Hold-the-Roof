import cv2 as cv
import numpy as np
import math


def Rx(theta):
    RxM = np.array([[1, 0, 0],
                    [0, np.cos(math.radians(theta)), -np.sin(math.radians(theta))],
                    [0, np.sin(math.radians(theta)), np.cos(math.radians(theta))]])
    return RxM


def Ry(theta):
    RyM = np.array([[np.cos(math.radians(theta)), 0, np.sin(math.radians(theta))],
                    [0, 1, 0],
                    [-np.sin(math.radians(theta)), 0, np.cos(math.radians(theta))]])
    return RyM


def Rz(theta):
    RzM = np.array([[np.cos(math.radians(theta)), -np.sin(math.radians(theta)), 0],
                    [np.sin(math.radians(theta)), np.cos(math.radians(theta)), 0],
                    [0, 0, 1]])
    return RzM


def main():
    cam_port = 0
    cam = cv.VideoCapture(cam_port)
    arucoDict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)

    result, image = cam.read()

    h = image.shape[0]
    w = image.shape[1]

    # fx = 1200
    fx = 1600
    fy = fx

    cx = fx / 2
    cy = fy / 2

    K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]]).astype(np.float32)

    points = np.array([[0, -0.5, -0.5, 0.5, 0.5],
                       [0, 0.5, -0.5, 0.5, -0.5],
                       [0, -3, -3, -3, -3],
                       [1, 1, 1, 1, 1]])

    marker3 = np.array([[-0.875], [2.125], [-1.25]])
    marker4 = np.array([[2.15], [2.25], [-1.55]])

    marker6 = np.array([[0.2],[5],[1.25]])

    # refineDetectMarkers()

    new_video = cv.VideoWriter('Test3.wmv', cv.VideoWriter_fourcc('W','M','V','2'), 30, (w, h))
    frame_count = 0

    # while (frame_count <= 500):
    while True:
        _, org_frame = cam.read()

        corners, ids, _ = cv.aruco.detectMarkers(image=org_frame, dictionary=arucoDict)
        # print(corners)



        if ids is not None:
        # if not ids == None:
        #     if frame_count > 0:
        #         ids_prev = ids[0][0]

            cv.aruco.drawDetectedMarkers(image=org_frame, corners=corners, ids=ids, borderColor=(100, 200, 255))
            # cv.putText(org_frame, "CURRENT ID: " + str(ids[0][0]), (10, 465), 1, 1, (0, 0, 255))

            rvecs, tvecs, _ = cv.aruco.estimatePoseSingleMarkers(corners=corners, markerLength=1.25, cameraMatrix=K,
                                                                 distCoeffs=0)
            # print(ids,rvecs,tvecs)
            rvec_m_c = rvecs[0]
            t_mc = tvecs[0][0]

            # if rvecs[0]

            # print("ID: ", ids[0][0])
            # print("CORN: ", corners[0][0])
            count = 0

            for line in corners[0][0]:
                # print(count, ": ", line)
                count += 1

            # print("RV: ", rvecs)
            # print("TV: ", t_mc)

            cv.drawFrameAxes(org_frame, cameraMatrix=K, distCoeffs=0, rvec=rvec_m_c, tvec=t_mc, length=2, thickness=4)

            R, _ = cv.Rodrigues(rvec_m_c)

            R_cm = R

            t_mc = np.array([t_mc])
            H_cm = np.block([[R_cm, t_mc.T], [0, 0, 0, 1]])


            Kn = np.array([[fx, 0, cx, 0],
                           [0, fy, cy, 0],
                           [0, 0, 1, 0]]).astype(np.float32)

            if ids[0][0] == 3:
                theta = 90
                R = Rx(theta)
                t = marker3

            elif ids[0][0] == 4:
                theta = 90
                R = Rx(theta)
                t = marker4


            elif ids[0][0] == 6:
                theta = -180
                R = Rx(theta)
                t = marker6

            H_mb = np.block([[R, t], [0, 0, 0, 1]])
            H_cb = H_cm @ H_mb

            tvec_cb = np.array([[H_cb[0][3]], [H_cb[1][3]], [H_cb[2][3]]])

            dist1 = H_cb[2][3]/2.54 # inches
            dist2 = t_mc[0][2]/2.54 # inches


            newpoints = []


            for i in range(5):
                p = Kn @ H_cb @ points[:, i]
                p = p / p[2]

                newpoints.append(p)

            point4 = tuple([int(newpoints[0][0]), int(newpoints[0][1])])
            point1 = tuple([int(newpoints[1][0]), int(newpoints[1][1])])
            point2 = tuple([int(newpoints[2][0]), int(newpoints[2][1])])
            point0 = tuple([int(newpoints[3][0]), int(newpoints[3][1])])
            point3 = tuple([int(newpoints[4][0]), int(newpoints[4][1])])

            cv.line(org_frame, pt1=point0, pt2=point1, color=(0, 0, 255), thickness=1)
            cv.line(org_frame, pt1=point1, pt2=point2, color=(0, 0, 255), thickness=1)
            cv.line(org_frame, pt1=point2, pt2=point3, color=(0, 0, 255), thickness=1)
            cv.line(org_frame, pt1=point3, pt2=point0, color=(0, 0, 255), thickness=1)
            cv.line(org_frame, pt1=point0, pt2=point4, color=(0, 0, 255), thickness=1)
            cv.line(org_frame, pt1=point1, pt2=point4, color=(0, 0, 255), thickness=1)
            cv.line(org_frame, pt1=point2, pt2=point4, color=(0, 0, 255), thickness=1)
            cv.line(org_frame, pt1=point3, pt2=point4, color=(0, 0, 255), thickness=1)

            cv.aruco.drawDetectedMarkers(image=org_frame, corners=corners, ids=ids, borderColor=(200, 200, 255))
            cv.putText(org_frame, "CURRENT IDS: " + str(ids[0][0]), (10, 465), 1, 1, (0, 0, 255))
            cv.putText(org_frame, "Distance Marker to Cam: " + str(np.round(dist2,2)), (10, 435), 1, 1, (0, 0, 255))
            cv.putText(org_frame, "Distance Obj to Cam: " + str(np.round(dist1,2)), (10,395), 1, 1, (0,0,255))

        else:
            cv.putText(org_frame, "NO ID FOUND", (10, 465), 1, 1, (0, 0, 255))

        frame_count += 1
        cv.imshow("Cam", org_frame)

        new_video.write(org_frame)

        cv.waitKey(10)

    else:
        print("No image detected. Please! try again")
    new_video.release()
    cam.release()


if __name__ == "__main__":
    main()
