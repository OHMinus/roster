import core
import pdf
import os
import glob

def Main(input_dir, output_file, encoding="utf-8"):

    # ディレクトリ内のPDFファイルを読み込む
    students = core.loadDir(input_dir)

    # 学生情報をCSV形式で保存する
    # CSVファイルのヘッダー
    header = core.Student.GetHeader()

    # CSVファイルにヘッダーを書き込む
    with open(output_file + "output.csv", 'w', encoding=encoding,errors='ignore') as f:
        f.write(','.join(header.values()) + '\n')
        # 学生情報をCSV形式で保存する
        for student in students:
            isLiveChiba = False

            #　千葉県在住か
            if "千葉県" in student.address:
                isLiveChiba = True

            #　団員情報の整合性チェック
            if student.complementFaculty() in student.facultycomp:
                print("学部が生徒証情報と異なる団員がいます。訂正と確認をしてください")
                print(f"名前:{student.name}")
                print(f"学生証番号:{student.id}")
                print(f"記載された学部:{student.major}")
                print(f"予想した学部:{student.facultycomp}")
                decision = ""
                while decision == "I" or decision == "F" or decision == "S":
                    decision = input("学生証(I)か学部(F)のどちらを直しますか?"+
                    "直さない場合はSを入力してください。>>")
                
                if decision == "I":
                    student.id = input("正しい生徒証番号を入力してください>>")
                elif decision == "F":
                    print("正しい学部・学科をC/Fもしくはマニュアルで入力してください。")
                    decision = input("記載を尊重(C) 推測を採用(F) >>")
                    if decision == "F":
                        student.major = student.facultycomp
                        student.facultycomp = "変更済み"
                        student.SpilitFac()
                    elif decision != "C":
                        student.major = decision
                        student.SpilitFac()
                elif decision == "S":
                    while decision == "Y" or decision == "N":
                        decision = print("CSVファイルに書き込みますか? Y/N >>")
                    if decision == "N":
                        continue #for文カウントアップ

            # 学生情報をCSV形式で保存する
            row = []
            for key in header.keys():
                if type(getattr(student,key)) == str:
                    row.append(getattr(student,key))
                else:
                    row.append(str(getattr(student,key)))
            # CSVファイルに書き込む
            f.write(','.join(map(str, row)) + '\n')