class Vehicle:
    def __init__(self, sys_id=1, mav_type=0, mav_autopilot=0, mav_mode_flag=128, mav_state=1, mavlink_version=2):
        self.sys_id = sys_id
        self.mav_type = mav_type
        self.mav_autopilot = mav_autopilot
        self.mav_mode_flag = mav_mode_flag
        self.mav_state = mav_state
        self.mavlink_version = mavlink_version

    def getTypeString(self):
        switcher = {
            0: "GENERIC",
            1: "FIXEDWING",
            2: "QUADROTOR",
            3: "COAXIALHELI",
        }
        return switcher.get(self.mav_type, "UNKNOWN")

    def getAutopilotString(self):
        switcher = {
            0: "GENERIC",
            1: "RESERVED",
            3: "ARDUPILOT",
            12: "PX4",
        }
        return switcher.get(self.mav_autopilot, "UNKNOWN")

    def getModeString(self):
        switcher = {
            128: "Safety Armed",
            64: "Manual",
            32: "HIL",
            81: "Stabilize",
            89: "Auto",
        }
        return switcher.get(self.mav_mode_flag, "UNKNOWN")

    def getStatusString(self):
        switcher = {
            0: "Unknown",
        }
        return switcher.get(self.mav_mode_flag, "UNKNOWN")