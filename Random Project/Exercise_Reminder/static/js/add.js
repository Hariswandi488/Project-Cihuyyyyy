const addform = document.getElementById("addform")
const addsubmit = document.getElementById("addsubmit")

addform.addEventListener("submit",
function () {
    addsubmit.innerText = "Loading...";
    addsubmit.disabled = true;
});