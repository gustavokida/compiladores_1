
arq = "exemplo.lalg.txt"

text = ''
with open(arq) as f:
    text = f.read()
    f.close()
# for c in range(len(text)):
#     if c+1 < len(text):
#         print(text[c+1])

