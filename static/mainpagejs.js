var draggableElements = document.getElementsByClassName('draggable');
let initialX, initialY, currentElement;
var condition = 1;
var cardsloaded = false;
const createBtn = document.getElementById("create_btn");
const menuBtn = document.getElementById("menuBtn");
const mncrbtn = document.getElementById("mncrbtn");
const menu = document.getElementById("menu");
menuBtn.onclick = function() {
    if (condition > 0) {
        menu.classList.toggle('show-menu');
    } else {
        menu.classList.toggle('menu');
    }
    condition *= -1;
};

createBtn.onclick = function() {
    create_note();
};
Array.from(draggableElements).forEach(element => {
    element.addEventListener('mousedown', startDragging);
    element.addEventListener('mouseup', stopDragging);
});

function delete_note(id) {
    $.ajax({
        url: "http://127.0.0.1:8080/api/cards/" + id,
        method: "DELETE",
        success: function(data) {
            const el = document.getElementById(id);
            el.remove();
            console.log(data);
        }
    })
}

function add_note(cid, left_px, top_px, nameS) {
    let NoteElemnet = document.createElement('div');
    NoteElemnet.classList.add('draggable');
    NoteElemnet.classList.add('bg-blue-500');
    NoteElemnet.classList.add('absolute');

    NoteElemnet.classList.add('cursor-move');
    NoteElemnet.classList.add('zind');
    console.log(nameS);
    NoteElemnet.textContent = nameS;
    NoteElemnet.id = cid;
    NoteElemnet.style.top = top_px + 'px';
    NoteElemnet.style.left = left_px + 'px';
    console.log(NoteElemnet.style.top, top_px + 'px');
    NoteElemnet.innerHTML = '<button class="delbtns" onclick="delete_note(' + cid + ')">X</button> <p><b>' + nameS + '</b></p><input class="inp-field"></input>';
    document.body.append(NoteElemnet);
    var draggableElements = document.getElementsByClassName('draggable');
    let initialX, initialY, currentElement;
    Array.from(draggableElements).forEach(element => {
        element.addEventListener('mousedown', startDragging);
        element.addEventListener('mouseup', stopDragging);
    });
}

function create_note() {
    NTname = document.getElementById('inp-note').value;
    console.log(NTname)
    postCards(NTname);
}

function startDragging(event) {
    currentElement = this;

    initialX = event.clientX - currentElement.offsetLeft;
    initialY = event.clientY - currentElement.offsetTop;
    document.addEventListener('mousemove', dragging);
}

function stopDragging() {
    document.removeEventListener('mousemove', dragging);
    var url = 'http://127.0.0.1:8080/api/cards/' + currentElement.id + '/' + currentElement.style.left.replace('px', '') + '/' + currentElement.style.top.replace('px', '')
    console.log(currentElement.style.left)
    $.ajax({
        url: url,
        method: 'PUT',
        success: function(data) {
            console.log(data)
        }
    })
    currentElement = null;
}

function dragging(event) {
    if (currentElement) {
        const newX = event.clientX - initialX;
        const newY = event.clientY - initialY;
        currentElement.style.left = newX + 'px';
        currentElement.style.top = newY + 'px';
    }
}

function loadCards() {
    let id_user = document.getElementById("cur_id").textContent;
    console.log(id_user, cardsloaded)
    if (cardsloaded == false) {

        $.ajax({
            url: 'http://127.0.0.1:8080/api/cards/' + id_user,
            method: 'GET',
            dataType: 'json',
            success: function(data) {
                var l = 0;
                for (let i in data) {
                    add_note(data[l]["Card"]["id"], data[l]["Card"]["left_px"], data[l]["Card"]["top_px"], data[l]["Card"]["name"]);
                    console.log(data[l]["Card"]["id"]);
                    l += 1;
                }
                cardsloaded = true;
            }
        })
    }
}

function postCards(nameN) {
    let name = nameN;
    let top_px = 100;
    let left_px = 100;
    let color = "red";
    let user_id = document.getElementById("cur_id").textContent;
    var data = {
        name: name,
        top_px: 500,
        left_px: 600,
        color: 'blue',
        user_id: user_id
    }

    $.ajax({
        url: 'http://127.0.0.1:8080/api/cards',
        method: 'POST',
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function(dl) {
            add_note(dl, 100, 100, nameN);

        }
    })
}