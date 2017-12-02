from json import dumps
from re import findall
res = {}
for str in open("kb.txt").readlines():
    try:
        a, b, c = findall(r'.*?"(.*?)".*?"(.*?)".*?"(.*?)".*', str.lower())[0]
        res.update({(a,c,b):1})
    except ValueError:
        pass
    except TypeError:
        pass
    except IndexError:
        pass
# print(dumps(res, ensure_ascii = 0, indent = 4))
