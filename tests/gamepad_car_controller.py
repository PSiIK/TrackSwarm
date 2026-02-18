# Imports
from nvidialibs.jetracer.nvidia_racecar import NvidiaRacecar
import pygame.joystick as joystick
import pygame

# Gamepad constants
GAMEPAD_ID = 0
LEFT_STICK_X_ID = 0
LEFT_STICK_Y_ID = 1
RIGHT_TRIGGER_ID = 4
LEFT_TRIGGER_ID = 5

# Initialize pygame modules
pygame.init()

# Entry point for program
def main():
  # Initialize jetracer
  car = NvidiaRacecar()
  car.steering_offset = -0.00390625
  print("JetRacer has been initialized!")  
  
  # Print out controller informations
  print("Number of connected joysticks:", joystick.get_count())
  gpad = joystick.Joystick(GAMEPAD_ID)
  print("Joystick name:", gpad.get_name())
  
  try:
    # Execution loop
    while True:
      pygame.event.get()
    
		  # Get current stick position  
      x = gpad.get_axis(LEFT_STICK_X_ID)
      y = gpad.get_axis(LEFT_STICK_Y_ID)
		  
		  # Get trigger positions
      rtrig = gpad.get_axis(RIGHT_TRIGGER_ID)
      ltrig = gpad.get_axis(LEFT_TRIGGER_ID)
      
      # Update car parameters
      car.steering = x
      
      if rtrig * ltrig > 0:    # Stop vehicle
        car.throttle = 0
      elif rtrig > 0:          # Move forward
        car.throttle = rtrig
      elif ltrig > 0:          # Move backward
        car.throttle = ltrig*-1
      
  finally:
    # Reset car parameters
    car.steering_offset = 0
    car.steering = 0
    car.throttle = 0
    
    

if __name__ == "__main__":
  main()
