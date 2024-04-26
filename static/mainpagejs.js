var draggableElements = document.getElementsByClassName('draggable');
let initialX, initialY, currentElement;
var condition = 1;
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

function create_note() {
    let NoteElemnet = document.createElement('div');
    NoteElemnet.classList.add('draggable');
    NoteElemnet.classList.add('bg-blue-500');
    NoteElemnet.classList.add('absolute');
    NoteElemnet.classList.add('cursor-move');
    NoteElemnet.classList.add('zind');


    NoteElemnet.textContent = "2task";
    document.body.append(NoteElemnet);
    var draggableElements = document.getElementsByClassName('draggable');
    let initialX, initialY, currentElement;
    Array.from(draggableElements).forEach(element => {
        element.addEventListener('mousedown', startDragging);
        element.addEventListener('mouseup', stopDragging);
    });
    postCards()
}

function startDragging(event) {
    currentElement = this;

    initialX = event.clientX - currentElement.offsetLeft;
    initialY = event.clientY - currentElement.offsetTop;
    document.addEventListener('mousemove', dragging);
}

function stopDragging() {
    document.removeEventListener('mousemove', dragging);
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
    $.ajax({
        url: 'http://127.0.0.1:8080/api/cards/' + id_user,
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            alert(data[0].Card.name)
        }
    })
}

function postCards() {
    let name = "test 2";
    let top_px = 100;
    let left_px = 100;
    let color = "red";
    let user_id = 2;
    var data = {
        name: 'javascript TEST',
        top_px: 500,
        left_px: 600,
        color: 'blue',
        user_id: 2
    }


    $.ajax({
        url: 'http://127.0.0.1:8080/api/cards',
        method: 'POST',
        data: JSON.stringify(data),
        contentType: "application/json",
    }).done(
        alert('Card added')
    )
}