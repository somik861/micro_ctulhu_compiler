from abc import abstractmethod

from src.ast_nodes.INode import INode
from src.CommandFactory import CommandFactory
from src.common import Command, CompileResult
from src.Environment import Environment


class _BinaryOp(INode):
    def __init__(self, lhs: INode, rhs: INode) -> None:
        self._lhs = lhs
        self._rhs = rhs
    
    @abstractmethod
    def _get_command(self) -> Command: ...
    
    def compile(self, env: Environment, cmd_factory: CommandFactory) -> CompileResult:
        code: list[str] = []
        
        lhs_res = self._lhs.compile(env, cmd_factory)
        rhs_res = self._rhs.compile(env, cmd_factory)
        
        code += lhs_res.code
        code += rhs_res.code
        
        assert len(lhs_res.new_variables) == 1
        assert len(rhs_res.new_variables) == 1
        
        code += env.prepare_variables_for_use([lhs_res.new_variables[0], rhs_res.new_variables[0]], [0, 1], cmd_factory)
        resvar_name = env.get_unused_variable_name('add_result')
        
        code += cmd_factory.create_command(self._get_command(), [0, 1, 2])
        env.add_precreated_variable(resvar_name, 2)
        
        return CompileResult(code, [resvar_name])
    
class Add(_BinaryOp):
    def __init__(self, lhs: INode, rhs: INode) -> None:
        super().__init__(lhs, rhs)
        
    def _get_command(self) -> Command:
        return Command.Add