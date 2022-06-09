from datetime import date

today = date.today()
print("Today's date:", today)

import os
#
path = [
    str(os.path.join(r'C:\..\Kimonaim\shufersal', str(today))),
    str(os.path.join(r'C:\..\Kimonaim\ramiLevi', str(today))),
    str(os.path.join(r'C:\..\Kimonaim\victory', str(today)))

]

import gzip, shutil

for p in path:
    os.chdir(p)
    gzfiles = []
    for file in os.listdir(os.getcwd()):
        if file.endswith(".gz"):
            gzfiles.append(file)
    print(gzfiles)
    for gz_file in gzfiles:
        with gzip.open(gz_file, 'rb') as f_in:
            with open(gz_file[:-3] + '.xml', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            print(gz_file[:-3] + '.xml')
        os.unlink(gz_file)
