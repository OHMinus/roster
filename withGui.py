"""
@file withGui.py
@brief GUI (Graphical User Interface) を提供します。
@details tkinter と eel を使用して GUI を構築し、学生データの処理を行います。
"""
import tkinter.filedialog
import eel
import core
import json
import tkinter
import os
import sys
import io
from base64 import urlsafe_b64encode 
import atexit
import asyncio
import copy
import base64


students = []
stream :io.StringIO = None

def CheckError(stu):
    """
    @brief 学生データのエラーチェックを行います。
    @param stu (core.Student): チェックする Student オブジェクト。
    @return (bool): エラーがある場合は True、ない場合は False。
    @details 学生の住所と学部情報の整合性をチェックします。
    """
    result = False
    isLiveChiba = False

    #　千葉県在住か
    if "千葉県" in stu.address:
        isLiveChiba = True
    
    if stu.isLiveChiba != isLiveChiba:
        result = True

    #　団員情報の整合性チェック
    if stu.complementFaculty() in stu.facultycomp:
        result = True
    
    return result

def Json2Student(StudentJson : str):
    """
    @brief JSON 文字列を Student オブジェクトに変換します。
    @param StudentJson (str): 学生情報の JSON 文字列。
    @return (core.Student): 変換された Student オブジェクト。
    @details JSON 文字列を解析し、Student オブジェクトの属性に値を設定します。
    """
    dic : dict = json.load(StudentJson)
    ref = core.Student.GetHeader().keys()
    stu = core.Student()
    for key in dic.keys():
        if key in ref:
            setattr(stu,key,dic[key])
    return stu

@eel.expose
def CheckErrorJson(StudentJson : str):
    """
    @brief JSON 形式の学生データのエラーチェックを行います (eel.expose)。
    @param StudentJson (str): 学生情報の JSON 文字列。
    @return (bool): エラーがある場合は True、ない場合は False。
    """
    return CheckError(Json2Student(StudentJson))

@eel.expose
def UpdateStudent(index : int, StudentJson : str):
    """
    @brief 学生データを更新します (eel.expose)。
    @param index (int): 更新する学生データのインデックス。
    @param StudentJson (str): 更新後の学生情報の JSON 文字列。
    @return (str): 更新された学生データの JSON 表現。
    """
    students[index] = Json2Student(StudentJson)
    return json.dump(students[index])

@eel.expose
def Ignition():
    """
    @brief 学生データの読み込みと GUI への表示を開始します (eel.expose)。
    @details ディレクトリ選択ダイアログを表示し、PDF ファイルから学生データを読み込んで GUI に表示します。
    """
    input_dir = tkinter.filedialog.askdirectory()
    eel.jump()
    students.extend(core.loadDir(input_dir))
    for student in students:
        isLiveChiba = False
        
        if student.isLiveChiba == None:
            #　千葉県在住か
            if "千葉県" in student.address:
                isLiveChiba = True

        student.isLiveChiba = isLiveChiba

        #　団員情報の整合性チェック
    
    #Htmlに書き出し
    jsonee = []
    jsonee.append(core.Student.GetHeader())
    for student in students:
        dic = {"submitted":None,"suggested":None,"warning":False}
        dic["submitted"] = student.getDict()
        tmp = copy.deepcopy(student)

        if tmp.facultycomp != "未解決":
            tmp.major = tmp.facultycomp
            tmp.SpilitFac()
        
        dic["suggested"] = tmp.getDict()
        dic["warning"] = CheckError(student)
        jsonee.append(dic)
        print(f"{student.name} {len(jsonee)} / {len(students)}")
        for j in jsonee:
            print(dic["suggested"]["name"])
    with io.StringIO() as s:
        json.dump(jsonee,s)
        eel.ShowData(s.getvalue())

@eel.expose
def Refresh():
    """
    @brief 学生データをクリアします (eel.expose)。
    @details 読み込まれている学生データのリストを空にします。
    """
    print("clear")
    students.clear()

@eel.expose
def SaveDir(encoding,datas):
    """
    @brief 学生データを CSV ファイルに保存します (eel.expose)。
    @param encoding (str): CSV ファイルのエンコーディング。
    @param datas (list): 保存する学生データのリスト。
    @details ファイル保存ダイアログを表示し、学生データを CSV ファイルに保存します。
    """
    filename = tkinter.filedialog.asksaveasfilename(
        title = "Save as...",
        filetypes = [("CSV", ".csv")], # ファイルフィルタ
        initialdir = "./", # 自分自身のディレクトリ
        defaultextension = "csv",
        initialfile = "output"
    )

    # 学生情報をCSV形式で保存する
    # CSVファイルのヘッダー
    header = core.Student.GetHeader()

    #要らない情報を削除
    header.pop("major")
    header.pop("facultycomp")
    header.pop("file_path")

    # CSVファイルにヘッダーを書き込む
    with open(str(filename), 'w', encoding=encoding,errors='ignore') as f:
        f.write(','.join(header.values()) + '\n')
        #生徒について取得
        for student in datas:
            print(student["name"])
            #参照したい項目を閲覧
            for key in header.keys():
                if key in student:
                    f.write(f"{student[key]},")
                else:
                    f.write(f"#N/A,")
            f.write("\n")
        
@eel.expose
def Getpdf(filepath):
    """
    @brief PDF ファイルの内容を base64 エンコードして返します (eel.expose)。
    @param filepath (str): PDF ファイルのパス。
    @return (str): base64 エンコードされた PDF データ URI。
    @details PDF ファイルを読み込み、base64 エンコードして Data URI 形式で返します。
    """
    gfg = ""
    with open(filepath,  "rb") as image_file:
        # bufに格納
        buf = image_file.read()
    
        # base64のdata取得
        data = base64.b64encode(buf)
        data_str = data.decode('utf-8')
        print(f"load pdf file {filepath} {len(buf)}")
        # Data URI
        gfg = "data:" + "application/pdf" + ";base64," + data_str

    return gfg

def cleanup():
    stream.close()

def StartGUI():
    print("initializing...")
    # フロントエンドのHTMLフォルダを指定
    eel.init('web')
    mode='chrome'
    if "win" in str(sys.platform):
        mode='edge'
    # アプリを起動 (トップページをindex.htmlに指定)
    eel.start('index.html', mode=mode, cmdline_args=['--start-fullscreen',"--allow-file-access-from-file"])
    atexit.register(cleanup)
    stream = io.StringIO()
    sys.stdout = stream
    nowait = StdOutDaemon()

async def StdOutDaemon():
    content = ""
    flag = True
    while True:
        await asyncio.sleep(1)
        while(flag):
            content = stream.readline()
            if content == "":
                flag = False
            else:
                eel.WriteLine(content)

        