def readFile(file):
    with open(file,'r', encoding='utf-8') as F:
        txt = F.readlines()
        return ''.join(txt),txt