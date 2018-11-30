import time
starttime=time.time()
while True:
    if (time.time() - starttime)//1 == 10:
        print(" I am a power up")
        starttime = time.time()

    #print((time.time() - starttime)//1)
