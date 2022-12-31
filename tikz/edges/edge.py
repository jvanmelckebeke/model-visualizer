from tikz.base import TikzElement


class Edge(TikzElement):
    def __init__(self, from_node, to_node, label="", edge_style="default_edge", label_style="default_label"):
        self.from_node = from_node
        self.to_node = to_node
        self.label = label
        self.edge_style = edge_style
        self.label_style = label_style
        super().__init__(f"edge_{from_node}_{to_node}", depends_on=[from_node, to_node])

    def draw(self):
        return self.to_code()

    def to_code(self):
        out = f"% edge from {self.from_node} to {self.to_node}\n"
        out += rf"\draw[->, {self.edge_style}] ({self.from_node}) " \
               rf"to node [{self.label_style}] {{{self.label}}} ({self.to_node});"
        return out + "\n"

    def __str__(self):
        return f"edge from {self.from_node} to {self.to_node} with label {self.label}"
