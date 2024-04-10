const canvas = document.createElement('canvas')
const ctx = canvas.getContext('2d')

body.append(canvas)

const width = canvas.width = window.innerWidth
const height = canvas.height = window.innerHeight

const circles = []

canvas.onclick = handleFirstClick

function clear() {
    ctx.clearRect(0, 0, width, height)
}

function drawLine(x1, y1, x2, y2, color, lineWidth) {
    ctx.beginPath()
    ctx.moveTo(x1, y1)
    ctx.lineTo(x2, y2)
    ctx.strokeStyle = color
    ctx.lineWidth = lineWidth
    ctx.stroke()
    ctx.closePath()
}

function drawCircle(x, y, r, fillCircle, color, lineWidth, lineColor) {
    ctx.beginPath()

    ctx.fillStyle = color
    ctx.strokeStyle = lineColor || color
    ctx.lineWidth = lineWidth

    ctx.arc(x, y, r, 0, Math.PI * 2, false)

    if (fillCircle) ctx.fill()

    ctx.stroke()

    ctx.closePath()
}

function addCircle(x, y, r, fill = false) {
    const circle = { x, y, r, fill, color: `hsl(${Math.random() * 360}, 75%, 60%)` }

    circles.push(circle)
    clear()
    renderAllCircles()
}

function startDrawingCircle(x0, y0) {
    drawCircle(x0, y0, 5, true, 'white', 2, 'green')

    canvas.onmousemove = handleMouseMove(x0, y0)
}

function handleFirstClick(e) {
    const { x, y } = e

    startDrawingCircle(x, y)
}

function handleMouseMove(x0, y0) {
    return e => {
        const { x: x1, y: y1 } = e
        const dx = x0 - x1
        const dy = y0 - y1
        const r = Math.hypot(dx, dy)

        clear()
        renderAllCircles()
        drawLine(x0, y0, x1, y1, 'green', 1)
        drawCircle(x0, y0, 5, true, 'white', 2, 'green')
        drawCircle(x0, y0, r, false, 'limegreen', 1)
        drawCircle(x1, y1, 5, true, 'white', 2, 'green')

        canvas.onclick = handleFinalClick(x0, y0)
    }
}

function handleFinalClick(x0, y0) {
    return e => {
        const { x: x1, y: y1, shiftKey } = e
        const dx = x0 - x1
        const dy = y0 - y1
        const r = Math.hypot(dx, dy)

        if (r > 3) addCircle(x0, y0, r, shiftKey)

        canvas.onmousemove = null
        canvas.onclick = handleFirstClick
    }
}

function renderAllCircles() {
    circles.forEach(({ x, y, r, color, fill }) => {
        drawCircle(x, y, r, fill, color, 2)
    })
}