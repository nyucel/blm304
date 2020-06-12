"""
    ========================= Veri Haberleşmesi Vize Ödevi ========================
    İsim ve Soyisim: Augusto GOMES JUNIOR
    Ögrenci_No: 130401074
"""

import os, time 
def list_directory(path):
    print( "CWD:", path)
    try:
        ld = os.listdir(path)
        if not len(ld):
            max_length = 0
        else:
           max_length = len(max(ld, key=len))
           hd = '| %*s | %9s | %12s | %20s | %11s | %12s |' % (max_length, 'Name', 'Filetype', 'Filesize', 'Last Modified', 'Permission', 'User/Group')
           tb = '%s\n%s\n%s\n' % ('-' * len(hd), hd, '-' * len(hd))
           data = str("")
           for i in ld:
                path = os.path.join(path, i)
                stat = os.stat(path)
                data += '| %*s | %9s | %12s | %20s | %11s | %12s |\n' % (max_length, i, 'Directory' if os.path.isdir(path) else 'File',
                str(stat.st_size) + 'B', time.strftime('%b %d, %Y %H:%M', time.localtime(stat.st_mtime)),
                oct(stat.st_mode)[-4:], str(stat.st_uid) + '/' + str(stat.st_gid))
           ft = '%s\n' % ('-' * len(hd))
           return tb + data + ft
    except Exception as e:
        return None
        print(str(e))



ld = list_directory("/home")
if ld:
    print(ld)
else:
    print("Dosya bostur.")
