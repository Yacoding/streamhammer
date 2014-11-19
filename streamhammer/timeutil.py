
import time

def microsleep(microsec):
    time.sleep(microsec / 1000000.0)

def timediffms(t1, t2):
    # compute t1 in milliseconds
    v1 = 1000 * ((t1.day * 86400) + (t1.hour * 3600) + (t1.minute * 60) + t1.second)
    v1 += (t1.microsecond / 1000)
    # compute t2 in milliseconds
    v2 = 1000 * ((t2.day * 86400) + (t2.hour * 3600) + (t2.minute * 60) + t2.second)
    v2 += (t2.microsecond / 1000)
    # Return difference in milliseconds
    return v2 - v1
