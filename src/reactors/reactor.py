from math import pi as PI, log, sqrt
from typing import Final
import numpy as np
from .substances import Solvent, Solid

SEC_PER_MIN: Final[int] = 60  # s/min
ML_PER_M3: Final[float] = 1e6  # ml/m^3
INCH_TO_METER: Final[float] = 0.0254  # m/inch
RE_LAM_LIM: Final[int] = 2300
DIFFUSION_LIQUID: Final[float] = 1e-9  # m^2/s

reactor_outer_diameter: dict[str, float] = {
    "1/8": INCH_TO_METER * 1 / 8,
    "1/16": INCH_TO_METER * 1 / 16,
}

#NOTE: Values for twisting Bodenstein number calculation
dean_values: list[int] = [10, 20, 30, 40, 50]
y_axis_values: list[float] = [11, 10.5, 10, 9, 8]


class Reactor:
    def __init__(self, inner_diameter_mm: float, outer_diameter_inch: float, length: float = 0.0) -> None:
        """
        Reactor dimensions
        
        Parameters:
            inner_diameter_mm (float): Internal reactor diameter in millimeter
            outer_diameter_inch (float): Outer reactor diameter in inch (1/16 or 1/8)
            length (float): Optional, length of reactor in m. Not needed if length is getting calculated.
        """
        self.inner_diameter: float = inner_diameter_mm / 1e3
        self.outer_diameter: float = outer_diameter_inch * INCH_TO_METER
        self.length: float = length
        self.area: float = PI * self.inner_diameter * length
        self.cross_section_area: float = PI / 4 * self.inner_diameter**2

    def __str__(self) -> str:
        return f"Reactor with an inner diameter of {self.inner_diameter * 1e3:.2f} mm, outer diamter of \
                 {self.outer_diameter * 1e3:.2f} mm and a length of {self.length:.2f} m"

    def bodenstein(self, flow_rate_mlmin: float, solvent: Solvent, twisting_radius_mm: float | None = None) -> None:
        """
        Calculate the bodenstein number of the previous defined reactor for a specific flow rate and solvent

        Parameters:
            flow_rate_mlmin (float): Total flow rate for reactor in ml/min
            solvent (Solvent): Possible solvents like 'Solvent.ethanol' with their material properties from the substances.py file
            twisting_radius(mm): Optional, radius of twisting when working with a twisted reactor based on Erdgogan & Chatwin 1967
        """

        self.flow_rate: float = flow_rate_mlmin / (SEC_PER_MIN * ML_PER_M3)
        self.velocity: float = self.flow_rate / self.cross_section_area
        self.tau: float = self.length / self.velocity

        rho: float = solvent.density
        eta: float = solvent.viscosity

        self.reynolds_number = rho * self.velocity * self.inner_diameter / eta
        self.diffusion_axial: float = DIFFUSION_LIQUID + (self.velocity**2 * self.inner_diameter**2) / (192 * DIFFUSION_LIQUID)
        self.bodenstein_number: float = self.velocity * self.length / self.diffusion_axial
        print(f"Bodenstein number of straight reactor is {self.bodenstein_number:.1f}.")

        if twisting_radius_mm:
            twisting_radius: float = twisting_radius_mm / 1000
            dean_number: float = self.reynolds_number * sqrt(self.inner_diameter / (2 * twisting_radius))
            y_axis_value: float = np.interp(dean_number, dean_values, y_axis_values)
            #TODO: Add warning if twisted axial diffusion is not interpolated but extrapolated
            self.diffusion_axial_twisted: float = self.diffusion_axial / ((1 / 192 * 10000) / y_axis_value)
            self.bodenstein_number_twisted: float = self.velocity * self.length / self.diffusion_axial_twisted
            print(f"Bodenstein number of twisted reactor is {self.bodenstein_number_twisted:.1f}.")
    
    def time_to_stationary(self, percent_steady: int, n_residence_times: float = 3) -> None:
        """
        Calculate time until steady state is reached to a certain percentage

        Paramters:
            percent_steady (int): Quantity value in percent at which the steady state is reached
            n_residence_times (float): Default 3, number of residence times to calculate
        """

        # Use diffusion of twisted reactor if that has been previous calculated
        try:
            self.diffusion_axial_twisted
            diffusion_axial = self.diffusion_axial_twisted
        except:
            diffusion_axial = self.diffusion_axial

        n = 100  # number of spatial nodes
        n_residence_times = 3
        dx = self.length / (n - 1)
        dt = 0.5 * min(dx / self.velocity, dx**2 / (2 * diffusion_axial))  # for explicit stability
        t_max = n_residence_times * self.length / self.velocity
        steps = int(t_max / dt)

        # Initial concentration profile: fluid A = 0 everywhere
        conc: np.ndarray = np.zeros(n)
        conc_out: np.ndarray = np.zeros(steps)

        # Time stepping using explicit forward integration on advection-dispersion
        for idx in range(steps):
            conc[0] = 1.0  # inlet switched to fluid B (C=1)
            conc_n = conc.copy()
            for i in range(1, n-1):
                adv = -self.velocity * (conc[i] - conc[i-1]) / dx
                diff = diffusion_axial * (conc[i+1] - 2*conc[i] + conc[i-1]) / dx**2
                conc_n[i] = conc[i] + dt*(adv + diff)
            conc_n[-1] = conc_n[-2]
            conc = conc_n
            conc_out[idx] = conc[-1]

        # Compute breakthrough time
        value_steady: float = percent_steady / 100
        times = np.linspace(0, t_max, steps)
        t_steady: float = np.interp(value_steady, conc_out, times)
        tau_steady = t_steady / self.tau
        print(f"{percent_steady} % of stationary achieved after {tau_steady:.1f} residence times or {t_steady:.1f} s.")


    #NOTE: Specify the temperature at the outlet or the remaining temperature difference for wich the length is getting calculated?
    def preheating(self, flow_rate_mlmin: float, initial_temperature_degC: float, outlet_temperature_degC: float,
                   cooling_temperature_degC: float, solvent: Solvent, solid: Solid) -> None:
        """
        Calculate tube length to reach outlet temperature.

        Parameters:
            flow_rate_mlmin (float): Volume flow rate in ml/min.
            initial_temperature_degC (float): Initial temperature in degree Celsius.
            cooling_temperature_degC (float): Cooling temperature in degree Celsius.
            solvent (Solvent): Possible solvents like'Solvent.ethanol' with their material properties from the substances.py file
            solid (Solid): Possible solvents like 'Solid.ptfe' with their paterial properties from the substances.py file
        """

        flow_rate: float = flow_rate_mlmin / (SEC_PER_MIN * ML_PER_M3)

        rho, cp, eta, lamb = solvent.props()
        tube_lamb: float = solid.thermal_conductivity
        
        mass_flow_rate = flow_rate * rho
        velocity = flow_rate / self.cross_section_area

        reynolds_number = velocity * self.inner_diameter * rho / eta
        if reynolds_number > RE_LAM_LIM:
            print(f"Flow is not fully laminar with a Reynolds number of {reynolds_number:.0f}.")
        nusselt_number = 3.66
        alpha_inner = nusselt_number * lamb / self.inner_diameter 
        heat_transfer_coefficient = 1 / (1 / alpha_inner + self.inner_diameter / (2 * tube_lamb)\
            * log(self.outer_diameter / self.inner_diameter))

        length_outlet_temperature = log((outlet_temperature_degC - cooling_temperature_degC)\
            / (initial_temperature_degC - cooling_temperature_degC))\
            * -(mass_flow_rate * cp) / (heat_transfer_coefficient * PI * self.inner_diameter)
        print(f"{length_outlet_temperature:.2f} m are needed to reach {outlet_temperature_degC} °C at the outlet.")
        self.length = length_outlet_temperature
        # NOTE: other idea is to calculate temperature based on length
        # outlet_temperature_degC = cooling_temperature_degC + (initial_temperature_degC - cooling_temperature_degC) * exp(-U * self.area / (mass_flow_rate * cp))
        # print(f"Temperature at the outlet is {outlet_temperature_degC:.2f} °C.")

