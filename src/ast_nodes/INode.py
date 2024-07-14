from abc import ABC, abstractmethod

from src.CommandFactory import CommandFactory
from src.common import CompileResult
from src.Environment import Environment


class INode(ABC):
    @abstractmethod
    def compile(self, env: Environment, cmd_factory: CommandFactory) -> CompileResult: ...
    """compile the node into ctulhu code"""
