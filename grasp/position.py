import numpy as np
from scipy.spatial.transform import Rotation as R

from frankapy import FrankaArm 
import time
from save_load import *

fa = FrankaArm()

file = 'position_1'

save_pose(fa,file)
