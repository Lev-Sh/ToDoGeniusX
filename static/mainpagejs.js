var draggable = document.getElementById('draggable');
print("HELLO")
draggable.onmousedown = function(event) {
    draggable.style.position = 'absolute';
    draggable.style.zIndex = 1000;

    function moveAt(pageX, pageY) {
        draggable.style.left = pageX - draggable.offsetWidth / 2 + 'px';
        draggable.style.top = pageY - draggable.offsetHeight / 2 + 'px';
    }

    moveAt(event.pageX, event.pageY);

    function onMouseMove(event) {
        moveAt(event.pageX, event.pageY);
    }

    document.addEventListener('mousemove', onMouseMove);

    draggable.onmouseup = function() {
        document.removeEventListener('mousemove', onMouseMove);
        draggable.onmouseup = null;
    };
};

draggable.ondragstart = function() {
    return false;
};