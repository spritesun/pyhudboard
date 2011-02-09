var buildName = document.title.replace("[Hudson]", "").trim();
var host = "dashboard02.win.int:5000";
var action = document.getElementById("hudson_claim").getAttribute("action");
var constructClaimUrl = function() {
    var person = "none";
    try {
        person = document.getElementById("hudson_claim").getAttribute("person");
    }
    catch(e) {
    }
    if(person === "none" || !person) {
        person = prompt("Claiming '" + buildName + "'. Please enter your name");
    }
    return "http://" + host + "/claim?build=" + buildName + "&person=" + person;
};

var url = '';
if(action === "claim") {
    url = constructClaimUrl();
}
else if(action === "clear") {
    url = "http://" + host + "/clear?build=" + buildName;
}

var xhr = new XMLHttpRequest();
var handleChange = function(e) {
    // do nothing!
};

xhr.open("GET", url);
xhr.onreadystatechange = handleChange;
xhr.send();
