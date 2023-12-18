class GraphScreen:
    def __init__(self, width, height, initial_graph_size=30):
        self.width = width
        self.height = height
        self.graph_size = initial_graph_size

    def convertVectorToScreen(self, vector):
        return [vector[0] * self.graph_size, self.height - vector[1] * self.graph_size]
