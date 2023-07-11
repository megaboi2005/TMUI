import tmui
import time
import random
import os
import datetime
screen = tmui.Screen()

helpscr = """
save:
    ctrl+s
close:
    ctrl+q
"""
global text
global textfilename

def getline(position, text):
    lines = text.split("\n")
    line_index = 0
    character_count = 0
    for line in lines:
        character_count += len(line) + 1  # Add 1 for the newline character
        if character_count > position:
            break
        line_index += 1
    return line_index + 1  # Adjust line index by adding 1

def getcolumn(position, text):
    lines = text.split("\n")
    line_index = 0
    character_count = 0
    for line in lines:
        character_count += len(line) + 1  # Add 1 for the newline character
        if character_count > position:
            break
        line_index += 1
    line = lines[line_index]
    column = position - (character_count - len(line)) + 1
    return column

def movecursor(variable,position):
    if variable == 1:
        textsplit = text.split("\n")
        size = len(textsplit[getline(position,text)-1])
        return size + 1
    elif variable == -1:
        textsplit = text.split("\n")
        size = len(textsplit[getline(position,text)+1])
        return -size

#def movecursor(position,direction):
#    if direction == 1:
#        line = getline(position,text)
#        textsplit = text.split("\n")
#        size = 0
#        for i in range(line):
#            size += len(textsplit[i])
#        
#        return position - size + get_column(position,text)


def openfile():
    selected = 0
    global text
    global textfilename
    objects = os.listdir()
    while True:
        key=tmui.inputcheck()
        screen.clear()
        screen.fillblank()
        
        match key:
            case "Right":
                selected+=1
            case "Left":
                selected-=1
            case "Up":
                selected-=1
            case "Down":
                selected+=1
            case "Enter":
                textfilename = objects[selected]
                text = open(objects[selected],"r").read()
                return editor()
            case _:
                if not key == None:
                    pass

        if selected <= 0:
            selected = len(objects)
        if selected > len(objects)-1:
            selected = 0
        
        filestats = f"""
Filename:\n{objects[selected]}

Size:\n{os.path.getsize(objects[selected])} bytes

Last modified:\n{datetime.datetime.fromtimestamp(os.path.getmtime(objects[selected])).strftime('%Y-%m-%d %H:%M:%S')}

                    """

        tmui.Menu(25,0,screen.width-25,screen.height,screen,objects,selected)
        tmui.Square(0,0,25,screen.height,screen,text=filestats)
        tmui.Square(133,0,screen.width-133,3,screen,"solid",tmui.Colors().YELLOW,tmui.Colors().BACK_GREEN,"MegPad")
        screen.refresh()


def editor():
    global text
    global textfilename
    timenow=0
    #text = open("text.txt","r").read()
    cursorloc = 0
    cursorarrayloc = 0
    scroll =  0
    scrolloffset = 0 
    frame = 0
    cursorhide = False
    cursor = "│"
    cursorcolor = tmui.Colors().GREEN
    editcount = 0
    while True:
        frame+=1
        if frame == 20:
            frame = 0
            if cursorhide:
                cursor = ""
                cursorhide = False
            else:
                cursor = "│"
                cursorhide = True
        key=tmui.inputcheck()
        screen.clear()
        screen.fillblank()
        try:
            fps = 1/(time.time()-timenow)

        except:
            fps=fps

        timenow = time.time()
        time.sleep(1/60)
        #screen.print("FPS: "+str(fps),0,0)
        tabname = ""
        if editcount > 0:
            tabname = textfilename + "*"
        else:
            tabname = textfilename
        match key:
            case "Right":
                cursorloc += 1
                cursor = "│"
            case "Left":
                cursorloc -= 1
                cursor = "│"
            case "Up":
                cursorloc -= movecursor(-1,cursorloc)
            case "Down":
                cursorloc += movecursor(1,cursorloc)
                
            case "Backspace":
                text = text[:cursorloc-1] + text[cursorloc:]
                #text += key
                cursor = "🗑"
                cursorloc -= 1
                editcount+=1
            case "Enter":
                text = text[:cursorloc] + "\n" + text[cursorloc:]
                #text += key
                cursorloc += 1
                #scroll += 1
                editcount+=1
            case "Ctrl+S":
                with open(textfilename,"w") as textwrite:
                    textwrite.write(text)
                    editcount = 0
            case "Ctrl+Q":
                return openfile()
            case _:
                if str(key).startswith("Ctrl+"):
                    continue
                if not key == None:
                    text = text[:cursorloc] + str(key) + text[cursorloc:]
                    editcount+=1
                    #text += key
                    cursorloc += 1

        if cursorloc > len(text) or cursorloc < 0:
            cursorloc = len(text)

        while scroll+screen.height-5 < getline(cursorloc,text):
            scroll += 1

        while scroll+1 > getline(cursorloc,text): 
            scroll -= 1

        listdir = os.listdir()
        listed = ""
        for i in listdir:
            if os.path.isdir(i):
                listed += i + "\n"
            else:
                listed += "-"+i+"\n"
        cursorinc = text
        cursorinc = cursorinc[:cursorloc] + cursor + cursorinc[cursorloc:]
        ruler = cursorinc.split("\n")
        textout = ""
        for i in range(len(ruler)):
            try:
                textout += str(i+scroll+1) + "    |" + ruler[i+scroll] + "\n"
            except:
                pass



        tmui.Square(0,0,20,screen.height,screen,"solid",tmui.Colors().LIGHT_WHITE,tmui.Colors().BACK_BLACK,listed)
        tmui.Square(20,0,screen.width-35,3,screen,"solid",tmui.Colors().LIGHT_WHITE,tmui.Colors().BACK_BLACK,tabname)
        tmui.Square(133,0,screen.width-133,3,screen,"solid",tmui.Colors().YELLOW,tmui.Colors().BACK_GREEN,"MegPad")
        tmui.Square(133,3,screen.width-133,screen.height-3,screen,"solid",tmui.Colors().YELLOW,tmui.Colors().BACK_GREEN,helpscr)
        tmui.Square(20,3,screen.width-35,screen.height-3,screen,"solid",tmui.Colors().LIGHT_WHITE,tmui.Colors().BACK_DARK_GREY,textout.replace("\t","   "))
        #screen.print("FPS: "+str(fps),0,0)
        screen.refresh()
    
openfile()