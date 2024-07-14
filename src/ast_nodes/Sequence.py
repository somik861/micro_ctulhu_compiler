from src.ast_nodes.INode import INode
from src.CommandFactory import CommandFactory
from src.common import CompileResult
from src.Environment import Environment


class Sequence(INode):
    def __init__(self, nodes: list[INode] | None = None) -> None:
        self._nodes: list[INode] = [] if nodes is None else nodes
    
    def add_node(self, node: INode) -> None:
        self._nodes.append(node)
    
    def compile(self, env: Environment, cmd_factory: CommandFactory) -> CompileResult:
        code: list[str] = []
        for node in self._nodes:
            res = node.compile(env, cmd_factory)
            code += res.code
            code += env.clean_temporaries(cmd_factory)
            
        return CompileResult(code=code)
