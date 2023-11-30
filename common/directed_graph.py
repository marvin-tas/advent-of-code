class Vertex:
    def __init__(self, vertex_id):
        self.vertex_id = vertex_id

    def __eq__(self, other):
        return self.vertex_id == other.vertex_id

    def __hash__(self):
        return hash(self.vertex_id)

    def __str__(self):
        return "[" + self.vertex_id + "]"
        
class DirectedEdge:
    def __init__(self, vertex_id_1, vertex_id_2):
        self.outgoing_vertex = vertex_id_1
        self.incoming_vertex = vertex_id_2

    def __eq__(self, other):
        return self.incoming_vertex == other.incoming_vertex and \
               self.outgoing_vertex == other.outgoing_vertex

    def __hash__(self):
        return 11 * hash(self.incoming_vertex) + 17 * hash(self.outgoing_vertex)

    def __str__(self):
        return str(self.outgoing_vertex) + "-->" + str(self.incoming_vertex)

class DirectedGraph:

    def __init__(self):
        self.vertices = set()
        self.edges = set()
        self.adjacent_vertex_map = {}
        self.adjacent_vertex_reverse_map = {}

    def add_vertex_by_id(self, vertex_id):
        vertex = Vertex(vertex_id)
        if vertex not in self.vertices:
            self.vertices.add(vertex)
            self.adjacent_vertex_map[vertex] = set()
            self.adjacent_vertex_reverse_map[vertex] = set()
        return vertex

    def add_directed_edge_and_required_vertices(self, vertex_id_1, vertex_id_2):
        vertex_1 = self.add_vertex_by_id(vertex_id_1)
        vertex_2 = self.add_vertex_by_id(vertex_id_2)
        edge = DirectedEdge(vertex_1, vertex_2)
        self.edges.add(edge)
        self.adjacent_vertex_map[vertex_1].add(vertex_2)
        self.adjacent_vertex_reverse_map[vertex_2].add(vertex_1)

    def __str__(self):
        return "G|V=" + str([str(vertex) for vertex in self.vertices]) + "|E=" + str([str(edge) for edge in self.edges])


class TopologicalSorter:

    def __init__(self):
        print("NO OP")

    def sort_dag(self, directed_graph):
        vertices_sorted = []
        vertices_processed = set()
        vertices_ready_for_processing = []
        # First find the vertices with no incoming edges
        for vertex in directed_graph.vertices:
            if len(directed_graph.adjacent_vertex_reverse_map[vertex]) == 0:
                vertices_ready_for_processing.append(vertex)
        while not len(vertices_ready_for_processing) == 0:
            current_vertex = vertices_ready_for_processing[0]
            vertices_ready_for_processing = vertices_ready_for_processing[1:]
            adjacent_vertices = directed_graph.adjacent_vertex_map[current_vertex]
            vertices_processed.add(current_vertex)
            for adjacent_vertex in adjacent_vertices:
                pre_requisite_vertices = directed_graph.adjacent_vertex_reverse_map[adjacent_vertex]
                if len(pre_requisite_vertices.difference(vertices_processed)) == 0:
                    vertices_ready_for_processing.append(adjacent_vertex)
            vertices_sorted.append(current_vertex)
        return vertices_sorted

