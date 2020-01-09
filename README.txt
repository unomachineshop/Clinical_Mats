[Pressure Mats]
A 2x2 grid of contact sensing mats allowing researchers to conduct
tests on there clients with an easy to use GUI. The idea is to allow
three seperate types of tests to be run on the fly. The tests include 
"front to back", "left to right", and "random" mode. The algorithm randomly 
selects active mats based upon the test criteria, ensuring that the tests will
be run uniquely, yet thoroughly for all individuals. 

This was accomplished through the use of...
-Raspberry Pi Model 3 B+: Acted as the brains of the operation. Displays GUI,
allows user interaction, calculates and produces the three algorithms mentioned above.
-Arduino UNO: Acted as the relay point, between the physical mats, and the
Raspberry Pi. Through some mathematics it was able to clearly define if the 
mat was pressed or not, sending out a 1 or 0 value to indicate.

[How to Operate]
You will need...
-A USB mouse, for selecting the different tests.
-A monitor with HDMI cable to display GUI.
-A micro USB cable. (standard Android phone charging cable will work)
In order to run this, all you need to do is simply power on the device, 
with the HDMI cable plugged in to a Monitor. The Raspberry Pi will boot up, and 
automatically run the program.

If the program terminates for any reason, on the Desktop itself, there is
a clearly defined icon to restart the program, named "Pressure Mats".

Should you need to look at the code, you can issue the following within
a terminal. Best not to change the code unless you know what you are doing :D.
cd /home/pi/PressureMats
vim pressure_mats.py
