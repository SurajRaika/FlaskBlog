console.log("ramram");

var mess=document.getElementById("notification")
if (mess) {
    setTimeout(function() {
        mess.classList.add("hide")
    }, 10000); // <-- time in milliseconds
    
}