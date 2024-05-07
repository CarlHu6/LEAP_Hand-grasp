This is the grasp function that uses the LEAP hand.

Dynamixel Preparing:

Before using the LEAP hand, it is necessary to download Dynamixel Wizard 2 to change the ID and frequency of each motor and request Dynamixel port access. 
The installation of Dynamixel Wizard has a link: https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/.

Tutorial about changing the ID and frequency of each motor: https://emanual.robotis.com/docs/en/software/rplus1/dynamixel_wizard/


ROS Setting:

Checking if it is using ROS 1 or not. If not, please Install ROS 1 Noetic normally first on Ubuntu 20.04.
The setting of ROS 1 could be easily by following the ROS setting part in the LEAP_Hand_API repository with this link https://github.com/leap-hand/LEAP_Hand_API/tree/main/ros_module


Python Setting:

Python setting with different systems could easily follow the python folder in the LEAP_Hand_API: https://github.com/CarlHu6/LEAP_Hand-grasp/tree/main/LEAP_hand_API/python.


For grasp:

The demo code only asks for the LEAP hand to be closed and not to control the Franka. The demo code for LEAP hand grasp could be run by: python grasp.py 

The control with Franka and LEAP hand grasp could be run by Franka_control.py

Franka pose information could be saved into an npz file in save_load.py, and it could also read the file for the Franka pose.

