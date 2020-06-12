#Batuhan :OZALP - 170401074
import time
import datetime
import socket

zaman_dilimi = +3

def main():
#    try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 142))
    s.listen(5)
    print("Istenen zaman dilimi >>", zaman_dilimi)
    
    u = str(datetime.datetime.utcnow())
    v = str(datetime.datetime.now())#pc saati
    
    zaman = time.time() 
    print("Server zamani >>", time.ctime(zaman))
    sss, address = s.accept()
    sss.send(str(zaman).encode())  
    u=str(u)
    u = u.split()
    print("UTC 0 zaman >>", datetime.datetime.utcnow())
    m1 = u[1].split(":")
    v = v.split()
    m2 = v[1].split(":")
    mm2 = int(m2[0])
    mm1 = int(m1[0])
    utc = mm2 - mm1
    
    time.sleep(0.3)
    sss.send(str(utc).encode())
    if(utc > 0):
        utc = str(utc)
        print("Server zaman dilimi >> UTC+%s" %utc)
    else:
        utc = str(utc)
        print("Server zaman dilimi >> UTC%s" %utc)
    
    time.sleep(0.3)
    sss.send(str(zaman_dilimi).encode())
#    except:
#    print("Hata")
    s.close()
main()












