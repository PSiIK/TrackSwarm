import numpy as np
import cv2
def generuj_obraz_z_log_odds(file_name, global_x, global_y):
    raw_grid = np.load(file_name)
    prob_grid = 1.0 - (1.0 / (1.0 + np.exp(raw_grid)))
    image = 1.0 - prob_grid
    imagecv2 = (image*255.0).astype(np.uint8)
    name = file_name.replace(".npy", "_opencv.png")
    imagecolor = cv2.cvtColor(imagecv2, cv2.COLOR_GRAY2BGR)
    x_lenght = raw_grid.shape[0]
    y_lenght = raw_grid.shape[1]
    mid_x = x_lenght // 2
    mid_y = y_lenght // 2
    rob_px_x = int(global_x / 0.1) + mid_x
    rob_px_y = int(global_y / 0.1) + mid_y
    pozycja_piksel = (rob_px_y, rob_px_x)
    cv2.circle(imagecolor, pozycja_piksel, radius=1, color=(0, 0, 255), thickness=-1)
    new_size = (imagecolor.shape[1] * 3, imagecolor.shape[0] * 3)
    imagecolor = cv2.resize(imagecolor, new_size, interpolation=cv2.INTER_NEAREST)
    cv2.imwrite(name, imagecolor)
    window_name = "map"
    cv2.imshow(window_name, imagecolor)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
file = open("pos.txt", "r")
text = file.readline()
x, y = text.split(" ")
generuj_obraz_z_log_odds("submap0.npy", float(x), float(y))