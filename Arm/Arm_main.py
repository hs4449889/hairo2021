# import
import arm_inverse
import realsense
import struct
from timeout_decorator import timeout, TimeoutError


# settings
arm = arm_inverse.ARMS([1, 1, 1], [10, 160, -80])
