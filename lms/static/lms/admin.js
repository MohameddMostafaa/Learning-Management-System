function AcceptUser(user) {
    let csrftoken = getCookie('csrftoken');
    fetch(`/pending/${user}`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({message: "accept"})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });
}

function RejectUser(user) {
    let csrftoken = getCookie('csrftoken');
    fetch(`/pending/${user}`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({message: "reject"})
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



document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.accept_button').forEach(button => {
        button.onclick = function() {
            console.log("accept pressed")
            document.querySelector('#div' + this.dataset.user).style.display = 'none';
            AcceptUser(this.dataset.user);
        }
    })
    document.querySelectorAll('.reject_button').forEach(button => {
        button.onclick = function() {
            console.log("reject pressed")
            document.querySelector('#div' + this.dataset.user).style.display = 'none';
            RejectUser(this.dataset.user);
        }
    })
});