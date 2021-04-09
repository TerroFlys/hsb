import pyautogui as pg
from time import sleep
from random import randint
import pydirectinput as pdi
import autopy
import sys
#import ReadWriteMemory
import pymem
import pymem.process
import psutil
#Ctypes ??


window_position = [0,0]
images_path = "images/"
images = {"logo1": "hslogo1.png",
"logo2": "hslogo2.png",
"restart": "restart.png",
"reset": "vote-reset.png",
"bluebutton": "blue.png"
}
destinations = { "MosDesert": 15,
"pyramid1": 16
}

name = "Hero_Siege"
#exe_name = "Hero_Siege.exe"
#axPointer = {"x": "Hero_Siege.exe+8617BCC", "y": "Hero_Siege.exe+8618260"}
Pointer_x = (0x8617BCC)
Pointer_y = (0x8618260)
mapwait = 7
rs_wait = 5
patience = 2


move = { "right": 'd', 
"left": 'a',
"up": 'w',
"down": 's',
"jump": 'space',
"use": 'f'
}
attack_dir = {"right": "right", #direction keys for base attacks
"left": "left",
"up": "up",
"down": "down"

}
ability_keys = {"shield": "3", # ability keys
"buff": "4",
"att1": "1",
"att2": "2"
}
ability_cd { "shield": "0",  #cooldowns
"buff": "10",
"att1": "5"
"att2": "4",
"global": "1"
}


def locate_game():
    try:
        return (pg.locateCenterOnScreen(images_path + images["logo1"]))
    except Exception as e:
        raise
        print("hslogo1 not found")
        try:
            return (pg.locateCenterOnScreen(images_path + images["logo2"]))

        except Exception as e:
            raise
            print("hslogo2 not found")

def reset_game(windowPos):
    #windowPos[0] = windowPos[0] + 960
    #windowPos[1] = windowPos[1] + 540 #sets positions to the middle of the screen
    print("Clicking the screen")
    pg.click(windowPos[0] + 10, windowPos[1]) # clicking next to the logo
    sleep(0.1)
    pg.moveRel(0, 50, 1)
    sleep(0.2 + (randint(0,1000)/10000))
    print("Pressing escape down")
    pdi.keyDown('esc')
    sleep(0.1 + (randint(0,1000)/10000))
    print("releasing escape")
    pdi.keyUp('esc')
    sleep(1)
    #Single Player  Testing here
    try:
        loc = pg.locateCenterOnScreen(images_path + images["restart"])
    except Exception as e:
        raise
        print("Did not find single player reset button.")
        try:
            loc = pg.locateCenterOnScreen(images_path + images["reset"])
        except Exception as e:
            raise
            print("Did not find Online reset button. Closing...")
            sys.exit(0)
    print("Clicking reset")
    pdi.moveTo(loc[0],loc[1], 0.2)
    autopy.mouse.click()
    sleep(0.2)
    autopy.mouse.click()
    print('waiting for reset to complete (' + str(rs_wait) + ' seconds)')
    sleep(rs_wait)

def goto_waypoint(windowPos):
    begin = [windowPos[0], windowPos[1]]
    coordsOne = [1101 + windowPos[0], 546 + windowPos[1]] #1485 - 336
    coordsTwo = [969 + windowPos[0], 796 + windowPos[1]]
    print("moving to first coords. x: " + str(coordsOne[0]) + " y: " + str(coordsOne[1]))
    autopy.mouse.move(coordsOne[0], coordsOne[1])
    sleep(0.1)
    autopy.mouse.click(autopy.mouse.Button.RIGHT)
    sleep(1)
    print("moving to second coords. x: " + str(coordsTwo[0]) + " y: " + str(coordsTwo[1]))
    autopy.mouse.move(coordsTwo[0], coordsTwo[1])
    sleep(0.1)
    autopy.mouse.click(autopy.mouse.Button.RIGHT) ####1305-336, 971-175
    sleep(1)
    print("on waypoint.")

def use_waypoint(destination, move):
    sleep(0.2)
    print('tapping ' + move["use"])
    pdi.press(move["use"])
    sleep(0.7)
    print("locating destination")
    try:
        for i in range(destination):
            pdi.press(move["right"])
        sleep(0.4)
        print("traveling")
        pdi.press(move["use"])
        print("waiting for map load (+ " +  str(mapwait) +" seconds)")
        sleep(mapwait)
    except Exception as e:
        raise
        print("something went wrong locating/travveling to destination")

def activate_shields(shield_key):
    pdi.press(shield_key)

def get_pid(name):
    try:
        for proc in psutil.process_iter():
            if name in proc.name():
                pid = proc.pid
                return pid
    except:
        raise
        print("Could not find process ID")
def get_name(pid):
    try:
        for proc in psutil.process_iter():
            if pid == proc.pid:
                return proc.name()
    except:
        raise
        print("Could not find name of pid")


def get_playerX(pm, client, point):
    x = pm.read_float(client + point)
    return x
def get_playerY(pm, client, point):
        y = pm.read_float(client + point)
        return y
def move_player(moveKey, pointx, pointy):
    curr = True
    while curr == True:
        sleep(0.05)
        old_x = get_playerX(pm, client, pointx)
        old_y = get_playerY(pm, client, pointy)
        coords = [old_x, old_y]
        pdi.keyDown(moveKey)
        for i in range(10):
            sleep(patience / 10) #waits abit
        pdi.keyUp(moveKey)
        new_x = get_playerX(pm, client, pointx)
        new_y = get_playerY(pm, client, pointy)
        new_coords = [new_x, new_y]
        if(new_coords == coords): #compares old coords with new ones to check if player is in place
            curr = False
            print("move " + str(moveKey) + " is at the same coords")
            break

def move_handler(pm, client, pointx, pointy):
    x = get_playerX(pm, client, pointx)
    y = get_playerY(pm, client, pointy)
    coords = [x,y]
    move_player(move["right"], pointx, pointy)
    move_player(move["up"], pointx, pointy)
    move_player(move["left"], pointx, pointy)
    move_player(move["down"], pointx, pointy)
    new_x =  get_playerX(pm, client, pointx)
    new_y = get_playerY(pm, client, pointy)
    newcoords = [new_x, new_y]
    if(coords == newcoords):
        wpos = locate_game()
        reset_game(wpos):


sleep(0.1)
PROCESS_ID = get_pid(name) #base name what its supposed te be put in to get PID
print("ProcessID: " + str(PROCESS_ID))
if(PROCESS_ID == None): #checks if a process has been found
    print("Process not found")
    sys.exit(1)
name = get_name(PROCESS_ID) #transforms name to the exact name.exe
pm = pymem.Pymem(name)
client = pymem.process.module_from_name(pm.process_handle, name).lpBaseOfDll
print("Exe Name: " + str(name) + " | heroProcess: " + str(client))
move_handler(pm, client, Pointer_x, Pointer_y)



#window = locate_game()
#window_position[0] = window[0]
#window_position[1] = window[1]

#reset_game(window_position)
#goto_waypoint(window_position)
#use_waypoint(destinations["MosDesert"],move)
#activate_shields(ability_keys["shield"])
        #Hero_Siege.exe+8618260 Y
        #Hero_Siege.exe+8617BCC X


print("Stopped")
