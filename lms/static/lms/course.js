function EnrollUser(user, course) {
    let csrftoken = getCookie('csrftoken');
    fetch(`/enroll/${user}/${course}`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({message: "enroll"})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });
}

function UnenrollUser(user, course) {
    let csrftoken = getCookie('csrftoken');
    fetch(`/enroll/${user}/${course}`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({message: "unenroll"})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function EnrollButton(dataUser, dataCourse, htmlVar) {
    console.log("enroll pressed");
    EnrollUser(dataUser, dataCourse);
    const newUnenrollButton = document.createElement("button"); 
    newUnenrollButton.setAttribute("class", "unenroll-button");
    newUnenrollButton.setAttribute("id", `unenroll${dataUser}`);
    newUnenrollButton.setAttribute("data-user", dataUser);
    newUnenrollButton.setAttribute("data-course", dataCourse);
    newUnenrollButton.innerHTML = htmlVar;
    newUnenrollButton.onclick = function() {
        UnenrollButton(dataUser, dataCourse, htmlVar);
    }
    const notEnrolledDiv = document.getElementById("enrolled");
    notEnrolledDiv.appendChild(newUnenrollButton);
    const oldEnrollButton = document.getElementById(`enroll${dataUser}`);
    oldEnrollButton.remove();
}


function UnenrollButton(dataUser, dataCourse, htmlVar) {
    console.log("unenroll pressed");
    UnenrollUser(dataUser, dataCourse);
    const newEnrollButton = document.createElement("button"); 
    newEnrollButton.setAttribute("class", "enroll-button");
    newEnrollButton.setAttribute("id", `enroll${dataUser}`);
    newEnrollButton.setAttribute("data-user", dataUser);
    newEnrollButton.setAttribute("data-course", dataCourse);
    newEnrollButton.innerHTML = htmlVar;
    newEnrollButton.onclick = function() {
        EnrollButton(dataUser, dataCourse, htmlVar);
    }
    const enrolledDiv = document.getElementById("notEnrolled");
    enrolledDiv.appendChild(newEnrollButton);
    const oldUnenrollButton = document.getElementById(`unenroll${dataUser}`);
    oldUnenrollButton.remove();
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.enroll-button').forEach(button => {
        button.onclick = function() {
            EnrollButton(this.dataset.user, this.dataset.course, this.innerHTML);
        }
    })
    document.querySelectorAll('.unenroll-button').forEach(button => {
        button.onclick = function() {
            UnenrollButton(this.dataset.user, this.dataset.course, this.innerHTML);
        }
    })
});