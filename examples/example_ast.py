from src.ast_nodes.BinaryOp import Add
from src.ast_nodes.Constant import Constant
from src.ast_nodes.CreateVar import CreateVar
from src.ast_nodes.DropVar import DropVar
from src.ast_nodes.INode import INode
from src.ast_nodes.SaveToVars import SaveToVars
from src.ast_nodes.Sequence import Sequence
from src.ast_nodes.UseVar import UseVar


def get_add_ast() -> INode:
    return Sequence([
        CreateVar('x', 1),
        CreateVar('y', 2),
        SaveToVars(
            ['z'],
            Add(
                Add(
                    UseVar('x'),
                    UseVar('y')
                ),
                Constant(3)
            )),
        DropVar('x'),
        DropVar('y')
    ])
