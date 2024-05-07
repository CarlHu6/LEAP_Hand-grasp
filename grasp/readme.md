This is the grasp funciton that using the LEAP hand

Dynamixel preparing:
Before using the LEAP hand, it is necessary to download Dynamixel Wizard 2 for changing ID and frequency of each motor, and request the dynamixel port access before use. 
The installation of Dynamixel Wizard has link: https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/
Tutorial about changing ID and frequency of each motor: https://emanual.robotis.com/docs/en/software/rplus1/dynamixel_wizard/

ROS setting:
Checking if it is using ROS 1 or not. If not, please Install ROS 1 Noetic normally first on Ubuntu 20.04.
The setting of ROS 1 could be easily by folloing the ROS setting part in the LEAP_Hand_API repostory with this link https://github.com/leap-hand/LEAP_Hand_API/tree/main/ros_module

python setting:
python setting with different system could easily follow the python folder in the LEAP_Hand_API: https://github.com/CarlHu6/LEAP_Hand-grasp/tree/main/LEAP_hand_API/python


For grasp:
The demo code only asking to close the LEAP hand and not controlling the Franka. The demo code for LEAP hand grasp could be run by: python grasp.py 
The controlling with Franka and LEAP hand grasp could be run by: Franka_control.py
Franka pose information could be saved into npz file in save_load.py and it could alse read the file for the Franka pose

