from src.ast_nodes.INode import CompileResult, INode
from src.CommandFactory import CommandFactory
from src.Environment import Environment


class CreateVar(INode):
    def __init__(self, name: str, value: int) -> None:
        self._name: str = name
        self._value: int = value
    
    def compile(self, env: Environment, cmd_factory: CommandFactory) -> CompileResult:
        code = env.add_variable(self._name, self._value, cmd_factory)
        return CompileResult(code)
