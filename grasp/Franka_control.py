
from scipy.spatial.transform import Rotation
import numpy as np
import time
from scipy.spatial.transform import Rotation as R
import keyboard
from save_load import *
from frankapy import FrankaArm
from grasp import LeapNode
import threading
import time
import numpy as np




class ContinuousHandController:
    def __init__(self, leap_hand):
        self.leap_hand = leap_hand
        self.keep_running = True
        self.current_pose = np.zeros(16)  # Default to an open hand

    def run(self):
        while self.keep_running:
            self.leap_hand.set_allegro(self.current_pose)
            time.sleep(0.02)  # Short sleep to prevent overloading the communication

    def update_pose(self, new_pose):
        self.current_pose = new_pose

    def stop(self):
        self.keep_running = False

    def adjust_force(self, coefficient):
        """
        Adjust the force by updating the current limit of the motors
        based on the specified coefficient.
        """
        self.leap_hand.update_current_limit(coefficient)




def to_position(fa, file_name):

    pose = load_pose(file_name)
    current_pose = fa.get_pose()
    # print(pose)

    pose_translation = pose[0]
    pose_rotation = pose[1]

    current_pose.translation = pose_translation
    fa.goto_pose(current_pose)


def move_franka_to_position(fa, file_name):
    """Move the Franka Emika robot to the specified position."""
    # Your Franka Emika control logic here
    pose = load_pose(file_name)
    current_pose = fa.get_pose()
    print(pose)

    pose_translation = pose[0]
    pose_rotation = pose[1]

    current_pose.translation = pose_translation
    fa.goto_pose(current_pose)
    time.sleep(5)
    

def main():

    half_close = np.array([0,0.5,0.5,0.5,0,0.5,0.5,0.5,0,0.5,0.5,0.5,0.5,0,0.5,0.5])
    all_close = np.array([0,1,1,1,0,1,1,1,0,1,1,1,1.5,-0.5,0.5,1])
    ready_pose = np.array([0,1.2,0,0,0,1.2,0,0,0,1.2,0,0,1.5,-1.3,-0.5,0])

    pick_close = np.array([0,1.5,0.5,0.5,0,1.5,0.5,0.5,0,1.5,0.5,0.5,1.5,-1.3,0.3,0.3])

    fa = FrankaArm() # Initialize Franka
    leap_hand = LeapNode()  # Initialize LEAP hand
    hand_controller = ContinuousHandController(leap_hand)
    
    
    # Start the continuous control thread
    t = threading.Thread(target=hand_controller.run)
    t.start()
    hand_controller.adjust_force(coefficient=0.3) 

    # Open the LEAP hand (if not already open)
    open_pose = np.zeros(16)  # Assuming zeros represent the open pose
    hand_controller.update_pose(open_pose)
    time.sleep(3)  # Allow time for the hand to open

    to_position(fa, 'position_1')
    to_position(fa, 'position_2')

    #prepare to pick up
    hand_controller.adjust_force(coefficient=0.1) 
    hand_controller.update_pose(ready_pose)
    time.sleep(2)


    #Close the LEAP hand
    close_pose = pick_close
    hand_controller.adjust_force(coefficient=1) 
    hand_controller.update_pose(close_pose)
    time.sleep(3) 

    
    # hand_controller.adjust_force(coefficient=0.3) 
    # hand_controller.update_pose(close_pose)
    # time.sleep(2)  # Allow time for the hand to close

    # Stop the continuous control thread
    fa.reset_joints()
    asking = input("type s for stop: ")
    if asking == 's':
        hand_controller.stop()

    t.join()




if __name__ == '__main__':
    print("start")
    main()
    print('end')
    # fa = FrankaArm()
    # to_position(fa, 'position_2')
    # # to_position(fa, 'position_1')