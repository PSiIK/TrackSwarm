from nvidialibs.jetcam.csi_camera import CSICamera
import cv2 as cv
import numpy as np

cam = CSICamera(width=1280,height=720)

CB_W, CB_H = 6, 5

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((CB_W*CB_H,3), np.float32)
objp[:,:2] = np.mgrid[0:CB_H,0:CB_W].T.reshape(-1,2)

objpoints = []
imgpoints = []

try:
  while len(imgpoints) < 160:
    frame = cam.read()
    grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    greys = cv.resize(grey, None, fx=0.25, fy=0.25)

    ret, corners = cv.findChessboardCorners(greys, (CB_H, CB_W), None, flags=cv.CALIB_CB_ADAPTIVE_THRESH|cv.CALIB_CB_NORMALIZE_IMAGE|cv.CALIB_CB_ACCURACY)

    if ret == True:
        objpoints.append(objp)
        corners *= 4
        
        corners2 = cv.cornerSubPix(grey, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)
 
        # Draw and display the corners
        cv.drawChessboardCorners(frame, (CB_H, CB_W), corners2, ret)
    cv.imshow('Cam', frame)
    if cv.waitKey(1) & 0xFF in (27, ord('q')):
      break
except KeyboardInterrupt:
  ...

ret = cv.calibrateCamera(objpoints, imgpoints, grey.shape[::-1], None, None, flags=cv.CALIB_USE_LU)

if ret[0]:
  print(ret)
