console.log("code.js");

var mess=document.getElementById("notification")
if (mess) {
    setTimeout(function() {
        mess.classList.add("hide")
    }, 30000); // <-- time in milliseconds
    
}