from dataclasses import dataclass
from random import choice, randint

from dataclasses_json import DataClassJsonMixin

from src.CommandFactory import CommandFactory
from src.common import Command


@dataclass
class Location(DataClassJsonMixin):
    stack: int
    depth: int


class Environment:
    def __init__(self) -> None:
        self._variables: dict[int, list[str]] = {i: [] for i in range(6)}

    def get_variable_location(self, name: str) -> Location | None:
        for stack_idx, stack in self._variables.items():
            for i, var in enumerate(stack):
                if var == name:
                    return Location(stack_idx, len(stack) - i - 1)

        return None

    def add_variable(self, name: str, value: int, cmd_factory: CommandFactory, ignore_indicies: set[int] | None = None) -> list[str]:
        """return index of stack that this variable is put on top of"""
        if ignore_indicies is None:
            ignore_indicies = set()

        idx = self._get_random_index(ignore_indicies)
        self._variables[idx].append(name)

        return cmd_factory.create_command(Command.Create, [value, idx])

    def add_precreated_variable(self, name: str, stack: int) -> None:
        """adds variable that was created by another source"""
        self._variables[stack].append(name)

    def move_variable_to_top(self, name: str, stack: int, cmd_factory: CommandFactory) -> list[str]:
        location = self.get_variable_location(name)
        assert location is not None

        tmp_stack = self._get_random_index({stack, location.stack})
        res_tmp_stack = self._get_random_index(
            {stack, location.stack, tmp_stack})
        code: list[str] = []
        for _ in range(location.depth):
            code += cmd_factory.create_command(Command.Move,
                                               [location.stack, tmp_stack])

        code += cmd_factory.create_command(Command.Move,
                                           [location.stack, res_tmp_stack])

        for _ in range(location.depth):
            code += cmd_factory.create_command(Command.Move,
                                               [tmp_stack, location.stack])

        code += cmd_factory.create_command(Command.Move,
                                           [res_tmp_stack, stack])

        self._variables[location.stack].remove(name)
        self._variables[stack].append(name)

        return code

    def prepare_variables_for_use(self, vars: list[str], indices: list[int], cmd_factory: CommandFactory) -> list[str]:
        """duplicates values of vars and puts them on indices"""
        assert len(vars) == len(indices)

        code: list[str] = []
        for var, idx in zip(vars, indices):
            code += self.move_variable_to_top(var, idx, cmd_factory)

        for idx in indices:
            tmp_idx = self._get_random_index({idx})
            code += cmd_factory.create_command(Command.Dup, [idx, tmp_idx])
            code += cmd_factory.create_command(Command.Move, [tmp_idx, idx])

        return code

    def get_unused_variable_name(self, suffix: str) -> str:
        num = randint(0, 2**16)
        name: str = ''
        while self.get_variable_location(name := f'__tmp__{num}_{suffix}') is not None:
            num = randint(0, 2**16)

        return name

    def drop_variable(self, name: str, cmd_factory: CommandFactory) -> list[str]:
        code: list[str] = []
        code += self.move_variable_to_top(name, 0, cmd_factory)
        code += cmd_factory.create_command(Command.Drop, [0])

        self._variables[0].pop()

        return code
    
    def clean_temporaries(self, cmd_factory: CommandFactory) -> list[str]:
        to_clean: list[str] = []
        for vars in self._variables.values():
            for var in vars:
                if var.startswith('__tmp__'):
                    to_clean.append(var)
                    
        code: list[str] = []
        for var in to_clean:
            code += self.drop_variable(var, cmd_factory)
        return code

    def duplicate_variable_to_new_variable(self, src_variable: str, new_variable: str, cmd_factory: CommandFactory) -> list[str]:
        code: list[str] = []
        code += self.move_variable_to_top(src_variable, 0, cmd_factory)
        code += cmd_factory.create_command(Command.Dup, [0, 1])
        self._variables[1].append(new_variable)
        return code

    def _get_random_index(self, ignore_indicies: set[int] | None = None) -> int:
        if ignore_indicies is None:
            ignore_indicies = set()
        indicies = set(self._variables.keys()) - ignore_indicies
        return choice(list(indicies))
