class Vehicle:
    def __init__(self, sys_id=1, mav_type=0, mav_autopilot=0, mav_mode_flag=128, mav_state=1, mavlink_version=2):
        self.sys_id = sys_id
        self.mav_type = mav_type
        self.mav_autopilot = mav_autopilot
        self.mav_mode_flag = mav_mode_flag
        self.mav_state = mav_state
        self.mavlink_version = mavlink_version