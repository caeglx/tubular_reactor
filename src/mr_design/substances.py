"""
Lookup classes for solvents and solids substance data.
"""

from dataclasses import astuple, dataclass
from enum import Enum


@dataclass(frozen=True)
class SolventProps:
    density: float  # kg/m^3
    heat_capacity: float  # J/(kg*K)
    viscosity: float  # Pa*s
    thermal_conductivity: float  # W/(m*K)


class Solvent(Enum):
    water = SolventProps(998, 4185, 0.001, 0.598)
    ethanol = SolventProps(789, 2430, 0.01074, 0.167)
    ethylacetate= SolventProps(894, 1920, 0.000423, 0.144)
    thf = SolventProps(890, 1720, 0.000456, 0.120)
    ethylenglycol = SolventProps(1110, 2357, 0.0161, 0.254)

    def __init__(self, props: SolventProps):
        self.density = props.density
        self.heat_capacity = props.heat_capacity
        self.viscosity = props.viscosity
        self.thermal_conductivity = props.thermal_conductivity

    def desc(self) -> SolventProps:
        """Access the dataclass for typing / convenience."""
        return self.value

    def props(self) -> tuple:
        return astuple(self.value)

    # # optional convenience properties to avoid writing `.spec.` repeatedly
    # @property
    # def density(self) -> float:
    #     return self.heat_capacity

@dataclass(frozen=True)
class SolidsProps:
    thermal_conductivity: float

class Solid(Enum):
    stainlesssteel = SolidsProps(15)
    ptfe = SolidsProps(0.25)
    pfa = SolidsProps(0.209)

    def __init__(self, props: SolidsProps) -> None:
        self.thermal_conductivity = props.thermal_conductivity


if __name__ == "__main__":
    solvent: Solvent = Solvent.water
    rho, cp, eta, lamb = solvent.props()
    print(lamb)
    print(solvent.thermal_conductivity)
