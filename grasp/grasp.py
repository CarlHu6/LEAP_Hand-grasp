#!/usr/bin/env python3
import numpy as np

from leap_hand_utils.dynamixel_client import *
import leap_hand_utils.leap_hand_utils as lhu
import time
# import keyboard
#######################################################
"""This can control and query the LEAP Hand

I recommend you only query when necessary and below 90 samples a second.  Each of position, velociy and current costs one sample, 
so you can sample all three at 30 hz or one at 90hz.

#Allegro hand conventions:
#0.0 is the all the way out beginning pose, and it goes positive as the fingers close more and more
#http://wiki.wonikrobotics.com/AllegroHandWiki/index.php/Joint_Zeros_and_Directions_Setup_Guide 
# I belive the black and white figure (not blue motors) is the zero position, and the + is the correct way around.  
# LEAP Hand in my videos start at zero position and that looks like that figure.

#LEAP hand conventions:
#180 is flat out for the index, middle, ring, fingers, and positive is closing more and more.

"""
########################################################
class LeapNode:
    def __init__(self):
        ####Some parameters
        # self.ema_amount = float(rospy.get_param('/leaphand_node/ema', '1.0')) #take only current
        self.kP = 600
        self.kI = 0
        self.kD = 200
        self.curr_lim = 350
        self.prev_pos = self.pos = self.curr_pos = lhu.allegro_to_LEAPhand(np.zeros(16))
        
        self.target_pos = lhu.allegro_to_LEAPhand(np.zeros(16))
        self.grab_thread = False
           
        #You can put the correct port here or have the node auto-search for a hand at the first 3 ports.
        self.motors = motors = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        try:
            self.dxl_client = DynamixelClient(motors, '/dev/ttyUSB0', 4000000)
            self.dxl_client.connect()
        except Exception:
            try:
                self.dxl_client = DynamixelClient(motors, '/dev/ttyUSB1', 4000000)
                self.dxl_client.connect()
            except Exception:
                self.dxl_client = DynamixelClient(motors, 'COM13', 4000000)
                self.dxl_client.connect()
                
        #Enables position-current control mode and the default parameters, it commands a position and then caps the current so the motors don't overload
        # self.dxl_client.sync_write(motors, np.ones(len(motors))*5, 11, 1)
        self.dxl_client.set_torque_enabled(motors, True)
        # self.dxl_client.sync_write(motors, np.ones(len(motors)) * self.kP, 84, 2) # Pgain stiffness     
        # self.dxl_client.sync_write([0,4,8], np.ones(3) * (self.kP * 0.75), 84, 2) # Pgain stiffness for side to side should be a bit less
        # self.dxl_client.sync_write(motors, np.ones(len(motors)) * self.kI, 82, 2) # Igain
        # self.dxl_client.sync_write(motors, np.ones(len(motors)) * self.kD, 80, 2) # Dgain damping
        # self.dxl_client.sync_write([0,4,8], np.ones(3) * (self.kD * 0.75), 80, 2) # Dgain damping for side to side should be a bit less
        
        #Max at current (in unit 1ma) so don't overheat and grip too hard #500 normal or #350 for lite
        
        self.dxl_client.sync_write(motors, np.ones(len(motors)) * self.curr_lim, 102, 2)
        self.dxl_client.write_desired_pos(self.motors, self.curr_pos)

    #Receive LEAP pose and directly control the robot
    def update_current_limit(self, coefficient):
        """
        Update the current limit applied to the motors by multiplying
        the base current limit with a given coefficient.
        """
        new_curr_lim = self.curr_lim * coefficient
        self.dxl_client.sync_write(self.motors, np.ones(len(self.motors)) * new_curr_lim, 102, 2)
    
    def set_leap(self, pose):
        self.prev_pos = self.curr_pos
        self.curr_pos = np.array(pose)
        self.dxl_client.write_desired_pos(self.motors, self.curr_pos)
    #allegro compatibility
    def set_allegro(self, pose):
        pose = lhu.allegro_to_LEAPhand(pose, zeros=False)
        self.prev_pos = self.curr_pos
        self.curr_pos = np.array(pose)
        self.dxl_client.write_desired_pos(self.motors, self.curr_pos)
    #Sim compatibility, first read the sim value in range [-1,1] and then convert to leap
    def set_ones(self, pose):
        pose = lhu.sim_ones_to_LEAPhand(np.array(pose))
        self.prev_pos = self.curr_pos
        self.curr_pos = np.array(pose)
        self.dxl_client.write_desired_pos(self.motors, self.curr_pos)
    #read position
    def read_pos(self):
        return self.dxl_client.read_pos()
    #read velocity
    def read_vel(self):
        return self.dxl_client.read_vel()
    #read current
    def read_cur(self):
        return self.dxl_client.read_cur()
    def disconnect(self):
        return self.dxl_client.disconnect()
    def connect(self):
        return self.dxl_client.connect()
    
    def goto(self, pose):
        self.set_allegro(pose)
        target = np.array(pose)
        re_target = target + 3.14159
        self.curr_pos = self.read_pos()
               
        # target_final = np.around(re_target, decimals=3)
        # self.curr_pos = np.around(self.curr_pos, decimals=3)
        all_differences = np.all(np.abs(re_target - self.curr_pos) < 0.08)
        while not all_differences:
            self.set_allegro(pose)
            self.curr_pos = self.read_pos()

            is_same = np.array_equal(re_target, self.curr_pos)
            all_differences = np.all(np.abs(re_target - self.curr_pos) < 0.1)
            # print(self.curr_pos)
            # print(re_target)
            # print(all_differences)
            
    
    
