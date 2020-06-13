import socket
import os
import time


host = input( "\nBaglanilacak Hedef Sunucunun IP'sini giriniz : " )
port = 142

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((host, port))
    s.send( bytes( "gecikme_suresi", encoding='utf-8' ) )
    
    register = s.recv( 128 )
    s.send( bytes( "client", encoding='utf-8' ) )
    time = s.recv( 128 )

    time_and_timezone = (time.decode( "utf-8" ))

    characters_to_remove = "[]'"
    for character in characters_to_remove:
    	time_and_timezone = time_and_timezone.replace(character, "")

    timezone = time_and_timezone.split(',')[0]
    time = time_and_timezone.split(',')[1]

    os.system( 'date --set "%s" +\"%%A %%d %%B %%Y %%H:%%M:%%S.%%6N\"' % time )
    
    s.close()