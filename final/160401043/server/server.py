

# HAZIRLAYAN
# ERENAY TOSUN - 160401043


import socket
import time
from datetime import datetime, timezone, timedelta
import sys


host = input( "\nServer'ın IP adresini giriniz: " )
port = 142
UTC = +3


def gecikmeSuresiHesaplama( client_control ):

    first = datetime.utcnow() + timedelta(hours = UTC)
    client_control.send( bytes( str( first ), encoding='utf-8' ) )
    
    kontrol = client_control.recv( 128 )
    
    end = datetime.utcnow() + timedelta( hours = UTC )
    gecikme_suresi = (end - first) / 2
    
    print( "\nToplam gecikme süresi: ", gecikme_suresi )
    return gecikme_suresi


with socket.socket() as s:

    try:
    
        s.bind((host, port))
        
    except:
    
        print( "\n-----------ISLEM BASARISIZ--------------\n" )
        sys.exit()

    print( "\n---------------SUNUCU CALISTIRILDI------------------" )
    
    while True:
    
        s.listen()
        connection, addr = s.accept()
        
        with connection:
        
            while True:
            
                data = connection.recv( 128 )
                if not data:
                    break
                    
                gecikme_suresi = gecikmeSuresiHesaplama( connection )
                time = datetime.utcnow() + timedelta(hours = UTC) + gecikme_suresi
                
                connection.send( bytes( str( time ), encoding='utf-8' ) ) 
                
    s.close()        
                
                
                
