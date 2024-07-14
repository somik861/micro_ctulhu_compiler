from pathlib import Path
from typing import Any

import yaml

from src.ast_nodes.Sequence import Sequence


def parse_source_file(source: Path) -> Sequence:
    return parse_source_list(yaml.load(open(source, 'r', encoding='utf-8'), yaml.CLoader))
    

def parse_source_list(lst: list[Any]) -> Sequence:
    out = Sequence()
    for part in lst:
        pass
    
    return out
