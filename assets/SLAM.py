import math
import numpy as np
import time
import os
from scipy.linalg import svd
from gz.transport import Node
from gz.msgs.laserscan_pb2 import LaserScan
start=0
class submap:
    def __init__(self, global_x_start, global_y_start, global_angle_start):
        self.grid = np.zeros((300,300), dtype=float)
        self.global_pos = (global_x_start, global_y_start, global_angle_start)
        self.scan=[]
        self.scanammount=0
        self.finished=False
    
    

class GazeboSLAM:
    def __init__(self):
        self.submaps = []
        self.active_submap=None
        self.scan_limit_per_submap = 50
        self.oldmap=[]
        self.global_x = 0.0
        self.global_y = 0.0
        self.global_angle = 0.0
        self.distance=0
        self.history =[]
        self.node = Node()
        command="/scan"
        self.node.subscribe(LaserScan,command,self.scan_response)
    def find_closest_points(self,new_points, old_points): # szukanie punktów do ustalenia przemieszczenia robota
        pairs = []
        for new_point in new_points:
            thelowest_distance = float('inf')
            best_old_point = None
            for old_point in old_points:
                distance = math.dist(new_point, old_point)
                if distance < thelowest_distance:
                    thelowest_distance = distance
                    best_old_point = old_point   
            pairs.append((new_point, best_old_point))
        return pairs
    def move_points(self,points, dx, dy, kat): # korekta aktualnego scanu
        new_points = []
        for (x, y) in points:
            new_x = x * math.cos(kat) - y * math.sin(kat) + dx
            new_y = x * math.sin(kat) + y * math.cos(kat) + dy
            new_points.append((new_x, new_y))
        return new_points
    def calculating_move_and_angle(self,pairs): # algorytm do wyznaczania przesunięcia
        oldpoints = np.array([p[1] for p in pairs])
        newpoints = np.array([p[0] for p in pairs])
        newcentre= np.mean(newpoints, axis=0)
        oldcentre=np.mean(oldpoints, axis=0)
        modnewpoints = newpoints-newcentre
        modoldpoints = oldpoints - oldcentre
        H=np.dot(modnewpoints.T, modoldpoints) 
        (U,L,V_T)=svd(H)
        R = np.dot(V_T.T,U.T)
        tx =oldcentre[0] - (newcentre[0]*R[0][0] + newcentre[1]*R[0][1])
        ty= oldcentre[1] - (newcentre[0]*R[1][0] + newcentre[1]*R[1][1])
        d_angle= math.atan2(R[1][0],R[0][0])
        return tx, ty, d_angle
    def Location(self,oldmap, newmap, max_iteration): #ustalenie przesunięcia robota
        final_dx = 0.0
        final_dy = 0.0
        final_angle = 0.0
        for i in range(max_iteration):
            pary = self.find_closest_points(newmap, oldmap)
            dx, dy, dangle = self.calculating_move_and_angle(pary)
            final_dx += dx
            final_dy += dy
            final_angle += dangle
            newmap = self.move_points(newmap, dx, dy, dangle)
            if abs(dx) < 0.001 and abs(dy) < 0.001 and abs(dangle) < 0.0001:
                break
        return final_dx, final_dy, final_angle
    def bresenham(self, x0, y0, x1, y1): # algorytm do określania punktów między ścianą a robotem
        points = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            points.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        return points
    def mapping(self,global_map,empty_rays,newscan, global_x, global_y, global_dangle): # tworzenie map
        x_lenght=len(global_map)
        y_lenght=len(global_map[0])
        resolution=0.05
        mid_x= x_lenght//2
        mid_y=y_lenght//2
        Hit=0.85
        Miss=-0.4
        MAX_LOG = 5.0
        MIN_LOG = -5.0
        rob_x=int(global_x/resolution)+mid_x
        rob_y=int(global_y/resolution)+mid_y
        if not (0 <= rob_x < x_lenght and 0 <= rob_y < y_lenght):
            print("Robot poza mapą")
            return global_map
        for (x_loc, y_loc) in empty_rays:
            glob_x = x_loc * math.cos(global_dangle) - y_loc * math.sin(global_dangle) + global_x
            glob_y = x_loc * math.sin(global_dangle) + y_loc * math.cos(global_dangle) + global_y
            wall_x = int(glob_x / resolution) + mid_x
            wall_y = int(glob_y / resolution) + mid_y
            line = self.bresenham(rob_x, rob_y, wall_x, wall_y)
            for (px, py) in line:
                if (0 <= px < x_lenght and 0 <= py < y_lenght):
                    global_map[px][py] = max(MIN_LOG, global_map[px][py] + Miss)
                else:
                    break
        for (x_loc, y_loc) in newscan:
            glob_x = x_loc *math.cos(global_dangle)-y_loc*math.sin(global_dangle) + global_x
            glob_y = x_loc *math.sin(global_dangle)+y_loc*math.cos(global_dangle) + global_y
            wall_x = int(glob_x/resolution)+mid_x
            wall_y=int(glob_y/resolution)+mid_y
            if (0<= wall_x) and wall_x< x_lenght and 0<=wall_y and wall_y < y_lenght:
                line = self.bresenham(rob_x,rob_y,wall_x,wall_y)
                for(px,py) in line[:-1]:
                    if (global_map[px][py]!=100):
                        global_map[px][py]= min(MAX_LOG, global_map[px][py]+Miss)
                global_map[wall_x][wall_y]=max(MIN_LOG, global_map[wall_x][wall_y]+Hit)
        return global_map
    def loopcorrection(self,looplist, newscan): # jeśli znajdzie pętlę to wyznacza ile wynosi potencjalny błąd
        for i in looplist:
            dx,dy,dangle = self.Location(i[3],newscan, 40)
            movement=math.hypot(dx,dy)
            if(movement<2.0):
                error_x = i[0] - dx - self.global_x
                error_y = i[1] - dy - self.global_y
                error_angle = i[2] - dangle - self.global_angle
                return (error_x, error_y, error_angle)
        return None
    def correcting_submaps(self, correction): # naprawa pozostałych map
        error_x, error_y, error_angle = correction
        submaps_ammount = len(self.submaps)
        for i in range(submaps_ammount):
            weight = (1+i)/submaps_ammount
            old_x ,old_y, old_angle = self.submaps[i].global_pos
            new_x = old_x + error_x*weight
            new_y = old_y + error_y*weight
            new_angle = old_angle + error_angle * weight
            self.submaps[i].global_pos = (new_x,new_y,new_angle)
    def scan_response(self, msg): # serce programu
        robpos=[0,0,0]
        empty_rays,newscan=self.converting_gazebo(robpos,msg)
        if (len(self.oldmap)==0):
            self.oldmap = newscan
            return
        if (self.active_submap==None):
            self.active_submap= submap(self.global_x,self.global_y,self.global_angle)
        dx, dy, dangle= self.Location(self.oldmap, newscan, 20)
        step=math.hypot(dx,dy)
        self.global_x += dx * math.cos(self.global_angle) - dy * math.sin(self.global_angle)
        self.global_y += dx * math.sin(self.global_angle) + dy * math.cos(self.global_angle)
        self.global_angle += dangle
        if(step>0.01 or abs(dangle)>0.01 or self.active_submap.scanammount==0):
            self.distance += step
            loc_x = self.global_x - self.active_submap.global_pos[0]
            loc_y = self.global_y - self.active_submap.global_pos[1]
            loc_angle = self.global_angle - self.active_submap.global_pos[2]
            self.active_submap.grid = self.mapping(self.active_submap.grid,empty_rays ,newscan, loc_x, loc_y, loc_angle)
            self.active_submap.scan.append(newscan)
            self.active_submap.scanammount+=1
            if (self.active_submap.scanammount>=self.scan_limit_per_submap):
                self.active_submap.finished=True
                filename="submap" + str(len(self.submaps))
                np.save(filename,self.active_submap.grid)
                self.submaps.append(self.active_submap)
                self.active_submap = submap(self.global_x,self.global_y,self.global_angle)
                print("zapis danych")
            if (self.distance%1.0<step):
                possib_loop= self.search_for_loop(self.global_x,self.global_y, self.distance,self.history)
                correction=self.loopcorrection(possib_loop,newscan)
                if(correction!=None):
                    self.global_x+=correction[0]
                    self.global_y+=correction[1]
                    self.global_angle+=correction[2]
                    self.correcting_submaps(correction)
                self.history.append((self.global_x,self.global_y,self.global_angle,newscan))
        self.oldmap=newscan
    def search_for_loop(self, global_x, global_y, global_dist, history): # szukanie map do potencjalnej pętli
        lidar_error = 0.05
        search_area = 0.5 + global_dist*lidar_error
        prob_loops =[]
        for i, hist in enumerate(history):
            hist_x, hist_y, hist_angle, hist_map = hist
            if (len(history) - i <50):
                continue
            rob_distance = math.hypot(global_x-hist_x,global_y-hist_y)
            if(rob_distance<=search_area):
                prob_loops.append(hist)
        return prob_loops
    def converting_gazebo(self, robpos, msg): # Do zmiany w przypadku wprowadzenia do robota
        rob_x, rob_y, rob_angle = robpos
        scan_map = []
        empty_rays=[]
        for i, rang in enumerate(msg.ranges):
            if math.isinf(rang) or math.isnan(rang) or rang<0.2:
                continue
            angle_measured = msg.angle_min + i * msg.angle_step
            angle_calculated = rob_angle + angle_measured
            if  rang > 9.5:
                X = rob_x + 9.5 * math.cos(angle_calculated)
                Y = rob_y + 9.5 * math.sin(angle_calculated)
                empty_rays.append([X, Y])
            else:
                X = rob_x + rang * math.cos(angle_calculated)
                Y = rob_y + rang * math.sin(angle_calculated)
                scan_map.append([X, Y])
        return empty_rays, scan_map
if (__name__ == "__main__"):
    SLAM = GazeboSLAM()
    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        os._exit(0)