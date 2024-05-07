# import keyboard
# import time
# Grasping = False

# c = 0
# m = 0

# while True:
#     print(c)
#     if c < 1000:
#         c+=1
#     if keyboard.is_pressed('g'):
#         print("Grasping start")
#         Grasping = True
#     while Grasping == True:
#         print("m",m)
#         if m < 500:
#             m += 1
#         if keyboard.is_pressed('e'):
#             Grasping = False
#             print("Grasping end")
#         time.sleep(0.1)
#     if c>= 1000:
#         break
#     time.sleep(0.1)
    
import threading
import time
# Import your LEAP hand control module and Franka Emika control module
# from leap_hand_utils.dynamixel_client import *
# import leap_hand_utils.leap_hand_utils as lhu
import keyboard
import numpy as np
# from grasp import LeapNode
# Import your Franka Emika control module here

class RobotSystem:
    def __init__(self):
        # self.leap_hand = LeapNode()  # Assuming LeapNode is your LEAP hand control class
        # Initialize your Franka Emika control object here
        self.running = True
        self.grab = False

    def control_leap_hand(self):
        # Example loop to open and close the hand
         
        while self.running == True:
            # Open the hand (set to your opening position)
            # self.leap_hand.set_allegro(np.zeros(16))  # Opening gesture
            # time.sleep(2)  # Adjust timing based on your requirements
            if keyboard.is_pressed('e'):
                self.grab = True 
            while self.grab == True:
                print("grabing")
                time.sleep(1)
            # Close the hand (set to your closing position)
            closing_positions =  180  # Example closing positions, adjust as needed
            # self.leap_hand.set_leap(closing_positions)  # Closing gesture
            time.sleep(0.1)  # Adjust timing based on your requirements

    def control_franka_emika(self):
        # Example loop to move Franka Emika
        while self.running:
            # Move Franka to a specific position
            # franka_emika.move_to(x, y, z)  # Placeholder for Franka Emika control command
            print("Moving Franka Emika...")
            time.sleep(1)  # Simulate the time for movement

    def start(self):
        # Create threads for hand and robot control
        leap_hand_thread = threading.Thread(target=self.control_leap_hand)
        franka_emika_thread = threading.Thread(target=self.control_franka_emika)

        # Start the threads
        leap_hand_thread.start()
        franka_emika_thread.start()

        try:
            # Keep the main thread running, or press Ctrl+C to stop
            while True:
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("Stopping...")
            self.grab = False
            self.running = False
            leap_hand_thread.join()
            franka_emika_thread.join()
            print("Stopped.")

if __name__ == "__main__":
    # npzfile = np.load('C:\Users\carlh\Desktop\CMU-Research\GitHub\LEAP_Hand_API\python\Initial_pose_1.npz')
    npzfile = np.load('C:/Users/carlh/Desktop/CMU-Research/GitHub/LEAP_Hand_API/python/Initial_pose_1.npz')

    # Print the list of array names contained in the file
    print("Arrays in NPZ file:", npzfile.files)

    # Loop through each array and print its contents
    for arr in npzfile.files:
        print(f"Contents of '{arr}':")
    print(npzfile[arr])
    robot_system = RobotSystem()
    robot_system.start()
    

        
