from src.common import Command


class CommandFactory:
    def create_command(self, command: Command, args: list[int]) -> list[str]:
        return [f'x_{command.value}_{'_'.join(str(arg) for arg in args)}']
