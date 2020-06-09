import sys
import h5py
import numpy as np
from model_prof_tools import check_model, read_model


def convert_model_to_hdf5(filename, outpath):

    filetype, nx, ny, nz = check_model(filename)

    if filetype == 'hdf5':
        return
    
    depth_keywords = [
        'z', 'tau', 'temperature',
        'gas_pressure', 'density',
        'electron_pressure', 'velocity_z',
        'velocity_turbulent', 'B_z', 'B_x',
        'B_y', 'B_local_x', 'B_local_y', 'B_local_z',
        'velocity_local_x', 'velocity_local_y',
        'velocity_local_z', 'hydrogen_populations',
        'nHminus', 'nHplus', 'nH2', 'nH2plus'
    ]
    non_depth_keywords = [
        'velocity_macroturbulent', 'straylight_fraction',
        'expansion', 'keep_electron_pressure',
        'keep_gas_pressure', 'keep_density',
        'keep_hydrogen_populations',
        'keep_nHminus', 'keep_nHplus', 'keep_nH2',
        'keep_nH2plus'
    ]

    arr_dict = {}

    

    for keyword in depth_keywords:
        arr_dict[keyword] = np.zeros(shape=(nx, ny, nz), dtype=np.float64)
    
    for keyword in non_depth_keywords:
        arr_dict[keyword] = 0.
    
    for i in np.arange(nx):
        for j in np.arange(ny):
            index = 0
            model = read_model(filename, filetype, nx, ny, nz, i, j)
            for keyword in depth_keywords:
                arr_dict[keyword][i][j] = model[index:index+nz]
                index += nz

    f = h5py.File(outpath, 'w')
    for keyword in depth_keywords:
        f[keyword] = arr_dict[keyword]
    for keyword in non_depth_keywords:
        f[keyword] = arr_dict[keyword]
    f.close()


if __name__ == '__main__':
    if not len(sys.argv) >= 3:
        sys.stdout.write('Usage: python convert_to_hdf5.py <filepath> <outfilepath>\n')
        sys.stdout.write('Example:\n')
        sys.stdout.write('python convert_to_hdf5.py __inputmod.bin __inputmod.h5\n')
        sys.exit(1)
    filename = sys.argv[1]
    outpath = sys.argv[2]
    convert_model_to_hdf5(filename, outpath)