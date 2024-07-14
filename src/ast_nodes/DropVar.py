from src.ast_nodes.INode import CompileResult, INode
from src.CommandFactory import CommandFactory
from src.Environment import Environment


class DropVar(INode):
    def __init__(self, name: str) -> None:
        self._name = name
    
    def compile(self, env: Environment, cmd_factory: CommandFactory) -> CompileResult:
        return CompileResult(env.drop_variable(self._name, cmd_factory))
