#!/usr/bin/env python

import sys
import curses

"""
"  This class allows the desired content to be selected.
"
"  Create a new class by passing service description menu items,
"    corresponding service strings to be returned as selections,
"    and keyboard shortcuts for each menu item, using 0 if there is none.
"""
class gridSelectionMenu:

    def teardownWindow(self):
        # General window teardown tasks
        curses.nocbreak()
        self.screen.keypad(0)
        curses.echo()
        curses.endwin()

    def getSelection(self):

        try:
            # Menu positions
            keyInput = None
            menuPosition = 0
            xoffset = 4
            yoffset = 3

            # Colors
            on = curses.A_REVERSE
            off = curses.A_NORMAL
            title = curses.A_BOLD

            # Loop until a selection is made with the Enter key
            while keyInput != ord('\n'):

                # Reset the screen and print the menu
                self.screen.clear()
                self.screen.border(0)
                self.screen.addstr(yoffset-2,xoffset-2, "Please select an option...", title)
                for i in range(0, len(self.services)):
                    self.screen.addstr(i+yoffset, xoffset, self.serviceDescriptions[i], off)

                # Reprint the selected line
                self.screen.addstr(menuPosition+yoffset, xoffset, self.serviceDescriptions[menuPosition], on)
                self.screen.refresh()

                # Get input by numeral or arrow key
                keyInput = self.screen.getch()

                # decide if it's a numeral
                try:
                    intKeyInput = int(chr(keyInput))
                    if intKeyInput in range(1,10):
                        if intKeyInput <= len(self.services):
                            menuPosition = intKeyInput - 1

                except:

                    # decide if it's a keyboard shortcut
                    for i in range(0, len(self.serviceShortcuts)):
                        if keyInput == self.serviceShortcuts[i]:
                            menuPosition = i

                    # decide if it's an arrow key
                    if keyInput == 258:
                        if menuPosition < (len(self.services) - 1):
                            menuPosition += 1
                        else:
                            menuPosition = 0
                    elif keyInput == 259:
                        if menuPosition > 0:
                            menuPosition -= 1
                        else:
                            menuPosition = len(self.services) - 1

                    # Visually punish the user for making a bad selection (optional)
                    #elif keyInput != ord('\n'):
                        #curses.flash()

            # Clean up and send the result home
            self.teardownWindow()
            return self.services[menuPosition]

        except:

            # Teardown in case there's a bug so we don't lock up the terminal
            self.teardownWindow()
            print("failed to get selection")
            print(sys.exc_info()[1])
            return self.services[len(self.services) - 1]

    def __init__(self, svcd, svc, svcsc):

        # General window setup tasks
        self.screen = curses.initscr()
        curses.noecho() # prevent the keystrokes from printing
        curses.cbreak() # keystrokes go immediately to the program
        self.screen.keypad(1) # something to do with arrow keys
        #curses.start_color() # make the background black (optional)

        # Adds the menu content
        self.serviceDescriptions = svcd
        self.services = svc
        self.serviceShortcuts = svcsc

