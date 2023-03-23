import inspect
import ast
import networkx as nx
import matplotlib.pyplot as plt
import sys


def task1(n):
    """
    :param n:
    :return: list first n Fibonachi's numbers
    """
    if n == 1:
        return [1]
    elif n == 2:
        return [1, 1]
    else:
        a, b = 1, 1
        fibonachi_numbers = [a, b]
        for _ in range(n - 2):
            a, b = b, a + b
            fibonachi_numbers.append(b)
        return fibonachi_numbers


def task2_3(filename):
    ast_object = ast.parse(inspect.getsource(task1))
    G = nx.DiGraph()
    node_colors = []
    labels = dict()

    def build_ast(node, parent=None):
        node_name = str(id(node))
        if isinstance(node, ast.Load) or isinstance(node, ast.Store) or isinstance(node, ast.Eq):
            return

        if isinstance(node, ast.Constant):
            labels[node_name] = node.value
            node_colors.append('gray')
        elif isinstance(node, ast.Module):
            labels[node_name] = "Module: \n" + node.__str__()
            node_colors.append('orange')
        elif isinstance(node, ast.Name):
            labels[node_name] = "Name: \n" + node.id
            node_colors.append('pink')
        elif isinstance(node, ast.Call):
            labels[node_name] = "Func: \n" + type(node.func).__name__
            node_colors.append('lightsalmon')
        elif isinstance(node, ast.FunctionDef):
            labels[node_name] = "Func: \n" + node.name
            node_colors.append('lightgreen')
        elif isinstance(node, ast.Return):
            labels[node_name] = "return"
            node_colors.append('red')
        elif isinstance(node, ast.BinOp):
            labels[node_name] = "BinOp: \n" + type(node.op).__name__
            node_colors.append('green')
        else:
            node_colors.append('lightblue')
            labels[node_name] = type(node).__name__
        G.add_node(node_name)
        if parent is not None:
            G.add_edge(parent, node_name)
        for child in ast.iter_child_nodes(node):
            build_ast(child, node_name)

    build_ast(ast_object)
    for k in labels.keys():
        labels[k] = str(labels[k])[:15]

    # Compute node positions using pydot layout
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')

    # Adjust node positions to prevent overlap
    def adjust_positions(pos, maxiter=1000, tol=1e-5):
        for i in range(maxiter):
            total = 0
            for node1 in pos:
                for node2 in pos:
                    if node1 != node2:
                        x1, y1 = pos[node1]
                        x2, y2 = pos[node2]
                        dx, dy = x2 - x1, y2 - y1
                        dist = (dx ** 2 + dy ** 2) ** 0.5
                        if dist > 0 and dist < tol:
                            total += 1
                            pos[node1] = x1 + dx * (tol - dist) / dist, y1 + dy * (tol - dist) / dist
            if total == 0:
                break

    adjust_positions(pos)

    # Plot the entire tree
    fig, ax = plt.subplots(figsize=(16, 8))
    nx.draw_networkx_nodes(G, pos, node_size=500, node_shape='s', node_color=node_colors, ax=ax)
    nx.draw_networkx_edges(G, pos, arrows=True, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=5, labels=labels, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'label'), ax=ax)

    ax.axis('off')
    plt.savefig(filename)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "task1":
            n = int(sys.argv[2])
            print(task1(n))
        else:
            filename = sys.argv[2]
            task2_3(filename)
    else:
        print("arguments not found, nothing to do")