#init the node
def main(**kwargs):
    leap_hand = LeapNode()
    count = 0
    while True:
        desired_pos1 = np.array([0,0.5,0.5,0.5,0,0.5,0.5,0.5,0,0.5,0.5,0.5,0.5,0,0.5,0.5])
        # desired_pos2 = np.array([0,1,1,1,0,0,0,0,0,1,1,1,1,0,1,1])
        desired_pos = np.array([0,1,1,1,0,0,0,0,0,1,1,1,1,0.5,1,1])
        default_pos = np.zeros(16)
        # leap_hand.set_allegro(desired_pos1)
        # leap_hand.set_allegro(desired_pos2)
        # leap_hand.goto(desired_pos1)
        print("Position: " + str(leap_hand.read_pos()))
        if count <60:
            leap_hand.goto(default_pos)
            time.sleep(0.05)
            count += 1
        elif count >= 60 and count<120:
            leap_hand.update_current_limit(0.13)
            leap_hand.goto(desired_pos1)
            time.sleep(0.05)
            count+=1
        else:
            print("disconnect the LEAP hand")
            leap_hand.disconnect()
            
            break
        
    # for i in range(50):
    #     desired_pos1 = np.array([0,0.5,0.5,0.5,0,0.5,0.5,0.5,0,0.5,0.5,0.5,0.5,0,0.5,0.5])
    #     desired_pos = np.array([0,1,1,1,0,0,0,0,0,1,1,1,1,0.5,1,1])
    #     leap_hand.set_allegro(desired_pos1)
    #     print("Position: " + str(leap_hand.read_pos()))
    # while True:
    #     x = np.zeros(16)
    #     print(type(x))
    #     desired_pos1 = np.array([0,0.5,0.5,0.5,0,0.5,0.5,0.5,0,0.5,0.5,0.5,0.5,0,0.5,0.5])
    #     desired_pos = np.array([0,1,1,1,0,0,0,0,0,1,1,1,1,0.5,1,1])
    #     leap_hand.set_allegro(desired_pos1)
    #     print("Position: " + str(leap_hand.read_pos()))
    #     time.sleep(0.03)
    #     count += 1
    #     case = 1
    #     print(count)
    #     if case == 1 and count > 100:
    #         case = 2
    #         desired_pos2 = np.array([0,1,1,1,0,0,0,0,0,1,1,1,1,0,1,1])
    #         leap_hand.set_allegro(desired_pos2)
    #         count += 1
    #     if count >200 and case ==2:
    #         print("disconnect the LEAP hand")
    #         leap_hand.disconnect()
    #         break

if __name__ == "__main__":
    main()