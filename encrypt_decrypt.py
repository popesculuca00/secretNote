import hashlib
from itertools import cycle
import base64

class encoder:
    def __init__(self, name):
        pass

        res = hashlib.sha1()
        name = name.encode('UTF-8')
        res.update(name)

        self.hash = res.hexdigest()

        #self.hash = int(self.hash, 16)



    def get_enc_text(self, text):

        #return str(base64.b64encode(text.encode("UTF-8")))
        return text

        #encrypted = ''.join(chr(ord(x) ^ ord(y)) for (x, y) in zip(text, cycle(self.hash)))
        #return encrypted

    def get_dec_text(self, text):
        #text = text[1:len(text)-2]
        #return str(base64.b64decode(text))
        return text
#
        #decrypted = ''.join(chr(ord(x) ^ ord(y)) for (x, y) in zip(text, cycle(self.hash)))
        #return decrypted
#

if __name__ == "__main__":
    a = encoder("Luca")
    b = a.get_enc_text("aa")
    print(b)
    b = a.get_dec_text(b)
    print(f"Decrypted:\n{b}" )

    encrypted = a.get_enc_text("SSSALUT")
    print( encrypted )
