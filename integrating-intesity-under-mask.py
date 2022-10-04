#!/usr/bin/env python3
import os
import sys
import h5py as h5
import numpy as np
import subprocess
import re
import argparse
os.nice(0)

MASK_BAD = int('0x0',16)
MASK_GOOD = int('0x1',16)

class CustomFormatter(argparse.RawDescriptionHelpFormatter,
                      argparse.ArgumentDefaultsHelpFormatter):
    pass

def parse_cmdline_args():
    parser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__,
        formatter_class=CustomFormatter)
    parser.add_argument('-f', type=str, help="The file with blocks for binning")
    parser.add_argument('-m', type=str, help="Mask file")
    parser.add_argument('-h5', type=str, help="hdf5 path to data")
    parser.add_argument('-mh5','--mh5', type=str, help="hdf5 path to slab mask data")

    return parser.parse_args()
    
if __name__ == "__main__":
    
    args = parse_cmdline_args()
    files = args.f
    mask_filename = args.m
    mask_h5path = args.mh5
    data_h5path = args.h5
    
    if mask_h5path is None:
        mask_h5path = '/data/data'
    

    output_file = open(os.path.join(os.getcwd(),'intensity.txt'),'w')

    mask = h5.File(mask_filename,'r')[mask_h5path][()]


    bitwise_bad = np.bitwise_and(mask, MASK_BAD) > 0
    bitwise_good = np.bitwise_and(mask, MASK_GOOD) == MASK_GOOD
            
    mask_new = np.logical_or(np.logical_not(bitwise_good) , bitwise_bad)
 
    with open(files, 'r') as f:
        for filename in f:
            file_data = h5.File(filename.strip(),'r')[data_h5path][()]
            for ind in range(len(file_data)):
                tmp = np.where(file_data[ind,]> 65000, 0, file_data[ind,])
                Int = np.where(mask_new == True, tmp, 0)
                intensity = np.sum(Int) #sum range of interest              
                print(intensity)
                if ind == 0:
                    
                    h5NEW = h5.File(os.path.join(os.getcwd(),'to_check.h5'),'w')
                    h5NEW.create_dataset('/data/data', data=Int)
                    h5NEW.close()
    
    
    