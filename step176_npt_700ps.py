
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

# Restrain solute heavy atoms at 0 kcal/mol/A^2.
# k = 418.4 kJ/mol/nm^2 in the 0.5*k*r^2 convention.
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

# Restore positions, velocities and periodic box from the
# restrained state without restoring its obsolete parameter k.
saved = mm.XmlSerializer.deserialize(
    (base / f"{prefix}_NPT_600ps.xml").read_text()
)
simulation.context.setPeriodicBoxVectors(
    *saved.getPeriodicBoxVectors()
)
simulation.context.setPositions(saved.getPositions())
simulation.context.setVelocities(saved.getVelocities())
simulation.context.setTime(saved.getTime())

trajectory = base / f"{prefix}_NPT_600to700ps.dcd"
simulation.reporters.append(
    app.DCDReporter(str(trajectory), 5000)
)

print("=== Step 43I-3CN-176 ===", flush=True)
print("NPT 600-700 ps; restraint 0 kcal/mol/A^2", flush=True)

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
        f"{610 + 10*i} ps | T={temperature:.1f} K | "
        f"V={volume:.2f} nm^3",
        flush=True
    )

output = base / f"{prefix}_NPT_700ps.xml"
simulation.saveState(str(output))

print("Saved state:", output, flush=True)
print("Saved trajectory:", trajectory, flush=True)
print("=== Step 176 completed ===", flush=True)
