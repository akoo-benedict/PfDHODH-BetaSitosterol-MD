# PfDHODH (6I4B)–beta-sitosterol molecular dynamics: reproducibility log

Status: living research record; last documented stage: 2026-10-17. All observations below are from user-shared terminal screenshots. No protein modifications or molecular dynamics simulations have yet been performed.

## Computing environment
- MD computer: HP EliteBook 830 G5, Intel Core i5-8350U, 4 cores/8 logical processors, 16 GB RAM, Windows 11 Pro, hardware virtualization enabled, integrated Intel graphics.
- WSL version 3.0.3.0; WSL2 Linux kernel 6.18.54.1-1.
- Ubuntu 24.04.5 LTS (noble), username `researcher`, home `/home/researcher`.
- GROMACS: Ubuntu package 2023.3-Ubuntu_2023.3_1ubuntu3; `/usr/bin/gmx`; mixed precision; 64-bit; thread_mpi; OpenMP enabled; GPU disabled; SIMD SSE4.1; FFTW 3.3.10; GCC 13.2.0.
- Ubuntu `sudo apt update` and `sudo apt upgrade` completed, per screenshots. No benchmark yet.

## Workspace
`/home/researcher/PfDHODH_BetaSitosterol_MD/`
Subdirectories: `01_Protein`, `02_Ligand`, `03_Docking`, `04_Topology`, `05_Minimization`, `06_Equilibration`, `07_Production_MD`, `08_Analysis`, `09_Figures`, `10_Reproducibility`.

## Source structure
- RCSB PDB ID: 6I4B; downloaded with `wget https://files.rcsb.org/download/6I4B.pdb` into `01_Protein`.
- HTTP 200 OK; download 1,079,730 bytes; file reported as approximately 1.1 MB.
- PDB header: Plasmodium falciparum mitochondrial dihydroorotate dehydrogenase (quinone), engineered construct, expressed in E. coli, X-ray diffraction, chains A and B.
- `grep '^HET ' 6I4B.pdb`: FMN A601 (31), ORO A602 (11), E2N A603 (22); FMN B601 (31), ORO B602 (11), E2N B603 (22). Parenthetical values are HET record atom counts, not occupancy.
- E2N is the crystallographic inhibitor; beta-sitosterol is not in the deposited complex.

## Missing residues (PDB REMARK 465)
Commands used:
```
grep '^REMARK 465' 6I4B.pdb | head -n 25
grep '^REMARK 465' 6I4B.pdb | tail -n 35
grep '^REMARK 465' 6I4B.pdb | awk '$4=="A" || $4=="B" {count[$4]++} END {print "Chain A:",count["A"],"missing residues"; print "Chain B:",count["B"],"missing residues"}'
grep '^REMARK 465' 6I4B.pdb | awk '$4=="A" {print}'
```
Observed: chain A 24 missing residues: 135-156 (22), 568-569 (2). Chain B 31 missing residues: 135-156 (22), 408-414 (7), 568-569 (2), consistent with the reported count and visible partial B listing. Verify the first B entry directly from the complete REMARK 465 record before manuscript submission.

## Scientific decisions still pending
1. Verify full REMARK 465 listing, experimental resolution, R/Rfree, structural quality, chain-specific binding-site integrity and biological assembly.
2. Assess missing-segment location; select chain/model and decide whether loop reconstruction is necessary. If modeled, record tool, template, settings, alternative models, validation and final coordinates.
3. Verify FMN, ORO, E2N chemistry and whether to retain each for the target simulation state. Preserve the deposited original.
4. Validate docking with redocking of E2N and document binding-site selection and reference RMSD.
5. Parameterize beta-sitosterol and retained cofactors consistently with the chosen protein force field.
6. Establish controls, replicas, equilibration, convergence, performance benchmark and production protocol before simulations.

## Evidence and provenance
Source: user-provided terminal screenshots from 2026-10-17. The working directory and files remain on the user's laptop; this log is a separate documentation copy, not a synchronization with that laptop.

## Missing-region proximity assessment

Structure: PDB 6I4B
Chain: A
Reference ligand: E2N
Software: PyMOL 3.1.0 and NumPy
Distance metric: Minimum heavy-atom distance

Met157 to E2N: 15.850189 Angstrom
Ser567 to E2N: 36.48544 Angstrom

Interpretation:
Both residues are outside the immediate 5 Angstrom
inhibitor-binding environment in the experimental structure.

These distances do not establish the positions or structural
effects of unresolved residues. Missing-region reconstruction
must be assessed separately before molecular dynamics.

## Internal missing-region boundary distance

Structure: PDB 6I4B
Chain: A
Missing residues: 384-413 (30 residues)
Flanking residues: Glu383 and Phe414

Measurement:
C-alpha to C-alpha distance = 3.798 Angstrom

Software: PyMOL 3.1.0

Interpretation:
The flanking residues are spatially close despite the
30-residue unresolved sequence segment. This does not
establish the conformation of the missing region.
The structural implications of the unresolved segment
must be evaluated before molecular dynamics simulations.

## Assessment of unresolved internal segment

Structure: PDB 6I4B
Protein: Plasmodium falciparum dihydroorotate dehydrogenase
Chain: A
Unresolved residues: 384-413 (30 residues)
Flanking residues: Glu383 and Phe414

### Structural measurements

