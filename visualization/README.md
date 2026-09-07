# MRI Probe Detection — Visualization

Python tools for visualizing MRI probe detection results on scalp surface meshes.

This module is part of the [MRIProbeDetection](https://github.com/assuntaciarlo/MRIProbeDetection) repository and provides visualization of:

* scalp surface curvature
* probe detection results using interactive 3D visualization

The visualization is implemented using [PyVista](https://pyvista.org/) and supports BrainVoyager surface (`.srf`), probe (`.probej`), and surface map (`.smp`) files through `bvbabel`.

## Directory structure

```text
visualization/
├── data/
│   ├── sub-03/
│   └── sub-08/
├── src/
│   ├── 1-visualize_results.py
│   └── utils/
│       ├── __init__.py
│       ├── probej.py
│       └── srf.py
├── requirements.txt
└── README.md
```

### `src/1-visualize_results.py`

Main visualization script. It:

1. Loads a BrainVoyager scalp surface.
2. Visualizes the mean curvature of the surface.
3. Visualizes a probe mask.
4. Loads probe detection results.
5. Converts probe source and detector coordinates to the coordinate convention used by PyVista.
6. Displays probe locations and labels on the cortical surface.

### `src/utils/`

Contains utilities for reading BrainVoyager file formats used by the visualization scripts:

* `srf.py` — reads BrainVoyager `.srf` surface files.
* `probej.py` — reads BrainVoyager `.probej` probe files.

## Requirements

The code is intended for **Python 3.10**.

The main dependencies are:

```text
numpy==1.26.4
pyvista==0.44.1
bvbabel
```

See [`requirements.txt`](requirements.txt) for the complete list.

## Installation

### Using Conda

Create a new Conda environment:

```bash
conda create -n mriprobe-visualization python=3.10
```

Activate the environment:

```bash
conda activate mriprobe-visualization
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

## Running the visualization

From the `visualization` directory:

```bash
python src/1-visualize_results.py
```

The script currently uses the example subject:

```python
subID = 'sub-03'
```

and expects the corresponding data under:

```text
visualization/data/sub-03/
```

## Input data

The visualization expects BrainVoyager files including:

### Scalp surface

```text
<subID>_standard_SPH.srf
```

The surface contains the scalp mesh vertices and triangular faces.

### Mean curvature

```text
mean_curvature_D0_S0_BVTrue.smp
```

This is used to visualize the mean curvature on the cortical surface.

### Probe mask

```text
<subID>_hd-patch.poi
```

The `.poi` file contains the surface vertices belonging to the probe mask.

### Probe detection results

The script can visualize `.probej` files containing probe source and detector coordinates and labels. For example:

```text
icp2_transformed_MNI_probes_FCP.probej
detected_recovered_probes_noSS_n27_iter100.probej
```

Additional `.probej` files can be added to the `probe_list` in the visualization script.

## Coordinate conversion

BrainVoyager and PyVista use different coordinate conventions. The visualization code performs the required coordinate transformation when loading the surface and probe coordinates.

For the cortical surface, the Z coordinate is flipped around the surface mesh center:

```python
mesh.points[:, 2] = (
    2 * mesh_center_z - mesh.points[:, 2]
)
```

Probe source and detector coordinates are transformed accordingly before being displayed.

## Related project

For the complete probe detection pipeline, see:

https://github.com/assuntaciarlo/MRIProbeDetection
