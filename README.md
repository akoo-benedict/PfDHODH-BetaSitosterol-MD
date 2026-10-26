# PfDHODH–β-Sitosterol: Molecular Docking and Molecular Dynamics

## Associated manuscript
**Molecular Docking and Short-Timescale Molecular Dynamics Reveal Persistent Interactions of β-Sitosterol with Plasmodium falciparum Dihydroorotate Dehydrogenase**

## Study overview
This repository contains supporting files for molecular docking and a 9.6 ns molecular dynamics (MD) study of β-sitosterol in complex with Plasmodium falciparum dihydroorotate dehydrogenase (PfDHODH), retaining the FMN cofactor. The starting crystal structure was PDB 6I4B. The study examines the predicted binding pose, protein and ligand mobility, residue contacts, and a TYR342–β-sitosterol hydrogen-bond interaction.

## Software and computational methods
- Structure preparation: RDKit, Gemmi, Open Babel, Meeko and AmberTools-related workflows.
- Docking: AutoDock Vina, Vina scoring function.
- Molecular visualization: PyMOL 3.1.0 and BIOVIA Discovery Studio Visualizer 2020.
- Molecular dynamics: OpenMM, with AMBER ff19SB protein parameters and GAFF2-compatible ligand and FMN parameters.
- Computational platforms: local Windows Subsystem for Linux (Ubuntu) and Google Colab using an NVIDIA Tesla T4 GPU.
- Analysis: Python-based RMSD, RMSF, radius of gyration, residue-contact and hydrogen-bond analyses.

## Docking configuration
- Receptor: PfDHODH–FMN derived from PDB 6I4B.
- Ligand: β-sitosterol.
- Grid centre (Å): 16.528, -33.340, 35.492.
- Grid dimensions (Å): 24 × 24 × 24.
- Exhaustiveness: 32.
- Number of output modes: 20.
- Energy range: 5 kcal/mol.
- Random seed: 20261021.
- Best reported docking score: -8.081 kcal/mol.

## Molecular dynamics protocol
The PfDHODH–FMN–β-sitosterol system underwent energy minimization and NPT equilibration before production simulation. Production MD was performed at 300 K and 1 bar with a 2 fs integration step, particle mesh Ewald electrostatics, a 1.0 nm nonbonded cutoff, constrained hydrogen-containing bonds, and a Monte Carlo barostat. The completed production trajectory covers 9.6 ns and was analyzed using 960 saved frames.

## Reported analysis results
- Mean protein backbone RMSD: 1.221 Å.
- Mean ligand RMSD: 3.002 Å.
- Mean Cα RMSF: 0.585 Å.
- Mean protein radius of gyration: 20.163 Å.
- TYR342 heavy-atom contact occupancy (4 Å cutoff): 99.79%.
- TYR342–β-sitosterol hydrogen-bond geometry occupancy (distance ≤ 3.5 Å and angle ≥ 150°): 86.77%.

These values describe a single short-timescale simulation and do not establish experimental inhibition or long-term binding stability.

## Repository contents
- `01_Docking_Files/`: docking input structures, configuration, poses and related files.
- `03_MD_Analysis_CSV/`: quantitative MD analysis datasets.
- `04_Manuscript_Figures/`: figures supporting the manuscript.
- `05_PyMOL_3D_Interactions/`: 3D molecular interaction visualizations.
- `06_DiscoveryStudio_2D_Interactions/`: 2D interaction visualizations.
- `10_Reproducibility/`: structure checksum, pocket-residue information and reproducibility log.
- `step173_npt_400ps.py` through `step177_npt_2000ps.py`: equilibration scripts.
- `step185_production_md.py`: production MD script.

## Trajectory availability
The full 9.6 ns production trajectory consists of sequential DCD segments and has not yet been deposited in this repository. A separate archive location will be added when the trajectory dataset is deposited. The currently available CSV files support inspection of the reported trajectory analyses.

## Reproducibility notes
The repository contains selected inputs, analysis outputs, scripts and methodological records. Consult the original scripts and reproducibility log for the exact implementation. Additional system topology and trajectory data may be needed to reproduce the entire simulation from its initial state.

## Citation
If using this repository, cite the associated manuscript when its publication details become available and identify the repository URL and accessed revision.

## Repository URL
https://github.com/akoo-benedict/PfDHODH-BetaSitosterol-MD