Glu383-Phe414 C-alpha distance: 3.798 Angstrom
Glu383-E2N minimum heavy-atom distance: 32.313 Angstrom
Phe414-E2N minimum heavy-atom distance: 33.315 Angstrom

Software:
PyMOL 3.1.0
Python 3 with NumPy

### Interpretation

The unresolved 30-residue segment is bounded by two residues
whose C-alpha atoms are separated by 3.798 Angstrom.

Both flanking residues are relatively distant from the
crystallographic reference ligand E2N.

These measurements do not establish the conformation,
flexibility, or functional importance of the missing segment.

Structural reconstruction or another justified treatment
of the unresolved segment must be considered before
production molecular dynamics simulations.


## Correction: Engineered deletion in PfDHODH 6I4B

The earlier interpretation of residues 384-413 as an
unresolved 30-residue segment requires correction.

Inspection of the SEQADV records confirms that residues
385-413 (29 residues) are annotated as DELETION relative
to UniProt Q08210 in chain A.

The ATOM records show a numbering discontinuity between
Glu383 and Phe414, with a C-alpha distance of 3.798 Angstrom.

Residue position 384 requires further verification to
reconcile the coordinate numbering gap with the SEQADV records.

The engineered deletion must not be treated as an
experimentally unresolved loop.

For simulations of the crystallographic engineered construct,
deleted residues should not be reconstructed automatically.

This correction supersedes the earlier interpretation
of the internal numbering gap.


## Verification of engineered deletion: PDB 6I4B

Inspection of SEQADV records confirms that residues
384-413 (30 residues) are annotated as DELETION
relative to UniProt Q08210 in chains A and B.

Residue 384: SER (Serine), DELETION.

The coordinate numbering discontinuity between
Glu383 and Phe414 therefore corresponds to the
engineered deletion.

Measured C-alpha distance (chain A):
Glu383-Phe414 = 3.798 Angstrom.

Interpretation:
The 30-residue segment represents an engineered
deletion, not an experimentally unresolved loop.

The deleted residues should not be reconstructed
automatically when simulating the crystallographic
engineered construct.

Before molecular dynamics, peptide connectivity,
local geometry, and other missing residues must
be evaluated.


## Engineered deletion junction: peptide connectivity

Structure: PDB 6I4B
Chain: A
Engineered deletion: residues 384-413
Junction: Glu383-Phe414

Measured distances:
Glu383 CA - Phe414 CA = 3.798 Angstrom
Glu383 C - Phe414 N = 1.333 Angstrom

Interpretation:
The C-N distance is consistent with a normal peptide
bond length and supports geometric continuity across
the engineered deletion junction.

This measurement alone does not establish correct
bond angles, peptide planarity, or stereochemistry.

Further local structural validation is required
before molecular dynamics simulations.


## Engineered junction: omega dihedral validation

Structure: PDB 6I4B
Chain: A
Junction: Glu383-Phe414

Omega dihedral angle:
CA(Glu383)-C(Glu383)-N(Phe414)-CA(Phe414)

Measured omega = -179.09 degrees

Interpretation:
The omega angle is consistent with a trans peptide
bond and deviates by approximately 0.91 degrees
from ideal trans geometry.

Together with the C-N distance of 1.333 Angstrom,
this supports plausible peptide-bond geometry
at the engineered deletion junction.

Additional bond-angle and stereochemical validation
is required before molecular dynamics simulations.


## Engineered junction: backbone bond-angle validation

Structure: PDB 6I4B
Chain: A
Junction: Glu383-Phe414

Measured backbone angles:
CA383-C383-N414 = 116.13 degrees
C383-N414-CA414 = 120.98 degrees

Previously measured:
CA383-CA414 distance = 3.798 Angstrom
C383-N414 distance = 1.333 Angstrom
Omega dihedral angle = -179.09 degrees

Interpretation:
Both backbone bond angles are consistent with
expected peptide geometry.

Together with the peptide bond length and
trans omega configuration, these findings support
plausible local geometry at the engineered junction.

The engineered deletion of residues 384-413
should be retained when preparing the
crystallographic construct.

Full protein stereochemical validation and
assessment of other missing residues remain necessary
before molecular dynamics simulations.


## C-terminal structural assessment: PDB 6I4B

Structure: PfDHODH, PDB 6I4B
Chain examined: A

Last experimentally resolved residue:
Ser567

Missing C-terminal residues:
Lys568 and Ser569

Evidence:
REMARK 465 identifies residues 568–569 as missing
from the atomic coordinates in chains A and B.

SEQRES confirms the terminal Lys–Ser sequence.

No corresponding engineered-deletion annotation
was identified for these two residues in SEQADV.

Distance assessment:
Ser567 to crystallographic ligand E2N
Minimum heavy-atom distance = 36.48544 Angstrom

Software:
PyMOL 3.1.0
Python with NumPy

Interpretation:
Ser567 is spatially distant from the crystallographic
reference ligand E2N.

The missing C-terminal residues are unlikely to
participate directly in the crystallographic ligand
binding site.

This observation does not exclude possible effects
on protein dynamics or structural stability.

Preparation decision:
Provisionally retain the experimentally resolved
C-terminus at Ser567 without automatically
reconstructing Lys568–Ser569.

Appropriate terminal chemistry and additional
structural validation are required before
molecular dynamics simulation.

