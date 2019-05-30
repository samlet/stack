import clipboard
import shortuuid
import time
import uuid
import string

def get_from_clip():
    text = clipboard.paste()
    text=text.replace("\n", "")
    return text
    
def to_clip(sentence):
    clipboard.copy(sentence)

def get_unique_base_time():
    u = uuid.uuid4()
    s = shortuuid.encode(u)
    short = s[:7]
    epoch = time.time()
    unique_id = "%s_%d" % (short, epoch)
    return unique_id

'''
print isEnglish('slabiky, ale liší se podle významu')
print isEnglish('English')
print isEnglish('ގެ ފުރަތަމަ ދެ އަކުރު ކަ')
print isEnglish('how about this one : 通 asfަ')
print isEnglish('?fd4))45s&')
print isEnglish('Текст на русском')

> False
> True
> False
> False
> True
> False
'''
def is_english(s):
    return s.translate(string.punctuation).isalnum()

ascii = set(string.printable)   
def remove_non_ascii(s):
    return list(filter(lambda x: x in ascii, s))
def is_ascii(ch):
    return (ch in ascii)

def write_to(outfilename, cnt):
    outfile = open(outfilename, "w")
    outfile.write(cnt)
    outfile.close()

