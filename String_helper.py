split = [
    "（","）","「","」","【","】","『","』","＜","＞","《","》","［","］","〔","〕","≪","≫","”","‘","’","・",".",",","'",'"',"…"
]

def Spilit(obj : str):
    result = []
    tmp = []
    for c in split:
        for b in result:
            tmp.append(b)
        result = []
        for a in tmp:
            result.extend(str(a).split(c))
        tmp = []
    return result

def Replace(obj :str , newchar :str):
    result = obj
    for c in split:
        result = result.replace(c,newchar)
    return result