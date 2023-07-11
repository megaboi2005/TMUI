import msvcrt
import os
import sys
#clear screen before use
os.system("cls")

def keyinput():
    if msvcrt.kbhit():
        char = msvcrt.getch()
        if char == b'\xe0':  # Arrow key prefix
            char = msvcrt.getch()
            if char == b'H':  # Up arrow
                return "Up"
            elif char == b'P':  # Down arrow
                return "Down"
            elif char == b'M':  # Right arrow
                return "Right"
            elif char == b'K':  # Left arrow
                return "Left"
        elif char == b'\t':
             return "\t"
        elif char == b'\r':  # Enter key
            return "Enter"
 
        elif char == b'\x08':  # Backspace key
            return "Backspace"
        elif char and ord(char) < 32:  # Ctrl + key combination
            return "Ctrl+" + chr(ord(char) + 64)
        else:
            return char.decode()
    return None


class Colors:
    def __init__(self):
        #colors
        self.BLACK = "\033[0;30m"
        self.RED = "\033[0;31m"
        self.GREEN = "\033[0;32m"
        self.BROWN = "\033[0;33m"
        self.BLUE = "\033[0;34m"
        self.PURPLE = "\033[0;35m"
        self.CYAN = "\033[0;36m"
        self.LIGHT_GREY = "\033[0;37m"
        self.DARK_GREY = "\033[1;30m"
        self.LIGHT_RED = "\033[1;31m"
        self.LIGHT_GREEN = "\033[1;32m"
        self.YELLOW = "\033[1;33m"
        self.LIGHT_BLUE = "\033[1;34m"
        self.LIGHT_PURPLE = "\033[1;35m"
        self.LIGHT_CYAN = "\033[1;36m"
        self.LIGHT_WHITE = "\033[1;37m"
        #backgrounds
        self.BACK_BLACK =       "\033[0;40m"
        self.BACK_RED =         "\033[0;41m"
        self.BACK_GREEN =       "\033[0;42m"
        self.BACK_BROWN =       "\033[0;43m"
        self.BACK_BLUE =        "\033[0;44m"
        self.BACK_PURPLE =      "\033[0;45m"
        self.BACK_CYAN =        "\033[0;46m"
        self.BACK_LIGHT_GREY =  "\033[0;47m"
        self.BACK_DARK_GREY =   "\033[1;40m"
        self.BACK_LIGHT_RED =   "\033[1;41m"
        self.BACK_LIGHT_GREEN = "\033[1;42m"
        self.BACK_YELLOW =      "\033[1;43m"
        self.BACK_LIGHT_BLUE =  "\033[1;44m"
        self.BACK_LIGHT_PURPLE ="\033[1;45m"
        self.BACK_LIGHT_CYAN =  "\033[1;46m"
        self.BACK_LIGHT_WHITE = "\033[1;47m"        
        #formatting
        self.BOLD = "\033[1m"
        self.FAINT = "\033[2m"
        self.ITALIC = "\033[3m"
        self.UNDERLINE = "\033[4m"
        self.BLINK = "\033[5m"
        self.NEGATIVE = "\033[7m"
        self.CROSSED = "\033[9m"
        self.END = "\033[0m"


class Screen:
    def __init__(self):
        size = os.get_terminal_size()
        self.width = size.columns

        self.height = size.lines-2

        self.display = []

        
    
    def fillblank(self):
        size = os.get_terminal_size()
        self.width = size.columns
        self.height = size.lines-2
        for y in range(self.height): #{
            self.display.append([])

            for x in range(self.width): #{
                self.display[y].append(" ")
            #}
        #}

    def clear(self):
        self.display = []
            
    def refresh(self):
        sys.stdout.write('\033[?25l')
        output = ""
        for y in range(self.height):
            for x in range(self.width): 
                output += self.display[y][x]
            output += "\n"
        sys.stdout.write(f'\033[0;0H')
        sys.stdout.flush()
        print(output)


    def place(self,char,x,y,color="",endcolor=Colors().END):
        if len(char) > 1:
            return
        try:
            self.display[y][x] = color+char+endcolor
        except IndexError:
            return
    def print(self,string,x,y,backgroundcolor="",width=20,height=20):
        yoffset = 0
        widthoffset = 0
        for i in range(len(string)):
            try:
                if string[i] == "\n":
                    yoffset += 1
                    widthoffset = 0
                    continue                    
                if width == widthoffset:
                    yoffset += 1
                    widthoffset = 0
                if yoffset == height:
                    return
                self.display[y+yoffset][x+widthoffset] = backgroundcolor+string[i]+Colors().END
                widthoffset += 1
            except IndexError:
                pass



def Square(x,y,width,height,screen, variant="clear", bordercolor="",backgroundcolor="",text=""):
    screen.place("┌",x,y,bordercolor)
    for i in range(width-2):
        screen.place("─",x+i+1,y,bordercolor)
    screen.place("┐",x+width-1,y,bordercolor)
    if variant =="solid":
        for i in range(height-2):
            for a in range(width):
                screen.place(" ",x+a,y+i+1,backgroundcolor)
    for i in range(height-2):
        screen.place("│",x,y+i+1,bordercolor)
        screen.place("│",x+width-1,y+i+1,bordercolor)
    screen.place("└",x,y+height-1,bordercolor)
    for i in range(width-2):
        screen.place("─",x+i+1,y+height-1,bordercolor)
    screen.place("┘",x+width-1,y+height-1,bordercolor)
    if not text == "":
        screen.print(text,x+1,y+1,backgroundcolor,width-2,height-2)
    return

def Menu(x,y,width,height,screen,objects,selected,variant="clear",bordercolor="",backgroundcolor="",text=""):
    output = ""
    for i in range(len(objects)):
        if i == selected:
            output += "|"+objects[i]+ "|" +"\n"
        else:
            output += objects[i]+"\n"
    Square(x,y,width,height,screen,variant,bordercolor,backgroundcolor,output)

def inputcheck():
    return keyinput()
