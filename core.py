import os
import glob
import pdf
import main
import  datetime
from    datetime import datetime
import re
from io import StringIO
import String_helper
import csv
import encodingDitector

facultys = {}

def getFacPatterns(patternFile: str):
    if len(facultys) == 0:
        encoding = encodingDitector.encordingDItector(patternFile)
        with open ( patternFile , 'r' ,encoding=encoding) as f :
            csvContent = csv.reader(f)
            for row in csvContent:
                facultys[re.compile(row[0])] = row[1]

    return facultys

def loadDir(dirPath):
    files =[]
    print(f"searching @ {dirPath}")
    if os.path.isfile(dirPath):
        raise Exception("Invalid path")

    if not os.path.isabs(dirPath):
        dirPath = os.path.abspath(dirPath)
    
    if str(dirPath).endswith("/"):
        dirPath = dirPath +"*"
    else:
        dirPath = dirPath +"/*"
    
    files = glob.glob(dirPath+"")


    if len(files) == 0:
        raise Exception("No files in directory")

    students = []
    for file in files:
        if file.endswith(".pdf"):
            # PDFファイルを読み込む
            students.append(pdf.pdf_to_student(file))
    
    for student in students:
        student.EstimateFaculty("faculty_patterns.csv")

    return students

def date_to_str(date:str):
    #型式推論

    # 例: "平成30年4月1日" -> "2018-04-01"

    result : datetime.date = None

    # 元号一覧
    gengo = {
        "明治": 1868,
        "大正": 1912,
        "昭和": 1926,
        "平成": 1989,
        "令和": 2019
    }
    wareki : int = -1

    for g in gengo.keys():
        if g in date:
            wareki = gengo.index(g)
            break

    date = date.replace("元", "0").replace("年","/").replace(" ","").replace("月","/").replace("日","/").replace(".","/")
    judger = re.compile(r"\d{4}\/\d{1,2}\/\d{1,2}")
    if date[len(date)-1] == "/":
        date = date[0:len(date)-1]
    if judger.search(date) == None:
        result = datetime.strptime(date, "%y/%m/%d")
    else:
        result = datetime.strptime(date, "%Y/%m/%d")
    
    if wareki != -1:
        # 和暦から西暦に変換
        result = datetime.date(result.year + gengo.values()[wareki], result.month, result.day)

    return result

    
class Student:
    name: str
    nameKana: str
    id : str
    gread: int
    faculty : str
    facultycomp : str
    department : str
    course : str
    field :str
    major : str
    majorcomp : str
    birth : datetime
    zip_code : str
    address : str
    phone_number : str
    email : str
    file_path : str
    isLiveChiba : bool
    sex : str
    
    @staticmethod
    def GetHeader():
        return {
        "name":"名前", 
        "nameKana":"氏名ふりがな", 
        "id":"学籍番号", 
        "gread":"学年",
        "major":"学部・学科", 
        "sex":"性別",
        "faculty":"学部", 
        "department":"学科", 
        "course":"コース",
        "field":"専攻", 
        "facultycomp":"推測された学部等",
        "birth":"生年月日", 
        "phone_number":"携帯電話番号", 
        "email":"メールアドレス",
        "zip_code":"郵便番号",
        "address":"現住所",
        "isLiveChiba":"千葉に住民票があるか",
        "file_path" : "ファイルパス"
    }

    def __init__(self, name: str = "" , nameKana: str = "", id: str = "", gread: int = 0, faculty: str = "", department: str = "", major: str = "",field:str = "",
                    birth: datetime = None, zip_code: str = "", address: str = "", phone_number: str = "", email: str = ""):
        self.name = name
        self.nameKana = nameKana
        self.id = id
        self.gread = gread
        self.faculty = faculty
        self.department = department
        self.major = major
        self.birth = birth
        self.zip_code = zip_code
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.field = field
        self.course = ""
        self.facultycomp = ""
        self.file_path = ""
        if address == "":
            self.isLiveChiba = None
        elif "千葉県" in self.address:
            self.isLiveChiba = True
        else:
            self.isLiveChiba = False

    def __str__(self):
        return f"Name: {self.name}, ID: {self.id}, Gread: {self.gread}, Faculty: {self.faculty}, Department: {self.department}, Major: {self.major}, Birth: {self.birth}, Zip Code: {self.zip_code}, Address: {self.address}, Phone Number: {self.phone_number}, Email: {self.email}"
    
    def __eq__(self, other):
        if not isinstance(other, self):
            return False
        
        var_list = vars(self)
        for key, value in other.__dict__.items():
            if key not in var_list or var_list[key] != value:
                return False
        # すべての属性が一致する場合
        return True

    def EstimateFaculty(self , patternFile: str):
        self.facultys = getFacPatterns(patternFile)
        self.id.upper()
        for pattern, faculty in self.facultys.items():
            if pattern.match(self.id):
                self.facultycomp = faculty
                break
        else:
            self.facultycomp = "未解決"

    def getDict(self):
        keys = self.GetHeader()
        for key in keys:
            if isinstance(keys[key], datetime):
                keys[key] = keys[key].isoformat()
            else:
                keys[key] = str(getattr(self,key))

        return keys
            

    def SpilitFac(self):
        tmp = String_helper.Replace(self.major,"").split("学部")
        self.faculty = f"{tmp[0]}学部"
        if len(tmp) > 1:
            if len(tmp[1].split("学科")) > 1 or len(tmp[1].split("課程")) > 1:
                if len(tmp[1].split("学科")) > 1:
                    tmp = tmp[1].split("学科")
                    self.department = f"{tmp[0]}学科"
                else:
                    tmp = tmp[1].split("課程")
                    self.department = f"{tmp[0]}課程"
                tmp = tmp[1].split("コース")
                if(tmp[0] != ""):
                    self.course = f"{tmp[0]}コース"
                    if len(tmp) > 1:
                        self.field = tmp[1]
            else:
                self.department = f"{tmp[1]}学科"

    def SetAddress(self,rawaddress):
        zipCodeTmp = re.search(r"\d{3}[-]{0,1}\d{4}", rawaddress)
        if zipCodeTmp is not None:
            self.zip_code = zipCodeTmp[0]
            self.address = rawaddress.replace("〒", "").replace(self.zip_code, "").strip().replace("\n", "")

    def complementFaculty(self):
        # 学部名を取得するための正規表現
        faculty_patterns = {
            "国": "国際教養学部",
            "文": "文学部",
            "法": "法政経学部",
            "教": "教育学部",
            "理": "理学部",
            "工": "工学部",
            "情": "情報・データサイエンス学部",
            "園": "園芸学部",
            "医": "医学部",
            "薬": "薬学部",
            "看": "看護学部",
        }


        for pattern, faculty in faculty_patterns.items():
            if pattern in self.major:
                return faculty

        return ""