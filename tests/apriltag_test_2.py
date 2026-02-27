from pupil_apriltags import Detector
from nvidialibs.jetcam.csi_camera import CSICamera
import cv2 as cv
import numpy as np

detector = Detector(families="tagCircle21h7", quad_decimate=2, quad_sigma=0.5, decode_sharpening=0.5)
cam = CSICamera(width=1280, height=720, fps=10)

fx, fy, cx, cy = None, None, None, None

K=[[1.14031559e+03, 0.00000000e+00, 6.75493397e+02],
   [0.00000000e+00, 1.11665091e+03, 3.72290304e+02],
   [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]

old = {}
new = {}

def near(v1, v2, thr=10):
  return np.sqrt(((v1-v2)**2).sum()) < thr

clahe=cv.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
while True:
  frame = cam.read()

  frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
  frame = cv.GaussianBlur(frame, (3, 3), 0.8)
  frame = clahe.apply(frame)
  _, frame0 = cv.threshold(frame, 127, 255, cv.THRESH_OTSU+cv.THRESH_BINARY_INV)
  frame1 = cv.adaptiveThreshold(frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 21, 3)

  frame = frame1 - frame0

  dets = detector.detect(frame, estimate_tag_pose=True, tag_size=0.04, camera_params=(K[0][0], K[1][1], K[0][2], K[1][2]))
  frame = cv.cvtColor(frame, cv.COLOR_GRAY2RGB)
  old = new
  new = {}
  correct = {}
  for det in dets:
    corners = np.array(det.corners, np.int32).reshape((-1,1,2))
    cv.polylines(frame, [corners], True, (0, 0, 255), thickness=4)
    detcenter = corners.mean(axis=0)
    new[det.tag_id] = detcenter
    if (det.tag_id in old) and near(old[det.tag_id], detcenter, 25):
      correct[det.tag_id] = det
      cv.polylines(frame, [corners], True, (255, 0, 0), thickness=4)
	 
  cv.imshow("Cam", frame)
  if cv.waitKey(1) & 0xFF in (27, ord('q')):
    break

cam.running=False
cv.destroyAllWindows()
