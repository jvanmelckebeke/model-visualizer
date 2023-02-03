import os

from keras.models import load_model
from wand.image import Image as WImage
from wand.color import Color
from visualizer.backend.diagram import Diagram
from visualizer.backend.document import Document
from visualizer.diagram.diagram_graph import DiagramGraph
from visualizer.util.config import StyleConfig, Config
from visualizer.util.tools import run_command

from texoutparse import LatexLogParser


def create_pdf(document: Document):
    if not os.path.exists('out'):
        os.makedirs('out')
    with open('generated_graph.tex', 'w') as f:
        f.write(document.generate_code())
    try:
        run_command(
            'pdflatex -file-line-error -interaction=nonstopmode -synctex=1 -output-format=pdf -output-directory=out '
            'generated_graph.tex > out/log.log')
        print("generated pdf file")
    except Exception as e:
        print(e)
        print("Error while generating pdf file")
    parser = LatexLogParser()
    with open('out/log.log') as f:
        parser.process(f)
    print(parser)


def visualize(model, resolution=200, canvas_width=None, canvas_height=None):
    input_layer = model.get_layer(name=model.inputs[0].name)
    output_layer = model.get_layer(index=-1)

    if canvas_width is None:
        canvas_width = Config.load_float('canvas', 'width')
    if canvas_height is None:
        canvas_height = Config.load_float('canvas', 'height')

    diagram_graph = DiagramGraph(input_layer, output_layer, canvas_width=canvas_width, canvas_height=canvas_height)
    document = Document()
    diagram = Diagram()

    document.add_styles(StyleConfig.load_styles())

    for node in diagram_graph.create_nodes():
        diagram.add_node(node)

    diagram.add_edges(diagram_graph.create_edges())

    document.add_element(diagram)

    create_pdf(document)

    img = WImage(filename='out/generated_graph.pdf', resolution=resolution)
    img.background_color = Color('white')
    img.alpha_channel = 'remove'
    return img


if __name__ == '__main__':
    _model = load_model('model.h5')
    visualize(_model)
