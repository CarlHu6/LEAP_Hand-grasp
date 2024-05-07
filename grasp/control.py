from grasp import LeapNode
import threading
import time
import numpy as np
# Assuming LeapNode is defined in your imports

class ContinuousHandController:
    def __init__(self, leap_hand):
        self.leap_hand = leap_hand
        self.keep_running = True
        self.current_pose = np.zeros(16)  # Default to an open hand

    def run(self):
        while self.keep_running:
            self.leap_hand.set_leap(self.current_pose)
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


def move_franka_to_position(x, y, z):
    """Move the Franka Emika robot to the specified position."""
    # Your Franka Emika control logic here
    print(f"Moving Franka to position: {x}, {y}, {z}")
    # Simulate some movement time
    time.sleep(5)
    print("Franka movement complete.")
    
    



def main():
    leap_hand = LeapNode()  # Initialize LEAP hand
    hand_controller = ContinuousHandController(leap_hand)
    
    
    # Start the continuous control thread
    t = threading.Thread(target=hand_controller.run)
    t.start()
    hand_controller.adjust_force(coefficient=0.3) 

    # Open the LEAP hand (if not already open)
    open_pose = np.zeros(16)  # Assuming zeros represent the open pose
    hand_controller.update_pose(open_pose)
    time.sleep(10)  # Allow time for the hand to open

    # Move the Franka Emika robot to a desired position
    # move_franka_to_position(100, 200, 300)  # Example coordinates

    # Close the LEAP hand
    close_pose = np.ones(16)  # Assuming this represents the closed pose
    hand_controller.update_pose(close_pose)
    time.sleep(10)  # Allow time for the hand to close

    # Stop the continuous control thread
    hand_controller.stop()
    t.join()

if __name__ == "__main__":
    main()
    