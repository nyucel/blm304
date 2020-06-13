
import socket
import time
from datetime import datetime, timezone, timedelta
import sys


host = input( "\nServerin IP adresini giriniz : " )
port = 142
UTC = +2


def gecikme_farki( client_control ):

    first = datetime.utcnow() + timedelta(hours = UTC)
    client_control.send( bytes( str( first ), encoding='utf-8' ) )
    
    kontrol = client_control.recv( 128 )
    
    end = datetime.utcnow() + timedelta( hours = UTC )
    gecikme_farki = (end - first) / 2
    
    print( "\nGecikme farki : ", gecikme_farki )

    return gecikme_farki


with socket.socket() as s:

    try:
    
        s.bind((host, port))
        
    except:
    
        print( "\n-----------HATALI ISLEM--------------\n" )
        sys.exit()

    print( "\n---------------SUNUCU CALISIYOR------------------" )
    
    while True:
    
        s.listen()
        connection, addr = s.accept()
        
        with connection:
        
            while True:
            
                data = connection.recv( 128 )
                if not data:
                    break
                    
                gecikme_farki = gecikme_farki( connection )
                time = datetime.utcnow() + timedelta(hours = UTC) + gecikme_farki
                
                print ("aaa", time)

                time_and_timezone = []
                time_and_timezone.append(UTC)
                time_and_timezone.append(str( time ))

                connection.send( bytes( str(time_and_timezone) , encoding='utf-8' ) ) 
                
    s.close()