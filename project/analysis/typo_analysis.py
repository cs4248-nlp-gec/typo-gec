import difflib
from pprint import pprint

text1 = "It has to a high density population because its small territory".split()
text2 = "It hgas a high densuty populqtion because is smwll terrifory".split()

d = difflib.Differ()
res = list(d.compare(text2, text1))
pprint(res)