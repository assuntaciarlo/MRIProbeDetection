'''Add functions to write and read json files with the newly create probe coordinates '''

import json

def write_probej(data_dict, filename):


    # Serializing json
    json_object = json.dumps(data_dict, indent=4)

    print(f'Writing file: {filename}')
    
    with open(filename, 'w') as f:
        f.write(json_object)

    print('Done.')    


def read_probej(filename):

    data = json.load(open(filename,'r'))

    return data    


def create_probej():

    data = dict()

    data['File Version'] = '0.2'
    data['Space'] = ''
    data['Reference Surface'] = ''
    data['Source Labels'] = []
    data['Detector Labels'] = []
    data['Source Coordinates'] = []
    data['Detector Coordinates'] = []
    data['Anatomical Landmarks'] = {}
    data['Custom Landmarks'] = {} # other custom landmarks that the user can define (not standard EEG)

    return data


def save_to_probej(ref_mesh, ref_mesh_filename, outfilename, src_coords=None, det_coords=None, src_labels=[],
                   det_labels=[],custom_landmark_dict={}, anatomical_landmask_dict={}, space='BV'):

    # TO DO: extend the function to Custom Landmarks and Anatomical Landmarks

    probe_dict = create_probej()
    probe_dict['Space'] = space
    probe_dict['Reference Surface'] =ref_mesh_filename

    if src_labels and det_labels:
        probe_dict['Source Labels'] = src_labels
        probe_dict['Detector Labels'] = det_labels

        if space == 'BV':
            # NOTE: when saving the coordinates we need to invert the axis to match BV coordinate system
            # BV_coords = my_coords[2,0,1]
            # we need also to invert the z axis
            zoffset = 2 * ref_mesh.center[2]

            # Reorient coordinates
            src = [[zoffset - v[2], v[0], v[1]] for v in src_coords]
            det = [[zoffset - v[2], v[0], v[1]] for v in det_coords]
        else:
            src = src_coords
            det = det_coords

        probe_dict['Source Coordinates'] = src
        probe_dict['Detector Coordinates'] = det

    if custom_landmark_dict:

        if space == 'BV':
            zoffset = 2 * ref_mesh.center[2]

            for k in custom_landmark_dict.keys():
                custom_landmark_dict[k] =[zoffset - custom_landmark_dict[k][2], custom_landmark_dict[k][0], custom_landmark_dict[k][1]]

        probe_dict['Custom Landmarks'] = custom_landmark_dict

    if anatomical_landmask_dict:

        if space == 'BV':
            zoffset = 2 * ref_mesh.center[2]

            for k in anatomical_landmask_dict.keys():
                anatomical_landmask_dict[k] = [zoffset - anatomical_landmask_dict[k][2], anatomical_landmask_dict[k][0],
                                           anatomical_landmask_dict[k][1]]

        probe_dict['Anatomical Landmarks'] = anatomical_landmask_dict

    write_probej(probe_dict, outfilename)



