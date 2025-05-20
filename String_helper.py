"""
@file String_helper.py
@brief 文字列操作を補助する関数を提供します。
@details 特定の文字での分割や置換を行う関数が含まれています。
"""

split = [
    "（","）","「","」","【","】","『","』","＜","＞","《","》","［","］","〔","〕","≪","≫","”","‘","’","・",".",",","'",'"',"…"
]

def Spilit(obj : str):
    """
    @brief 指定された文字で文字列を分割します。
    @param obj (str): 分割する文字列。
    @return (list): 分割された文字列のリスト。
    @details 複数の区切り文字を使用して文字列を分割します。
    """
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
    """
    @brief 指定された文字を別の文字に置換します。
    @param obj (str): 置換を行う文字列。
    @param newchar (str): 置換後の文字。
    @return (str): 置換後の文字列。
    @details 複数の文字を一括で置換します。
    """
    result = obj
    for c in split:
        result = result.replace(c,newchar)
    return result