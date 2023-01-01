from layers.layer import Layer
from tikz.edges.edge import Edge
import keras.layers


class UtilityLayer(Layer):
    sort_order = 9998

    def __init__(self, layer: keras.layers.Layer):
        super().__init__(layer)

    @property
    def layer_description(self) -> tuple:
        return self.type,

    def create_edges(self):
        edges = []

        for inbound_layer in self.inbound_layers:
            edges.append(Edge(inbound_layer.name, self.name))
        return edges
