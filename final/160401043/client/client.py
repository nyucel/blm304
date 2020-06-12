

# HAZIRLAYAN
# ERENAY TOSUN - 160401043


import socket
import os


host = input( "\nHedef Sunucu IP'sini giriniz: " ) 
port = 142

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((host, port))
    s.send( bytes( "gecikme_suresi", encoding='utf-8' ) )
    
    register = s.recv( 128 )
    s.send( bytes( "client", encoding='utf-8' ) )
    time = s.recv( 128 )
    print( time )
    
    os.system( 'date --set "%s" +\"%%A %%d %%B %%Y %%H:%%M:%%S.%%6N\"' % time.decode( "utf-8" ) )
    
    s.close()
