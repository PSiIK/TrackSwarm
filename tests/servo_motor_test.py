# Imports
from nvidialibs.jetracer.nvidia_racecar import NvidiaRacecar
import time 

# Constants
CHANGE = 0.25
DELAY = 0.01

# Entry point for program
def main():
  print("Hello World")
  car = NvidiaRacecar()  
  print(car)
  
  try:
    # Make sure that car doesn't move
    car.steering = 0
    car.throttle = 0  
    direction = 1
    
    # Execution loop
    while True:
      car.steering += CHANGE*direction
      car.throttle += CHANGE*direction
      
      # Change spinning direction
      if abs(car.steering) == 1:
        direction *= -1
        
      time.sleep(DELAY)
      
  except KeyboardInterrupt:
    # Reset car parameters
    car.steering = 0
    car.throttle = 0

if __name__ == "__main__":
  main()
