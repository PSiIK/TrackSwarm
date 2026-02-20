from pupil_apriltags import Detector
from nvidialibs.jetcam.csi_camera import CSICamera
import cv2 as cv
import numpy as np

detector = Detector()
cam = CSICamera(width=640,height=360)

fx, fy, cx, cy = None, None, None, None

K=[[947.57831706,   0.        , 324.35691989],
   [  0.        , 931.81281943, 181.92066756],
   [  0.        ,   0.        ,   1.        ]]

while True:
  frame = cam.read()
  frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

  dets = detector.detect(frame, estimate_tag_pose=True, tag_size=0.15, camera_params=(K[0][0], K[1][1], K[0][2], K[1][2]))
  frame = cv.cvtColor(frame, cv.COLOR_GRAY2RGB)
  for det in dets:
    corners = np.array(det.corners, np.int32).reshape((-1,1,2))
    cv.polylines(frame, [corners], True, (255, 0, 0), thickness=4)
	 
  cv.imshow("Cam", frame)
  if cv.waitKey(1) & 0xFF in (27, ord('q')):
    break

camera.running=False
cv.destroyAllWindows()
