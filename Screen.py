import curses

class Screen:
    def __init__(self):
        self.tablestart_row = 4
        self.cursor = 12
        self.cursor_x = 0
        self.screen_height = 24
        self.screen_width = 24
        self.key = 0
        self.table_attr =["SYSID  ", "TYPE       ", "AUTOPILOT  ", "STATUS     ", "MODE     ", "VERSION  "]

    def setSize(self, height, width):
        self.screen_height = height
        self.screen_width = width

    def moveCursor(self, stdscr, key):

        self.key = key
        if key == curses.KEY_DOWN:
            self.cursor = self.cursor + 1
        elif key == curses.KEY_UP:
            self.cursor = self.cursor - 1
        elif key == curses.KEY_RIGHT:
            self.cursor_x = self.cursor_x + 1
        elif key == curses.KEY_LEFT:
            self.cursor_x = self.cursor_x - 1

        self.cursor_x = max(0, self.cursor_x)
        self.cursor_x = min(self.screen_width - 1, self.cursor_x)
        self.cursor = max(self.tablestart_row + 1, self.cursor)
        self.cursor = min(self.screen_height - 2, self.cursor)

        stdscr.move(self.cursor, self.cursor_x)
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(self.cursor, 0, " " * self.screen_width)
        stdscr.attroff(curses.color_pair(4))

        if key == curses.KEY_ENTER:
            self.cursor_x = self.cursor_x
            # Open subwindow with options


    def getCursor(self):
        return self.cursor

    def getCursorX(self):
        return self.cursor_x

    def drawTable(self, stdscr, list):
        tableheaderstr = self.table_attr[0] +\
                         self.table_attr[1] +\
                         self.table_attr[2] +\
                         self.table_attr[3]+\
                         self.table_attr[4] +\
                         self.table_attr[5] + "".format(0, self.cursor)

        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(self.tablestart_row, 0, tableheaderstr)
        stdscr.addstr(self.tablestart_row, len(tableheaderstr), " " * (self.screen_width - len(tableheaderstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        for mav_count in range (0, len(list)):
            mav1str = str(list[mav_count].sys_id) + " " * (len(self.table_attr[0]) - len(str(list[mav_count].sys_id))) +\
                      str(list[mav_count].getTypeString()) + " " * (len(self.table_attr[1]) - len(str(list[mav_count].getTypeString()))) +\
                      str(list[mav_count].getAutopilotString()) + " " * (len(self.table_attr[2]) - len(str(list[mav_count].getAutopilotString()))) +\
                      str(list[mav_count].getModeString()) + " " * (len(self.table_attr[3]) - len(str(list[mav_count].getModeString()))) +\
                      str(list[mav_count].getStatusString()) + " " * (len(self.table_attr[4]) - len(str(list[mav_count].getStatusString()))) +\
                      str(list[mav_count].mavlink_version) + "".format(self.cursor_x, self.cursor)
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(self.tablestart_row + mav_count + 1, 0, mav1str)
            stdscr.addstr(self.tablestart_row + mav_count + 1, len(mav1str), " " * (self.screen_width - len(mav1str) - 1))
            stdscr.attroff(curses.color_pair(3))


    def drawHeader(self, stdscr, list):
        # Declaration of strings
        title = "MAVTOP"[:self.screen_width - 1]

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(0, self.screen_width - (len(title) // 2) - len(title), title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(self.screen_width, self.screen_height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        keystr = []
        if self.key == 0:
            keystr = "No key press detected..."[:self.screen_width - 1]
        else:
            keystr = "Last key pressed: {}".format(self.key)[:self.screen_width - 1]

        stdscr.addstr(self.tablestart_row - 3, 0, keystr)

        num_mav = len(list)
        num_mav_str = "Number of Vehicles : " + str(num_mav).format(0, self.cursor)
        stdscr.addstr(self.tablestart_row-2, 0, num_mav_str)

    def drawStatusBar(self, stdscr):
        # Render status bar
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(self.cursor_x, self.cursor)
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(self.screen_height - 1, 0, statusbarstr)
        stdscr.addstr(self.screen_height - 1, len(statusbarstr), " " * (self.screen_width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))








