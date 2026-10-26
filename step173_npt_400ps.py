
from pathlib import Path
import openmm as mm
from openmm import app, unit

base = Path("03_Complex/Solvation")
prefix = "PfDHODH_FMN_BST_015M"

top = app.AmberPrmtopFile(
    str(base / "PfDHODH_FMN_BST_solvated_015M.prmtop")
)
crd = app.AmberInpcrdFile(
    str(base / f"{prefix}_restrained_minimized.inpcrd")
)

system = top.createSystem(
    nonbondedMethod=app.PME,
    nonbondedCutoff=1.0 * unit.nanometer,
    constraints=app.HBonds,
    rigidWater=True
)

# Restrain solute heavy atoms at 2 kcal/mol/A^2.
# k = 1673.6 kJ/mol/nm^2 in the 0.5*k*r^2 convention.
force = mm.CustomExternalForce(
    "0.5*k*((x-x0)^2+(y-y0)^2+(z-z0)^2)"
)
force.addGlobalParameter(
    "k", 1673.6 * unit.kilojoule_per_mole / unit.nanometer**2
)
for name in ("x0", "y0", "z0"):
    force.addPerParticleParameter(name)

positions = crd.positions.value_in_unit(unit.nanometer)
count = 0
for atom in top.topology.atoms():
    if atom.index < 6218 and atom.element.symbol != "H":
        p = positions[atom.index]
        force.addParticle(atom.index, [p.x, p.y, p.z])
        count += 1

system.addForce(force)
system.addForce(
    mm.MonteCarloBarostat(1 * unit.bar, 300 * unit.kelvin, 25)
)

integrator = mm.LangevinMiddleIntegrator(
    300 * unit.kelvin,
    1 / unit.picosecond,
    0.002 * unit.picoseconds
)

simulation = app.Simulation(
    top.topology,
    system,
    integrator,
    mm.Platform.getPlatformByName("CPU"),
    {"Threads": "4"}
)

simulation.loadState(str(base / f"{prefix}_NPT_300ps.xml"))

trajectory = base / f"{prefix}_NPT_300to400ps.dcd"
simulation.reporters.append(
    app.DCDReporter(str(trajectory), 5000)
)

print("=== Step 43I-3CN-173 ===", flush=True)
print("NPT 300-400 ps; restraint 2 kcal/mol/A^2", flush=True)
print("Restrained heavy atoms:", count, flush=True)

for i in range(10):
    simulation.step(5000)
    state = simulation.context.getState(getEnergy=True)
    volume = state.getPeriodicBoxVolume().value_in_unit(
        unit.nanometer**3
    )
    kinetic = state.getKineticEnergy()
    dof = 3 * system.getNumParticles() - system.getNumConstraints() - 3
    temperature = (
        2 * kinetic / (dof * unit.MOLAR_GAS_CONSTANT_R)
    ).value_in_unit(unit.kelvin)
    print(
        f"{310 + 10*i} ps | T={temperature:.1f} K | "
        f"V={volume:.2f} nm^3",
        flush=True
    )

output = base / f"{prefix}_NPT_400ps.xml"
simulation.saveState(str(output))

print("Saved state:", output, flush=True)
print("Saved trajectory:", trajectory, flush=True)
print("=== Step 173 completed ===", flush=True)
