import os
import binascii

print(binascii.hexlify(os.urandom(25)))
#first try
'dd1f46b3779db044f8c0f89e36c486baaa84c2e9ff853d6c42'