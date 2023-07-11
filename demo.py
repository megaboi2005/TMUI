import tmui
import time
import math
#create screen
screen = tmui.Screen()

frame = 1
timenow = 0
sizex = 5
sizey = 5
while True:
    #get input
    key=tmui.inputcheck()
    #reset the screen
    screen.clear()
    screen.fillblank()
    
    #flashes every frame
    if (frame%3) > 1:
        tmui.Square(50,0,21,5,screen,text="flashes every frame")
    frame += 1

    #limit to 60 fps
    time.sleep(1/70)

    #calculate the fps
    try:
        fps = 1/(time.time()-timenow)
    except:
        fps=fps
        
    timenow = time.time()

    #input
    match key:
        case "Right":
            sizex += 1
        case "Left":
            sizex -= 1
        case "Up":
            sizey += 1
        case "Down":
            sizey -= 1

    #           width height
    #           x,y,^ ,^ ,screen,optional text
    tmui.Square(10,10,25,3,screen,text=str(frame))
    
    #frame printer


    #fps
    tmui.Square(0,0,25,3,screen,text=str(math.floor(fps)),bordercolor=tmui.Colors().RED)

    #input + text renderer
    tmui.Square(71,0,sizex,sizey,screen,text="The text adapts to the squares width (won't show if the box is too small)",bordercolor=tmui.Colors().GREEN)

    #clear boxes
    tmui.Square(0,20,11,5,screen,text="clear box")
    tmui.Square(3,22,11,5,screen,text="clear box")

    #solid boxes
    tmui.Square(20,20,11,5,screen,variant="solid",text="solid box")
    tmui.Square(23,22,11,5,screen,variant="solid",text="solid box")

    #refresh and display in terminal.
    screen.refresh()