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
    dic : dict = json.load(StudentJson)
    ref = core.Student.GetHeader().keys()
    stu = core.Student()
    for key in dic.keys():
        if key in ref:
            setattr(stu,key,dic[key])
    return stu

@eel.expose
def CheckErrorJson(StudentJson : str):
    return CheckError(Json2Student(StudentJson))

@eel.expose
def UpdateStudent(index : int, StudentJson : str):
    students[index] = Json2Student(StudentJson)
    return json.dump(students[index])

@eel.expose
def Ignition():
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
    print("clear")
    students.clear()

@eel.expose
def SaveDir(encoding,datas):
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

        