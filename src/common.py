from dataclasses import dataclass, field
from enum import Enum
from random import choice

from dataclasses_json import DataClassJsonMixin


@dataclass
class CompileResult(DataClassJsonMixin):
    code: list[str] = field(default_factory=list)
    new_variables: list[str] = field(default_factory=list)
        
class Command(Enum):
    Move = 'move'
    Create = 'create'
    Add = 'add'
    Dup = 'dup'
    Drop = 'drop'