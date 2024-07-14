from src.ast_nodes.INode import CompileResult, INode
from src.CommandFactory import CommandFactory
from src.Environment import Environment


class Constant(INode):
    def __init__(self, value: int) -> None:
        self._value = value
    
    def compile(self, env: Environment, cmd_factory: CommandFactory) -> CompileResult:
        name = env.get_unused_variable_name('constant')
        
        code: list[str] = []
        code += env.add_variable(name, self._value, cmd_factory)
        
        return CompileResult(code, [name])
