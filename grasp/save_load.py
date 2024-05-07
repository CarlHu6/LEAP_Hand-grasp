
import numpy as np 
import os 

def save_pose(fa, file_name: str):
    """
    Saves the pose info of Franka
    """
    try: 
        save_pose = fa.get_pose()
        print(save_pose)
    except AttributeError:
        print("Error: No pose info")
        return None
    
    translation = save_pose.translation
    rotation = save_pose.rotation
    print(translation)

    try:
        joints = fa.get_joints()
    except AttributeError:
        print("Error: No Joints Info")
        return None
    

    root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    save_folder = os.path.join(root_folder, 'pose_info')

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    save_path = os.path.join(save_folder, f"{file_name}.npz")
    

    try:
        np.savez(save_path, translation=translation, rotation=rotation, joints=joints)
        print("Saved: Pose & Joints Info Saved")
    except IOError:
        print(f"Error: Could not save to file {file_name}.")
        return None


def load_pose(file_name):
    root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    file_path = os.path.join(root_folder, 'pose_info', f'{file_name}.npz')
    try:
        robot_info = np.load(file_path, encoding='latin1', allow_pickle=True)
        print("Loaded: Pose & Joints Info Loaded")
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None

    translation = robot_info['translation']
    rotation = robot_info['rotation']
    joints = robot_info['joints']

    return translation, rotation, joints
