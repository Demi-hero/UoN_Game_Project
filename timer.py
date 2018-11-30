import time
starttime=time.time()
power_up = False
print(starttime)
while True:
    if (time.time() - starttime)//1 == 10 and not power_up:
        print("I am a power up")
        power_up = True
        starttime = time.time()
    elif (time.time() - starttime)//1 == 10 and  power_up:
        print("Powerup despawn?")
        starttime = time.time()
        power_up = False
