import curses

# Initialize
stdscr = curses.initscr()

# Configure Curses
curses.noecho()
curses.cbreak()
curses.start_color()

stdscr.keypad(1)

stdscr.addstr(0, 0, "Current mode: Typing mode",
              curses.A_REVERSE)
stdscr.refresh()
# stdscr.addstr("Pretty text", curses.color_pair(1))
stdscr.refresh()


# # Terminate program
# curses.nocbreak(); stdscr.keypad(0); curses.echo()