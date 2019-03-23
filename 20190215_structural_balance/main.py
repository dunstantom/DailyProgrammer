import argparse
from Queue import Queue

def main():
    parser = argparse.ArgumentParser(description="Determine if graph is balanced")
    parser.add_argument("-i", dest="filename", required=True, help="Input file specifying graph")
    args = parser.parse_args()

    graph = read_graph(args.filename)
    verify_graph(graph)


def read_graph(filename):
    print "Loading graph from " + filename
    edges = {}
    with open(filename) as f:
        num_nodes, num_edges = f.readline().split()
        for line in f:
            if "--" not in line:
                continue
            node_a, node_b = [x.strip() for x in line.split("--")]
            if node_a in edges:
                edges[node_a].append(node_b)
            else:
                edges[node_a] = [node_b]
            if node_b in edges:
                edges[node_b].append(node_a)
            else:
                edges[node_b] = [node_a]
    return edges


def verify_graph(graph):
    print "Verifying graph"
    red = []
    blue = []
    unvisited_nodes = Queue()

    print "Adding " + graph.keys()[0]
    red.append(graph.keys()[0])
    unvisited_nodes.put(graph.keys()[0])

    while not unvisited_nodes.empty():
        node = unvisited_nodes.get()
        color_red = node in blue
        for neighbor in graph[node]:
            # check for conflict
            if (neighbor in blue and color_red) or (neighbor in red and not color_red):
                print "red: " + ', '.join(red)
                print "blue: " + ', '.join(blue)
                print "unbalanced due to " + neighbor + ": " + ', '.join(graph[neighbor])
                return 0
            # check not colored already
            if neighbor not in red and neighbor not in blue:
                print "adding " + neighbor
                unvisited_nodes.put(neighbor)
                if color_red:
                    red.append(neighbor)
                else:
                    blue.append(neighbor)
    print "red: " + ', '.join(red)
    print "blue: " + ', '.join(blue)
    print "balanced"
    return 1


if __name__ == "__main__":
    main()
