# ライブラリのインポート
from pypdf import PdfReader
import main 
import re
import datetime
import core
import unicodedata


def pdf_to_text(pdf_path):
    # PDFファイルの読み込み
    reader = PdfReader(pdf_path)

    # ページ数の取得
    number_of_pages = len(reader.pages)

    # ページの取得。この場合は、1ページ目を取得する。
    page = reader.pages[0]

    # テキストの抽出
    text = page.extract_text()
    
    with open(f"{pdf_path}.txt", 'w', encoding="utf-8",errors='ignore') as f:
        f.write(unicodedata.normalize('NFKC',text))
        
    return unicodedata.normalize('NFKC',text)

def Test():
    # テスト用のPDFファイルのパス
    pdf_path = input("PDFファイルのパスを入力してください: ")

    # PDFからテキストを抽出
    text = pdf_to_text(pdf_path)

    # 抽出したテキストを表示
    print(text)



def pdf_to_student(pdf_path):
    text = pdf_to_text(pdf_path)

    # テキストを行ごとに分割
    lines = text.split('\n')

    stu = core.Student()

    rawaddress = ""

    for line in lines:
        match line:
            case l if "氏名ふりがな" in l:
                stu.nameKana = l.replace("氏名ふりがな", "").strip()
            case l if "氏名" in l:
                stu.name = l.replace("氏名", "").strip()
            case l if "学籍番号" in l:
                stu.id = l.replace("学籍番号", "").strip()
            case l if "学年" in l:
                greadTmp = l.replace("学年", "").strip()
                print(greadTmp)
                if "B" in greadTmp or "学部" in greadTmp:
                    greadTmp = greadTmp.replace("B","").replace("学部","")
                elif  "M" in greadTmp or  "修士" in greadTmp:
                    greadTmp = greadTmp.replace("M","").replace("修士","")
                    stu.gread = 4
                elif  "D" in greadTmp or  "博士" in greadTmp:
                    greadTmp = greadTmp.replace("D","").replace("博士","")
                    stu.gread = 6                    
                stu.gread = stu.gread + int(greadTmp.replace("年","").strip())
            case l if "学部・学科" in l:
                stu.major = l.replace("学部・学科", "").strip()
            case l if "生年月日" in l:
                stu.birth = core.date_to_str(l.replace("生年月日", "").strip())
            case l if "携帯" in l:
                number = l.replace("携帯TEL", "").strip()
                number = number.replace("-","")
                stu.phone_number = f"{number[0:3]}-{number[3:7]}-{number[7:11]}"
            case l if "メールアドレス" in l:
                stu.email = l.replace("メールアドレス", "").strip()
            case l if "現住所" in l:
                rawaddress = l.replace("現住所", "").strip()
                rawaddress += "\n"
                rawaddress += lines[lines.index(l) + 1].replace("現住所", "").strip()
    
    # 住所
    stu.SetAddress(rawaddress)
    
    # 学部
    stu.SpilitFac()

    stu.file_path = pdf_path

    return stu

if __name__ == "__main__":
    Test()
