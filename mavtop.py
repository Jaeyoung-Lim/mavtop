from __future__ import print_function
import sys,os
import curses
import time
import threading
from pymavlink import mavutil
from argparse import ArgumentParser
from Vehicle import Vehicle

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

    cursor_x = 0
    cursor_y = 0

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

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        # Declaration of strings
        title = "MAVTOP"[:width-1]
        subtitle = "Written by Jaeyoung Lim"[:width-1]
        keystr = "Last key pressed: {}".format(k)[:width-1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)

        if k == 0:
            keystr = "No key press detected..."[:width-1]

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 10)

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))
        
        # Render Table header
        table_y = int((height // 2) - 2)
        tableheaderstr = " SYS_ID  TYPE       AUTOPILOT  MODE        STATUS     VERSION".format(cursor_x, cursor_y)
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(table_y, 0, tableheaderstr)
        stdscr.addstr(table_y, len(tableheaderstr), " " * (width - len(tableheaderstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        num_mav = len(list)
        num_mav_str = "Number of Vehicles : " + str(num_mav).format(cursor_x, cursor_y)
        stdscr.addstr(table_y-1, 0, num_mav_str)


        # Render values of tables
        for mav_count in range (0, len(list)):
            mav1str = " "+ str(list[mav_count].sys_id) + "       " + str(list[mav_count].getTypeString()) + "  " + str(list[mav_count].getAutopilotString()) + "        " + str(list[mav_count].getModeString()) + "   " + str(list[mav_count].getStatusString()) + "    " + str(list[mav_count].mavlink_version) + "".format(cursor_x, cursor_y)
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(table_y + mav_count + 1, 0, mav1str)
            stdscr.addstr(table_y + mav_count + 1, len(mav1str), " " * (width - len(mav1str) - 1))
            stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)
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