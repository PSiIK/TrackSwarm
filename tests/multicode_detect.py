from nvidialibs.jetcam.csi_camera import CSICamera
import cv2 as cv
import cv2.aruco as aruco

dicts = [aruco.getPredefinedDictionary(predef) for predef in 
               (aruco.DICT_4X4_100, aruco.DICT_4X4_250, aruco.DICT_5X5_100,
                aruco.DICT_5X5_250, aruco.DICT_6X6_250, aruco.DICT_7X7_250,
                aruco.DICT_APRILTAG_25H9, aruco.DICT_APRILTAG_36H11)]

detector = aruco.ArucoDetector(dicts)

cam = CSICamera(fps=29, capture_width=1920, capture_height=1080, width=1280, height=720)

while not (cv.waitKey(10) & 0xff in (27, ord('q'))):
  img = cam.read()
  cor, ids, *_ = detector.detectMarkersMultiDict(img)
  aruco.drawDetectedMarkers(img, cor, ids)
  cv.imshow("cam", img)
