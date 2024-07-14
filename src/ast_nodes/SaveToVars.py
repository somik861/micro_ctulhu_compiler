from src.ast_nodes.INode import CompileResult, INode
from src.CommandFactory import CommandFactory
from src.Environment import Environment


class SaveToVars(INode):
    def __init__(self, names: list[str], node: INode) -> None:
        self._names = names
        self._node = node
    
    def compile(self, env: Environment, cmd_factory: CommandFactory) -> CompileResult:
        res = self._node.compile(env, cmd_factory)
        
        code: list[str] = []
        code += res.code
        for old_var, new_var in zip(res.new_variables, self._names):
            code += env.duplicate_variable_to_new_variable(old_var, new_var, cmd_factory)

        return CompileResult(code, [])