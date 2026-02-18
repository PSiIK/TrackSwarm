# Imports
import pygame.joystick as joystick
import pygame

# Constants
GAMEPAD_ID = 0
LEFT_STICK_X_ID = 0
LEFT_STICK_Y_ID = 1
RIGHT_TRIGGER_ID = 4
LEFT_TRIGGER_ID = 5

# Initialize pygame modules
pygame.init()

# Entry point for program
def main():
  # Print out controller informations
  print("Number of connected joysticks:", joystick.get_count())
  gpad = joystick.Joystick(GAMEPAD_ID)
  
  print("Joystick name:", gpad.get_name())
  print("Power level:", gpad.get_power_level())
  print("Number of axes:", gpad.get_numaxes())
  print("Number of buttons:", gpad.get_numbuttons())
  
  # Execution loop
  while True:
    pygame.event.get()
  
		# Get current stick position  
    x = gpad.get_axis(LEFT_STICK_X_ID)
    y = gpad.get_axis(LEFT_STICK_Y_ID)
		
		# Get trigger positions
    rtrig = gpad.get_axis(RIGHT_TRIGGER_ID)
    ltrig = gpad.get_axis(LEFT_TRIGGER_ID)

    print(f"Current stick position: ({x},{y})")
    print(f"Left trigger: {ltrig}, Right trigger: {rtrig}") 

if __name__ == "__main__":
  main()
  
