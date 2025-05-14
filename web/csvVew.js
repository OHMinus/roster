let filenum = 0;
function LoadSavedData(){
    var datas = [];
    key = "Header"
    let head = JSON.parse(localStorage.getItem(key));
    datas.push(head)
    for (let index = 0; index < localStorage.length; index++) {
        key = localStorage.key(index);
        console.info(key)
        if(key == "Header"){
            continue;
        }else{
            let data = JSON.parse(localStorage.getItem(key));
            datas.push(data)
        }
    }

    console.info(datas)

    ShowData(JSON.stringify(datas));
}

function ShowData(json){
    localStorage.clear()
    document.getElementById("top").style="display: none";
    document.getElementById("loader").style="display: grid";
    document.getElementById("main").style="display: none";
    WriteLine("Load Datas");
    filenum = 0;
    const table = document.getElementById('csvTable');
    //table.innerHTML = '';
    WriteLine("clame element");
    data = JSON.parse(json);
    WriteLine("Json data has been dumped");
    localStorage.setItem("Header", JSON.stringify(data[0]));
    WriteLine("Header has been loaded");
    var uuid = null;
    const selector = document.getElementById("student-selector")
    let element = document.createElement("a");
    console.log(data)
    for (let i = 1; i < data.length; i++) {
        try {
            console.log(data[i]["submitted"])
            uuid = `${crypto.randomUUID()}-${i}`
            WriteLine(`${i}/${data.length} id:${uuid}`);
            localStorage.setItem(uuid, JSON.stringify(data[i]));
            element = document.createElement("a");
            WriteLine(`create elem`);
            element.innerText = data[i]["submitted"]["name"];
            WriteLine(`set innerText`);
            element.id = uuid;
            WriteLine(`set id`);
            element.addEventListener("click",LoadData,false);
            WriteLine(`addEventListener`);
            element.classList.add("btn");
            if(data[i]["warning"] == true){
                WriteError(`There is an error in ${data[i]["submitted"]["name"]}'s data.`);
                element.classList.add("error");
            }
            selector.appendChild(element);
        } catch (error) {
            console.log(error);
            WriteError(JSON.stringify(error));
        }
    }
    document.getElementById("loader").style="display: none";
    document.getElementById("main").style="display: grid";
}


function ClearData(){
    localStorage.clear();
    Location.reload();
}

function LoadData(event){
    id = event.target.id;
    LoadDataByID(id);
}

function SharrowEquals(a,b){
    for (const key in a) {
        if (Object.hasOwn(a, key) && Object.hasOwn(b, key)) {
            if(b[key] !== a[key]){
                return false;
            }            
        }else{
            return false;
        }
    }
    return true;
}

function tableGenerator(table,data){
    table.innerHTML = "";
    header = JSON.parse(localStorage.getItem("Header"))
    for (const key in data) {
        if (Object.hasOwn(data, key)) {
            if(key == "facultycomp" || key == "major" || key == "file_path"){
                //変更されても意味のないものや変更されると困るものはスキップ
                continue;
            }
            var tr = document.createElement("tr");
            var td = document.createElement("td");
            if (Object.hasOwn(header, key)) {
                td.innerText = header[key];
            }else{
                td.innerText = key;
            }
            tr.appendChild(td);
            td = document.createElement("td");
            td.innerText = data[key];
            td.setAttribute("data-key",key);
            tr.appendChild(td);
            table.appendChild(tr);
        }
    }
    return table;
}

async function LoadDataByID(id){
    sessionStorage.setItem("Current", id);
    const content = JSON.parse(localStorage.getItem(id));
    let table = document.getElementById("SubmittedContent");
    tableGenerator(table,content["submitted"]);
    table = document.getElementById("SuggestedContent");
    data = content["suggested"];
    if(SharrowEquals(content["submitted"],data)){
        var tr = document.createElement("tr");
        var td = document.createElement("td");
        td.innerText = "変更の必要がありません。";
        tr.appendChild(td);
        table.appendChild(tr);
    }else{
        tableGenerator(table,data);
    }
    document.getElementById("pdf-viewer").src = await eel.Getpdf(content["submitted"]["file_path"])();
}

function Reject(){
    id = sessionStorage.getItem("Current");
    target = document.getElementById(id);
    target.classList.remove("error");
    target.classList.add("audited");
}

function Accsept(){
    id = sessionStorage.getItem("Current");
    structure = JSON.parse(localStorage.getItem(id));
    structure["submitted"] = structure["suggested"]
    target = document.getElementById(id);
    target.classList.add("error");
    localStorage.setItem(id,JSON.stringify(structure))
    LoadDataByID(id);
}

function EnableModify(){
    let table = document.getElementById("SubmittedContent");
    tds = table.getElementsByTagName("td");
    for (td of tds){
        td.contentEditable = true;
        td.addEventListener("input",ModifyData);
    }
}

function ModifyData(event){
    id = sessionStorage.getItem("Current");
    structure = JSON.parse(localStorage.getItem(id));
    key = event.target.getAttribute("data-key")
    if(Object.hasOwn(structure["submitted"],key)){
        structure["submitted"][key] = event.target.innerText;
        localStorage.setItem(id,JSON.stringify(structure));
        console.info(`Modified data @ ${id} to`)
        console.info(structure)
    }else{
        WriteError(`Cannot found "${key}" in object (id: ${id})`);
    }    
}

function WriteLine(msg) {
    let today = new Date();
    var element = document.getElementById("popUp");
    element.getElementsByTagName("p")[0].innerText  = msg;
    element.style = "display:block";
    console.log(msg);
    element = document.createElement('p');
    element.innerText = `${today.getHours()}:${today.getMinutes()}:${today.getSeconds()}>${msg}`;
    document.getElementById("loading-message").appendChild(element)
    setTimeout(() => {Remove("popUp")},5000);
}

function WriteError(msg) {
    let today = new Date();
    var element = document.getElementById("popUp-error");
    element.getElementsByTagName("p")[0].innerText = msg;
    element.style = "display:block";
    console.error(msg);
    element = document.createElement('p');
    element.classList.add("error")
    element.innerText = `${today.getHours()}:${today.getMinutes()}:${today.getSeconds()}>${msg}`;
    document.getElementById("loading-message").appendChild(element)
    setTimeout(() => {Remove("popUp-error")},5000);
}

function Remove(id){
    var element = document.getElementById(id);
    element.style = "display:none";
}

function SaveUTF() {
    console.log("Save!")
    const contenttask = eel.SaveDir('UTF-8',GetDatas())();
}

function SaveSHIFT() {
    console.log("Save!")
    const contenttask = eel.SaveDir('shift_jis',GetDatas())();
}

function GetDatas(){
    var datas = [];
    key = ""
    for (let index = 0; index < localStorage.length; index++) {
        key = localStorage.key(index);
        if(key == "Header"){
            continue;
        }else{
            let data = JSON.parse(localStorage.getItem(key));
            if(Object.hasOwn(data,"submitted")){        
                console.info(`${key} ${datas.push(data["submitted"])}`)
            }
        }
    }
    return datas;
}

eel.expose(ShowData);
eel.expose(WriteLine);  
eel.expose(WriteError);