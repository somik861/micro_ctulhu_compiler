from src.ast_nodes.INode import CompileResult, INode
from src.CommandFactory import CommandFactory
from src.Environment import Environment


class UseVar(INode):
    def __init__(self, name: str) -> None:
        self._name = name
    
    def compile(self, env: Environment, cmd_factory: CommandFactory) -> CompileResult:
        assert env.get_variable_location(self._name) is not None
        return CompileResult([], [self._name])
