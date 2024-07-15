import SimpleITK as sitk
import nibabel as nib
import numpy as np
import argparse
import os

def convert_nrrd_to_nifti(nrrd_file, nifti_file):
    # Read the NRRD file
    image = sitk.ReadImage(nrrd_file)
    
    # Convert to Numpy array
    image_array = sitk.GetArrayFromImage(image)
    
    # Create a NIfTI image
    nifti_image = nib.Nifti1Image(image_array, np.eye(4))
    
    # Save the NIfTI image
    nib.save(nifti_image, nifti_file)
    print(f'NRRD file {nrrd_file} has been converted to NIfTI file {nifti_file}')

def main():
    parser = argparse.ArgumentParser(description="Convert NRRD file to NIfTI format")
    parser.add_argument('--input', type=str, required=True, help='Path to the input NRRD file')
    parser.add_argument('--output', type=str, required=True, help='Path to the output NIfTI file')
    args = parser.parse_args()

    convert_nrrd_to_nifti(args.input, args.output)

if __name__ == "__main__":
    main()
