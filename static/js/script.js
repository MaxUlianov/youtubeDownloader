
function loading(){
    document.getElementById("loading").style.display = "block";
    document.getElementById("dl-options").style.display = "none";
}

function afterLoading(){
    document.getElementById("loading").style.display = "block";
    document.getElementById("dl").style.display = "none";
    document.getElementById("redirect-back").style.display = "block";
}
