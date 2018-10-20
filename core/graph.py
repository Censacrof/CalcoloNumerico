from matrix import Matrix

class Graph:
    _adj_mat = None
    _n_nodes = None

    def __init__(self, adj_mat):
        if isinstance(adj_mat, Matrix):
            self._adj_mat = adj_mat
        else:
            self._adj_mat = Matrix.from_2d_array(adj_mat)

        assert self._adj_mat._n_rows == self._adj_mat._n_cols, 'The adjacency matrix has to be a square matrix'
        self._n_nodes = self._adj_mat._n_rows

        pass
    

    def dijkstra(self, starting_node):
        distances = []
        prev = []
        unvisited_nodes = []

        for i in range(self._n_nodes):
            distances.append(0 if i == starting_node else None)
            prev.append(None)
            unvisited_nodes.append(i)        

        adj_mat = self._adj_mat._mat

        while len(unvisited_nodes) > 0:
            #find the closest node to the current
            min_dist = None
            min_dist_node = None
            for node in unvisited_nodes:
                if distances[node] is None:
                    continue
                
                if min_dist is None:
                    min_dist = distances[node]
                    min_dist_node = node
                    continue
                
                if  min_dist > distances[node]:
                    min_dist = distances[node]
                    min_dist_node = node
                    continue
            
            #if the min_dist_node is None exit
            if min_dist_node is None:
                break

            #remove min_dist_node from unvisited_nodes
            unvisited_nodes.remove(min_dist_node)

            for neighbor in unvisited_nodes:
                if adj_mat[min_dist_node][neighbor] is None:
                    continue
                
                dist = distances[min_dist_node] + adj_mat[min_dist_node][neighbor]

                if distances[neighbor] is None:
                    distances[neighbor] = dist
                    prev[neighbor] = min_dist_node
                    

                elif distances[neighbor] > dist:
                    distances[neighbor] = dist
                    prev[neighbor] = min_dist_node

        return distances, prev
    

    def __str__(self):
        
        res = ''
        for from_node in range(len(self._adj_mat._mat)):
            res += 'node %d goes to:\n' % from_node
            at_least_one = False

            for to_node in range(len(self._adj_mat._mat[from_node])):
                if self._adj_mat._mat[from_node][to_node] is not None:
                    res += '\tnode %d, weight %d\n' % (to_node, self._adj_mat._mat[from_node][to_node])
                    at_least_one = True
                    
            if not at_least_one:
                res += '\tnobody\n'
            
            res += '\n'
        
        res += '\n'
        return res

    pass



# g = Graph([
#     [None, 99, 50, None, None],
#     [None, None, 50, 50, 50],
#     [None, None, None, 99, None],
#     [None, None, None, None, 75],
#     [None, None, None, None, None]
# ])

# print(g.dijkstra(0))
