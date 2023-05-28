from flask import Flask, render_template, request
import networkx as nx
import matplotlib.pyplot as plt

app = Flask(__name__,template_folder="templates")

# Define the graph and H_table


mygraph = {
    "CMH Attock": [("Dr Saeed Hospital Attock", 820.24), ("Attock City Police Station", 1180)],
    "Civil Hospital Attock": [("Darul Islam Colony", 301.32)],
    "Alam Hospital Attock": [("NADRA office attock", 2030), ("Darul Islam Colony", 820.31), ("Wajahat Hospital Attock", 386.85), ("Peoples colony chowk", 139)],
    "Wajahat Hospital Attock": [("Darul Islam Colony", 426.58), ("Alam Hospital Attock", 386.85), ("Peoples colony chowk", 497)],
    "Dr Saeed Hospital Attock": [("Darul Islam Colony", 534.56), ("CMH Attock", 820.24)],
    "Peoples colony chowk": [("Wajahat Hospital Attock", 497), ("Alam Hospital Attock", 139)],
    "NADRA office attock": [("Alam Hospital Attock", 2030)],
    "Darul Islam Colony": [("Dr Saeed Hospital Attock", 534.56), ("Alam Hospital Attock", 820.31), ("Wajahat Hospital Attock", 426.58), ("Civil Hospital Attock", 301.32)],
    "Attock City Police Station": [("CMH Attock", 1180)]
}

H_table = {
    "CMH Attock": 50,
    "Civil Hospital Attock": 55,
    "Alam Hospital Attock": 60,
    "Wajahat Hospital Attock": 65,
    "Dr Saeed Hospital Attock": 70,
    "Peoples colony chowk": 75,
    "NADRA office attock": 80,
    "Darul Islam Colony": 85,
    "Attock City Police Station": 90
}


# Define the positions of nodes
pos = {
    "CMH Attock": (0, 2),
    "Civil Hospital Attock": (7, -2),
    "Alam Hospital Attock": (3, 2),
    "Wajahat Hospital Attock": (3, 5),
    "Dr Saeed Hospital Attock": (4, -1),
    "Peoples colony chowk": (1, 4),
    "NADRA office attock": (5, 5),
    "Darul Islam Colony": (6, 1),
    "Attock City Police Station": (1, -2),
}

graph = nx.Graph()

# Add nodes to the graph
graph.add_nodes_from(mygraph.keys())


# Add edges with weights to the graph
for node, neighbors in mygraph.items():
    for neighbor, distance in neighbors:
        graph.add_edge(node, neighbor, weight=distance)

# Define the graph visualization function
def visualize_graph(answer_path):
    plt.figure(figsize=(10, 8))

    # Draw nodes
    node_colors = ['lightgreen' if node in [n for n, _ in answer_path] else 'lightblue' for node in graph.nodes()]
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=5000)

    # Draw edges
    path_edges = [(answer_path[i][0], answer_path[i + 1][0]) for i in range(len(answer_path) - 1)]
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=5.0)

    # Draw all other edges
    all_edges = list(graph.edges())
    other_edges = list(set(all_edges) - set(path_edges))
    nx.draw_networkx_edges(graph, pos, edgelist=other_edges, edge_color='lightblue', width=1.0)

    # Draw labels
    nx.draw_networkx_labels(graph, pos, font_size=10)

    # Draw edge labels
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')


    # Show the graph
    plt.axis('off')
    plt.savefig('static/graph.png') 

# Define the path cost calculation function
def my_path_cost_a_star(path):
    total_cost = 0
    for i in range(len(path) - 1):
        node1 = path[i][0]
        node2 = path[i + 1][0]
        edge_data = graph.get_edge_data(node1, node2)
        edge_weight = edge_data['weight']
        total_cost += edge_weight
    return total_cost


# Define the A* algorithm function
def my_a_star(mygraph, start):
    visited = []
    queue = [[(start, 0)]]
    while queue:
        queue.sort(key=my_path_cost_a_star)
        path = queue.pop(0)
        node = path[-1][0]
        if node not in visited:
            visited.append(node)
            if node in ["CMH Attock", "Civil Hospital Attock", "Alam Hospital Attock", "Wajahat Hospital Attock", "Dr Saeed Hospital Attock"]:
                return path
            else:
                neighbour_nodes = mygraph.get(node, [])
                for node2, cost in neighbour_nodes:
                    new_path = path.copy()
                    new_path.append((node2, cost))
                    queue.append(new_path)
        else:
            continue
    

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define the route for handling the form submission
@app.route('/find_path', methods=['POST'])
def find_path():
    emergency_location = request.form['emergency_location']
    answer_path = my_a_star(mygraph, emergency_location)
    nearest_hospital = answer_path[-1][0]
    path_cost = round(my_path_cost_a_star(answer_path), 2)  # Calculate the path cost

    visualize_graph(answer_path)  # Visualize the graph

    return render_template('result.html', nearest_hospital=nearest_hospital,path=answer_path, path_cost=path_cost)

if __name__ == '__main__':
    app.run(debug=True)  

