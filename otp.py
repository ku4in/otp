
'''
One time password generator
'''

import pyotp
import subprocess
import sys

confname = '.otp.conf'
fnames = list(map(str.strip, open(confname).readlines()))

# .otp.conf should contain paths to gpg encrypted files like
# /root/.password-store/gov/gosuslugi.ru.gpg
# /root/.password-store/inet/github.com.gpg
# ...
# gpg file should contain in any place the string with a secret in format
# secret: discription : key
# secret: Gosuslugi.ru (mail@example.com): XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

for fname in fnames:
    if fname.endswith(".gpg"):
        batcmd=f"gpg2 -q -d {fname}"
        result = subprocess.check_output(batcmd, shell=True)
        data = result.decode()
    else:
        data = open(fname).read()

    for line in data.split('\n'):
        if "secret" in line:
            spl = line.split(':')
            name = spl[1].strip()
            secret = spl[2].strip()
            break

    t = pyotp.TOTP(secret)
    print(f"{name:<29}:  {t.now()}")
