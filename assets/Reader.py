import numpy as np
import cv2
def generuj_obraz_z_log_odds(file_name):
    raw_grid = np.load(file_name)
    prob_grid = 1.0 - (1.0 / (1.0 + np.exp(raw_grid)))
    image = 1.0 - prob_grid
    imagecv2 = (image*255.0).astype(np.uint8)
    name = file_name.replace(".npy", "_opencv.png")
    cv2.imwrite(name, imagecv2)
    window_name = "map"
    cv2.imshow(window_name, imagecv2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
generuj_obraz_z_log_odds("submap0.npy")