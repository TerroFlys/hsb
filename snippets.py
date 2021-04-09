            print("getting screenshot")
            s = pg.screenshot()
            print("scanning")
            for x in range(s.width):
                print("nope2")
                for y in range(s.height):
                    print("color: " + str(color) + " | pixel: " + str(s.getpixel((x,y))))
                    if s.getpixel((x,y)) == color:
                        print("changing coords to closer ones")
                        temploc = [x ,y]
                        tempcalc = (temploc[0] - x) + (temploc[1] - y)
                        print("abs of tempcalc: " + str(abs(tempcalc)) + " <  lowest")
                        if(abs(tempcalc) < lowest):
                            lowest = tempcalc
                            coordsBlue[0] = temploc[0]
                            coordsBlue[1] = temploc[1]
                            #print("lowest value = " + str(lowest) + " || coords x:" + str(coordsBlue[0]) + " y: " + str(coordsBlue[1]))


    print("locating blue")
    for i in pg.locateAllOnScreen(images_path + images["bluebutton"]):
        print(str(i))
    sleep(0.5)
    print("moving and clicking location x: " + str(coordsBlue[0]) + " y: " + str(coordsBlue[1]) )
    autopy.mouse.move(coordsBlue[0], coordsBlue[1])
    sleep(0.1)
    autopy.mouse.click()
    sleep(5)
except Exception as e:
    raise
    print("something went wrong trying to get/click the blue pixel")
