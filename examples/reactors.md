From the reactors module, the classes of `Reactor`, `Solvent` and `Solid` are getting imported for the functions as well as the substance data for possible fluids inside the reactor and the reactor material itself.

```python
from reactors import Reactor, Solvent, Solid
```

This reactor is getting created with an inner diameter of 1 mm, an outer diameter of 1/16 inch since that is the used unit by the manufacturers and the length. All non-SI-unit-parameters are accordingly named.

```python
reac1 = Reactor(inner_diameter_mm=1, outer_diameter_inch=1/16, length=5)
```

The Bodenstein number is getting calculated for a flow of 2 ml/min with the properties of the solvent tetrahydrofuran. For self-made coiled microreactors, an optional parameter is the coiling or twisting radius.

```python
reac1.bodenstein(flow_rate_mlmin=2.0, solvent=Solvent.thf, twisting_radius_mm=10)
```

Despite the high Bodenstein number, setting changes still have an axial diffusion. The idea is to simulate this dispersion and calculate the number or residence times and times in seconds until a specific switch percentage occurred.

```python
reac1.time_to_stationary(percent_steady=99)
```

Though, heat transfer is excellent in microreactors, it does not appear instantaneously. A preheating path in front of the mixer and the reaction path is therefore recommended. The used flow rate here is the one of the single reactant flows while the initial temperature, the outlet temperature and the cooling temperature are self-explanatory as well as the need for solvent and solid specifications.

```python
reac1.preheating(flow_rate_mlmin=1.0, initial_temperature_degC=20, outlet_temperature_degC=0.5, cooling_temperature_degC=0, solvent=Solvent.thf, solid=Solid.ptfe)
```

