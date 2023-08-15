# Pico-pong
A pong game for the Raspberry Pi Pico.

Materials:  
  Two Joystick modules that use potentiometers  
  An SH1106 128x64 I2C OLED display  
  A Raspberry Pi Pico (Wireless or not, it doesn't matter)  
  Dupont wires and breadboard  

To make:  
  Download both sh1106.py and main.py and oppen them in Thonny (or your micropython IDE)  
  Save both files to the Pico's memory  
  Connect the GND and +5v pins of the joysticks to ground and 3.3v (or 5v)  
  Connect the VRy pin of Player 1's joystick to GPIO 26 (pin 31)  
  Connect the VRy pin of Player 2's joystick to GPIO 27 (pin 32)  
  Connect the GND and VCC pins of the OLED display to ground and 3.3v  
  Connect the SCL pin of the OLED display to GPIO 1 (pin 2)  
  Connect the SDA pin of the OLED display to GPIO 0 (pin 1)  

Plug in the Pico to a power source and ready up by wiggling your joystick up and down!  

If it doesn't work, check your pin connections.  
If the joystick doesn't work, try using VRx instead of VRy, or turn your joystick sideways.  
