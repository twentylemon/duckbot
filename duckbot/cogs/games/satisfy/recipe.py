from dataclasses import dataclass
from typing import List

from .building import Building
from .item import Form, Item
from .rates import Rates


@dataclass
class Recipe:
    name: str
    building: Building
    inputs: Rates
    outputs: Rates

    def __hash__(self):
        return hash(self.name)


@dataclass
class ModifiedRecipe:
    original_recipe: Recipe
    power_shards: int
    sloops: int

    def __hash__(self):
        return hash(self.name)

    @property
    def name(self) -> str:
        return f"{self.original_recipe.name}#{self.power_shards}#{self.sloops}"

    @property
    def building(self) -> Building:
        return self.original_recipe.building

    @property
    def inputs(self) -> Rates:
        return self.original_recipe.inputs * self.shard_scale

    @property
    def outputs(self) -> Rates:
        return self.original_recipe.outputs * self.shard_scale * self.sloop_scale

    @property
    def shard_scale(self) -> float:
        return 1.0 + self.power_shards * 0.5 if self.building.max_shards > 0 else 1.0

    @property
    def sloop_scale(self) -> float:
        return 1.0 + self.sloops / self.building.max_sloop if self.building.max_sloop > 0 else 1.0


def default() -> List[Recipe]:
    return [
        smelt("IronIngot", Item.IronOre * 30 >> Item.IronIngot * 30),
        ctor("IronPlate", Item.IronIngot * 30 >> Item.IronPlate * 20),
        ctor("IronRod", Item.IronIngot * 30 >> Item.IronRod * 30),
        refine("Plastic", Item.CrudeOil * 30 >> Item.Plastic * 20 + Item.HeavyOilResidue * 10),
        refine("Rubber", Item.CrudeOil * 30 >> Item.Rubber * 20 + Item.HeavyOilResidue * 20),
    ]


def awesome_sink() -> List[Recipe]:
    return [sink(item) for item in Item if item.form == Form.Solid and item.points > 0]


def all() -> List[Recipe]:
    return default() + recycled() + awesome_sink()


def recipe(name: str, building: Building, inout: tuple[Rates, Rates]) -> Recipe:
    return Recipe(name, building, inputs=inout[0], outputs=inout[1])


def smelt(name: str, inout: tuple[Rates, Rates]) -> Recipe:
    return recipe(name, Building.Smelter, inout)


def ctor(name: str, inout: tuple[Rates, Rates]) -> Recipe:
    return recipe(name, Building.Constructor, inout)


def assy(name: str, inout: tuple[Rates, Rates]) -> Recipe:
    return recipe(name, Building.Assembler, inout)


def manu(name: str, inout: tuple[Rates, Rates]) -> Recipe:
    return recipe(name, Building.Manufacturer, inout)


def refine(name: str, inout: tuple[Rates, Rates]) -> Recipe:
    return recipe(name, Building.Refinery, inout)


def pack(name: str, inout: tuple[Rates, Rates]) -> Recipe:
    return recipe(name, Building.Packager, inout[0] + Item.EmptyCanister * list(inout[0].rates.values())[0] >> inout[1])


def unpack(name: str, inout: tuple[Rates, Rates]) -> Recipe:
    return recipe(name, Building.Packager, inout[0] >> inout[1] + Item.EmptyCanister * list(inout[1].rates.values())[0])


def blend(name: str, inout: tuple[Rates, Rates]) -> Recipe:
    return recipe(name, Building.Blender, inout)


def sink(item: Item) -> Recipe:
    return recipe(f"Sink{item}", Building.AwesomeSink, item * 1 >> Item.AwesomeTicketPoints * item.points)


def bioburn(name: str, input: Rates) -> Recipe:
    return recipe(name, Building.BiomassBurner, input >> Item.MwPower * 30)


def recycled() -> List[Recipe]:
    return [
        refine("HeavyOilResidue", Item.CrudeOil * 30 >> Item.HeavyOilResidue * 40 + Item.PolymerResin * 20),
        refine("RecycledPlastic", Item.Rubber * 30 + Item.Fuel * 30 >> Item.Plastic * 60),
        refine("RecycledRubber", Item.Plastic * 30 + Item.Fuel * 30 >> Item.Rubber * 60),
        refine("ResidualPlastic", Item.PolymerResin * 60 + Item.Water * 20 >> Item.Plastic * 20),
        refine("ResidualRubber", Item.PolymerResin * 40 + Item.Water * 40 >> Item.Rubber * 20),
        refine("DilutedPackagedFuel", Item.HeavyOilResidue * 30 + Item.PackagedWater * 60 >> Item.PackagedFuel * 60),
        pack("PackagedWater", Item.Water * 60 >> Item.PackagedWater * 60),
        unpack("UnpackageFuel", Item.PackagedFuel * 60 >> Item.Fuel * 60),
    ]
