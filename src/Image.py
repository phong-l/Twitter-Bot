from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


def svgtopng(pic):
    drawing = svg2rlg(pic)
    renderPM.drawToFile(drawing, 'temp.png', fmt='png')
