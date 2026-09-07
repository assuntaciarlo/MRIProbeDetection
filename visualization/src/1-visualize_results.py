import pyvista as pv
from utils import srf, probej
from bvbabel import smp, poi
import numpy as np
import os

def create_pv_mesh(nodes, faces, mesh_center_z, indexing=0):

    # assuming triangular faces
    # the face array must contain as first element the number of points of each face
    faces = np.hstack((np.array([3] * faces.shape[0]).reshape(-1, 1), faces.astype(int) - indexing))
    mesh = pv.PolyData(nodes, np.vstack(faces))

    # flip L-R (needed given the different axis convention between pyvista and BrainVoyager)
    mesh.points.__array__()[:, 2] = 2 * mesh_center_z - mesh.points.__array__()[:, 2]

    # flip z axis for all normals
    mesh.point_normals.__array__()[:, 2] = -mesh.point_normals.__array__()[:, 2]
    mesh.face_normals.__array__()[:, 2] = -mesh.face_normals.__array__()[:, 2]

    return mesh

pv.global_theme.font.size = 50

subID = 'sub-03'
subdir = os.path.join('..', 'data', subID)

# ------------------------------------------------------------------
# Visualize scalp mean curvature
# ------------------------------------------------------------------

hdr, curvature = smp.read_smp(f'{subdir}/mean_curvature_D0_S0_BVTrue.smp')

srf_hdr, mesh_data = srf.read_srf(f'{subdir}/{subID}_standard_SPH.srf')

mesh = create_pv_mesh(mesh_data['vertices'], mesh_data['faces'], srf_hdr['Mesh center Z'], indexing=0)

plotter = pv.Plotter()
plotter.add_mesh(mesh,
                 scalars=np.squeeze(curvature),
                 cmap='coolwarm',
                 show_scalar_bar=True,
                 interpolate_before_map=True,
                 clim=0.2)
plotter.show()


# ------------------------------------------------------------------
# Visualize probe mask
# ------------------------------------------------------------------

poi_hdr, mask_data = poi.read_poi(f'{subdir}/{subID}_hd-patch.poi')
probe_mask = np.zeros(len(mesh_data['vertices']))
probe_mask[mask_data[0]['Vertices']] = 1

plotter = pv.Plotter()
plotter.add_mesh(mesh,
                 scalars=probe_mask,
                 cmap='coolwarm',
                 clim=1,
                 interpolate_before_map=False,
                 show_scalar_bar=False
                 )
plotter.show()


# ------------------------------------------------------------------
# Visualize probe detection results
# ------------------------------------------------------------------

probe_list = ['icp2_transformed_MNI_probes_FCP.probej',
              'detected_recovered_probes_noSS_n27_iter100.probej']

plot_colors = ['red',
               'green']

plotter = pv.Plotter()
plotter.add_mesh(mesh,
                 interpolate_before_map=False,
                 show_scalar_bar=False,
                 color='lightgray')

for i, probe_file in enumerate(probe_list):

    probe_data = probej.read_probej(f'{subdir}/{probe_file}')

    Zoffset = 2*srf_hdr['Mesh center Z']

    src_coords_to_surf = [[coord[1],coord[2], Zoffset - coord[0]] for coord in probe_data['Source Coordinates']]
    det_coords_to_surf = [[coord[1],coord[2], Zoffset - coord[0]] for coord in probe_data['Detector Coordinates']]

    plotter.add_points(np.array(src_coords_to_surf), render_points_as_spheres=True, point_size=15, color=plot_colors[i], label=probe_file)
    plotter.add_points(np.array(det_coords_to_surf), render_points_as_spheres=True, point_size=15, color=plot_colors[i])

plotter.add_point_labels(src_coords_to_surf,  probe_data['Source Labels'], shape_opacity=0, font_size=20, always_visible=True)
plotter.add_point_labels(det_coords_to_surf, probe_data['Detector Labels'], shape_opacity=0, font_size=20, always_visible=True)

legend = plotter.add_legend(face='circle', size=(0.5, 0.1), loc='upper left')
plotter.show()

