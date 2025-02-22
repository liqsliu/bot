import logging

logger = logging.getLogger(__name__)
mp = logger.warning



# https://github.com/hustcc/xmorse/blob/master/src/const.ts

STANDARD = {
  'A': '01' ,
  'B': '1000' ,
  'C': '1010' ,
  'D': '100' ,
  'E': '0' ,
  'F': '0010' ,
  'G': '110' ,
  'H': '0000' ,
  'I': '00' ,
  'J': '0111' ,
  'K': '101' ,
  'L': '0100' ,
  'M': '11' ,
  'N': '10' ,
  'O': '111' ,
  'P': '0110' ,
  'Q': '1101' ,
  'R': '010' ,
  'S': '000' ,
  'T': '1' ,
  'U': '001' ,
  'V': '0001' ,
  'W': '011' ,
  'X': '1001' ,
  'Y': '1011' ,
  'Z': '1100' ,
  '0': '11111' ,
  '1': '01111' ,
  '2': '00111' ,
  '3': '00011' ,
  '4': '00001' ,
  '5': '00000' ,
  '6': '10000' ,
  '7': '11000' ,
  '8': '11100' ,
  '9': '11110' ,
  '.': '010101' ,
  ',': '110011' ,
  '?': '001100' ,
  "'": '011110' ,
  '!': '101011' ,
  '/': '10010' ,
  '(': '10110' ,
  ')': '101101' ,
  '&': '01000' ,
  ':': '111000' ,
  ';': '101010' ,
  '=': '10001' ,
  '+': '01010' ,
  '-': '100001' ,
  '_': '001101' ,
  '"': '010010' ,
  '$': '0001001' ,
  '@': '011010' 
}





space = '/'
short = '.'
long = '-'

STANDARD = dict(zip(STANDARD.keys(), (i.replace("0", short).replace("1", long) for i in STANDARD.values())))
# print(STANDARD)
REVERSED_STANDARD = dict(zip(STANDARD.values(),STANDARD.keys()))


def replace(data):
    return data.replace("0", short).replace("1", long)

def get_bin(data):
    return data.replace(short, "0").replace(long, "1")


def encode(msg):
    msg = msg.replace(' ', '') # need fix
    tmp = ""
    msg = msg.upper()
    for c in msg:
        if c in STANDARD:
            tmp += STANDARD[c]
        else:
#            if ord(c) < 128:
            if ord(c) < 256:
                tmp += replace(format(ord(c), "b"))
            else:
                tmp += format(int(ascii(c)[3:-1], 16), "b").replace("0", short).replace("1", long)
        tmp += space
    return tmp.rstrip(space)


def decode(data):
    data = data.split(space)
    tmp = ""
    for c in data:
        if c in REVERSED_STANDARD:
            tmp += REVERSED_STANDARD[c]
        else:
            if c.replace(short, "").replace(long, ""):
                return tmp
            t = int(get_bin(c), 2)
            if t < 256:
                tmp += chr(t)
            else:
                try:
                    tmp += (r"\u" + hex(t)[2:]).encode().decode("unicode_escape")
                except UnicodeDecodeError as e:
                    return tmp
    return tmp.rstrip(space)





if __name__ == '__main__':
    print('{} 作为主程序运行'.format(__file__))
    encode("test")
    encode("I LOVE YOU 我爱你")
    decode('../.-../---/...-/./-.--/---/..-/-/---/---/--...-....-...-/-..---..-.-----/---..-...--...-/-..----.--.....')

else:
    print('{} 运行'.format(__file__))
