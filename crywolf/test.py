from random import choices

alphaNum = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

codes = []

while len(codes) < 101:
    temp = choices(alphaNum,k=6)
    code=""
    for char in temp:
        code+=char
    if code not in codes:
        codes.append(code)


