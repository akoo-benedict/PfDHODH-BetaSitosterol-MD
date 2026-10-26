from pathlib import Path
import openmm as mm
from openmm import app, unit

base = Path("03_Complex/Solvation")
prefix = "PfDHODH_FMN_BST_015M"
out = base / "Production_MD"
out.mkdir(exist_ok=True)

top = app.AmberPrmtopFile(
    str(base / "PfDHODH_FMN_BST_solvated_015M.prmtop")
)

system = top.createSystem(
    nonbondedMethod=app.PME,
    nonbondedCutoff=1.0 * unit.nanometer,
    constraints=app.HBonds,
    rigidWater=True
)

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

# Identify the latest completed production segment.
completed = sorted(
    int(p.stem.split("_")[-1])
    for p in out.glob("state_*.xml")
    if p.stem.split("_")[-1].isdigit()
)

start = completed[-1] if completed else 0

if start:
    saved_path = out / f"state_{start}.xml"
else:
    saved_path = base / f"{prefix}_NPT_700ps.xml"

saved = mm.XmlSerializer.deserialize(saved_path.read_text())

simulation.context.setPeriodicBoxVectors(
    *saved.getPeriodicBoxVectors()
)
simulation.context.setPositions(saved.getPositions())
simulation.context.setVelocities(saved.getVelocities())
simulation.context.setTime(saved.getTime())

print("=== Step 185: Production MD ===", flush=True)
print("Restart state:", saved_path, flush=True)
print("Completed production:", start * 0.1, "ns", flush=True)
print("Target production: 10 ns", flush=True)

for segment in range(start + 1, 101):
    trajectory = out / f"trajectory_{segment:03d}.dcd"

    reporter = app.DCDReporter(str(trajectory), 5000)
    simulation.reporters.append(reporter)

    simulation.step(50000)

    simulation.reporters.remove(reporter)

    state_path = out / f"state_{segment}.xml"
    simulation.saveState(str(state_path))

    print(
        f"Completed {segment * 0.1:.1f} ns / 10.0 ns",
        flush=True
    )

print("=== Production MD completed ===", flush=True)
