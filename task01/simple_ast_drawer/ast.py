import ast
import networkx as nx
from pathlib import Path
from dataclasses import dataclass


@dataclass
class NodeInfo:
    label: str
    color: str


def _get_node_info(node: ast.AST) -> NodeInfo:
    if isinstance(node, ast.Attribute):
        return NodeInfo(f'.{node.attr}', '#c49b5c')
    if isinstance(node, ast.Constant):
        return NodeInfo(f'{node.value}', '#89abfa')
    if isinstance(node, ast.Name):
        return NodeInfo(f'{node.id}', '#ffedd1')
    if isinstance(node, ast.arg):
        return NodeInfo(f'{node.arg}', '#f2d596')
    if isinstance(node, (ast.Sub, ast.USub)):
        return NodeInfo(f'-', '#8fd1f7')
    if isinstance(node, ast.Add):
        return NodeInfo(f'+', '#8fd1f7')
    if isinstance(node, ast.Assign):
        return NodeInfo(f'=', '#8fd1f7')
    if isinstance(node, ast.Lt):
        return NodeInfo(f'<', '#8fd1f7')
    if isinstance(node, ast.FunctionDef):
        return NodeInfo(f'def {node.name}', '#e36456')
    if isinstance(node, ast.While):
        return NodeInfo(f'while', '#e36456')
    if isinstance(node, ast.Expr):
        return NodeInfo(f'do', '#e36456')
    if isinstance(node, ast.Return):
        return NodeInfo(f'return', '#e36456')
    if isinstance(node, ast.arguments):
        return NodeInfo(f'(args...)', '')
    if isinstance(node, ast.List):
        return NodeInfo(f'[args...]', '')
    if isinstance(node, ast.Compare):
        return NodeInfo(f'compare', '#c48ad1')
    if isinstance(node, ast.Call):
        return NodeInfo(f'call()', '#c48ad1')
    if isinstance(node, ast.Subscript):
        return NodeInfo(f'[]', '#c48ad1')
    if isinstance(node, ast.BinOp):
        return NodeInfo(f'binary op', '#c48ad1')
    if isinstance(node, ast.UnaryOp):
        return NodeInfo(f'unary op', '#c48ad1')
    if isinstance(node, ast.Slice):
        return NodeInfo(f':', '#8fd1f7')
    if isinstance(node, ast.Module):
        return NodeInfo(f'Module', '')
    return NodeInfo(str(type(node)), '')


def _build_graph(node: ast.AST, graph: nx.DiGraph):
    node_id = graph.number_of_nodes()
    node_info = _get_node_info(node)
    graph.add_node(node_id, label=node_info.label, color=node_info.color, style='filled')
    for k, v in ast.iter_fields(node):
        if not isinstance(v, list):
            v = [v]
        for child in v:
            if isinstance(child, ast.AST) and not isinstance(child, ast.Load) and not isinstance(child, ast.Store):
                graph.add_edge(node_id, _build_graph(child, graph))
    return node_id


def _draw_graph(graph: nx.DiGraph, file: Path):
    if not file.parent.exists():
        file.parent.mkdir(parents=True)
    nx.drawing.nx_pydot.to_pydot(graph).write_png(str(file))


def draw_ast(source_path: Path, image_path: Path):
    source_node = ast.parse(source_path.read_text())
    graph = nx.DiGraph()
    _build_graph(source_node, graph)
    _draw_graph(graph, image_path)
