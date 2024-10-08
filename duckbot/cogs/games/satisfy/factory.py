from dataclasses import dataclass
from typing import List, Set

from .item import Item
from .rates import Rates
from .recipe import Recipe


@dataclass
class Factory:
    inputs: Rates
    recipes: List[Recipe]
    targets: Rates
    maximize: Set[Item]
    power_shards: int = 0
    sloops: int = 0
