from nvidialibs.jetracer.nvidia_racecar import NvidiaRacecar
from nvidialibs.jetcam.csi_camera import CSICamera
import cv2 as cv
import cv2.aruco as aruco
import numpy as np

TARGET_ARUCO_ID = 339
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 10

def main(): 
  detector = aruco.ArucoDetector(aruco.getPredefinedDictionary(aruco.DICT_4X4_1000))
  cam = CSICamera(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fps=FPS)
  car = NvidiaRacecar()  
   
  try:
    while True:
      # Read data from camera
      frame = cam.read()
      frame = cv.cvtColor(frame, cv.COLOR_BGRA2BGR)
      cv.imshow("Cam", frame)

      # Detect tags
      dets, det_ids, _ = detector.detectMarkers(frame)
      dets = np.array(dets)
      det_ids = np.array(det_ids)
      
      # Process tags
      if len(dets) > 0:
        mask = (det_ids == TARGET_ARUCO_ID).reshape(-1)
        target_dets = dets[mask]
        target_det_ids = det_ids[mask]
     
     
        if len(target_dets) > 0:
          aruco.drawDetectedMarkers(frame, target_dets, target_det_ids)
          cv.imshow("Cam", frame)
        
          # Adjust steering
          centroid = target_dets[0][0].mean(axis=0)
          car.steering = (centroid[0]- WINDOW_HEIGHT / 2) / (WINDOW_HEIGHT / 2)
          
          print("Target tag has been found")
          print("Corners:", target_dets[0][0])
          print("Target shape:", target_dets[0][0].shape)
          print("Type:", type(target_dets[0][0]))
          print("Centroid:", centroid)

      # Exit window
      if cv.waitKey(1) & 0xFF in (27, ord('q')):
        break
  finally:
    car.steering = 0
    car.throttle = 0
   

  cam.running=False
  cv.destroyAllWindows()

if __name__ == "__main__":
  main()
