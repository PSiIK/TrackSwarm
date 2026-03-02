from nvidialibs.jetcam.csi_camera import CSICamera
import cv2 as cv
import cv2.aruco as aruco
import numpy as np

detector = aruco.ArucoDetector(aruco.getPredefinedDictionary(aruco.DICT_4X4_1000))
cam = CSICamera(width=1280, height=720, fps=10)

fx, fy, cx, cy = None, None, None, None

K=[[1.14031559e+03, 0.00000000e+00, 6.75493397e+02],
   [0.00000000e+00, 1.11665091e+03, 3.72290304e+02],
   [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]

old = {}
new = {}

def near(v1, v2, thr=10):
  return np.sqrt(((v1-v2)**2).sum()) < thr

while True:
  frame = cam.read()
  frame = cv.cvtColor(frame, cv.COLOR_BGRA2BGR)

#  _, frame0 = cv.threshold(frame, 127, 255, cv.THRESH_OTSU+cv.THRESH_BINARY_INV)
#  frame = cv.adaptiveThreshold(frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 15, 3)

#  frame -= frame0

  dets, det_ids, _ = detector.detectMarkers(frame)

  print(dets, det_ids)

#  frame = cv.cvtColor(frame, cv.COLOR_GRAY2RGB)
  cv.imshow("Cam", frame)
  old = new
  new = {}
  correct = {}
#  if det_ids is None: continue
  aruco.drawDetectedMarkers(frame, dets, det_ids)

  cv.imshow("Cam", frame)
  if cv.waitKey(1) & 0xFF in (27, ord('q')):
    break

cam.running=False
cv.destroyAllWindows()
