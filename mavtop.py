from __future__ import print_function
import sys,os
import curses
import time
import threading
from pymavlink import mavutil
from argparse import ArgumentParser
from Vehicle import Vehicle
from Screen import Screen

k = 0
list = []

def findvehicle(id, list):
    for i in range(0, len(list)):
      if (id == list[i].sys_id):
        return i
    return -1

def draw_menu(stdscr):
    global k
    global list

    screen = Screen()

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()
    # stdscr.nodelay(1)

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # create a mavlink serial instance

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        screen.setSize(height, width)

        screen.moveCursor(stdscr, k)

        cursor_y = screen.getCursor()
        cursor_x = screen.getCursorX()

        # Declaration of strings
        title = "MAVTOP"[:width-1]


        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_y = 0

        # Render Elements
        screen.drawHeader(stdscr, list)
        screen.drawTable(stdscr, list)
        screen.drawStatusBar(stdscr)

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def mavlinkThread():
    connection = mavutil.mavlink_connection('udpin:0.0.0.0:14550')

    global list

    while True:
        msg = connection.recv_match(type='HEARTBEAT', blocking=True)

        sys_id = 1
        vehicle_id = findvehicle(sys_id, list)
        sys_status = msg.system_status
        mav_type = msg.type
        mav_autopilot = msg.autopilot
        mav_mode_flag = msg.base_mode
        mavlink_version = msg.mavlink_version

        if vehicle_id < 0 :
            vehicle = Vehicle(sys_id, mav_type, mav_autopilot, mav_mode_flag, sys_status, mavlink_version) # Create vehicle object if the vehicle was not seen before
            list.append(vehicle)
        else:
            list[vehicle_id].sys_id = 1
            list[vehicle_id].mav_state = msg.system_status

def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--baudrate", type=int,
                  help="master port baud rate", default=115200)
    parser.add_argument("--device", required=False, help="serial device")
    args = parser.parse_args()
    
    t = threading.Thread(name='daemon', target=mavlinkThread)
    t.setDaemon(True)
    t.start()

    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()