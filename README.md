# MRI Probe Detection (work in progress ...)

Simultaneous fNIRS-fMRI acquisition is essential to ensure accurate inter-modality comparison by avoiding confounding factors deriving from separate measurement sessions. However, accurate localisation of fNIRS probes is crucial for joint analysis. Existing methods rely on fiducial markers (e.g., Vitamin E capsules) or external digitisation tools. In this project, we propose an alternative method that identifies optode pressure points directly visible in T1-weighted (T1w) MR images for detecting probe locations.

The project is designed to identify probe locations from MRI data and recover their anatomical positions on the scalp surface. The resulting probe positions can be compared with reference probe configurations and visualized together with scalp surface data. The probe detection pipeline consists of a semi-automatic procedure described below.

<img width="1280" height="720" alt="pipeline" src="https://github.com/user-attachments/assets/941ba34a-092f-4c89-b99c-da2431c82e49" />

## Repository structure

The repository contains tools for evaluating and visualizing the resulting probe locations.

```text
MRIProbeDetection/
├── doc/
│   └── Documentation and supporting material
│
├── visualization/
│   ├── src/
│   │   ├── 1-visualize_results.py
│   │   └── utils/
│   ├── data/
│   ├── requirements.txt
│   └── README.md
│
├── LICENSE
└── README.md
```

## Visualization and quality control

The visualization module provides an interactive way to inspect the detected probe configuration on the scalp surface using [PyVista](https://pyvista.org/).
Reference and detected probe positions can be displayed together, allowing the detection and registration results to be visually inspected.

The visualization module supports BrainVoyager surface and probe-related file formats and provides interactive 3D visualization of:

* scalp surface meshes
* surface curvature
* probe masks
* detected probe configurations
* reference probe configurations

See the [visualization README](visualization/README.md) for installation and usage instructions.

## Documentation

Additional documentation and supporting material can be found in the [`doc/`](doc/) directory, including a detailed description of all output files.

## License

This project is distributed under the [MIT License](LICENSE).

