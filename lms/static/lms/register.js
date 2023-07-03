const emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

function emailValidation(email) {
    if (emailRegex.test(email)) {
        return true;
    }
    else {
        return false;
    }
}


document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('label[for="newGroup"]').style.display = "none";
    document.querySelector("#newGroup").style.display = "none";
    document.querySelector("#emailFormat").style.display = "none";
    document.querySelector("#existingGroups").style.display = "none"

    var emailElement = document.querySelector('#email');
    var newGroupButton = document.querySelector('#addNewGroup');
    var existingGroupsButton = document.querySelector("#existingGroups");
    newGroupButton.onclick = function() {
        document.querySelector("#groups").value = '';
        newGroupButton.style.display = "none";
        document.querySelector("#groups").disabled = true;
        document.querySelector("#groups").style.display = "none";
        existingGroupsButton.style.display = "block";
        document.querySelector('label[for="newGroup"]').style.display = "block";
        document.querySelector("#newGroup").style.display = "block";
    }
    existingGroupsButton.onclick = function() {
        existingGroupsButton.style.display = "none";
        newGroupButton.style.display = "block";
        document.querySelector("#groups").style.display = "block";
        document.querySelector("#groups").disabled = false;
        document.querySelector("#newGroup").value = '';
        document.querySelector('label[for="newGroup"]').style.display = "none";
        document.querySelector("#newGroup").style.display = "none";
    }
    emailElement.onkeyup = function() {
        if (emailValidation(this.value) == true) {
            document.querySelector("#emailFormat").style.display = "none";
            document.querySelector("#submitReg").disabled = false;
        }
        else {
            document.querySelector("#emailFormat").style.display = "block";
            document.querySelector("#submitReg").disabled = true;
        } 
    };
});