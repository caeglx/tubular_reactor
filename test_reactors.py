from reactors import Reactor, Solvent, Solid  # this way the classes are getting imported
# import reactors.reactor  # and this way the complete file 

reac1 = Reactor(inner_diameter_mm=1, outer_diameter_inch=1/16, length=5)
reac1.bodenstein(flow_rate_mlmin=2.0, solvent=Solvent.thf, twisting_radius_mm=10)
reac1.time_to_stationary(percent_steady=99)

reac2 = Reactor(0.5, 1/16, 5)
reac2.bodenstein(flow_rate_mlmin=0.5, solvent=Solvent.thf, twisting_radius_mm=10)
reac2.time_to_stationary(percent_steady=99)
reac2.preheating(flow_rate_mlmin=0.25, initial_temperature_degC=20, outlet_temperature_degC=0.5, cooling_temperature_degC=0, solvent=Solvent.thf, solid=Solid.ptfe)
