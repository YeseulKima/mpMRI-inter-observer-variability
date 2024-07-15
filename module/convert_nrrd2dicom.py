import SimpleITK as sitk
import pydicom
import argparse
import os

def convert_nrrd_to_dicom(nrrd_file, dicom_dir):
    # Read the NRRD file
    image = sitk.ReadImage(nrrd_file)
    
    # Convert to Numpy array
    image_array = sitk.GetArrayFromImage(image)
    
    # Normalize the image array
    image_array = sitk.Cast(image, sitk.sitkInt16)
    
    # Convert to SimpleITK image
    dicom_image = sitk.GetImageFromArray(image_array)
    
    # Create output directory if it does not exist
    if not os.path.exists(dicom_dir):
        os.makedirs(dicom_dir)
    
    # Write the DICOM series
    writer = sitk.ImageFileWriter()
    writer.SetImageIO("GDCMImageIO")
    
    series_tag_values = {
        "0010|0010": "PatientName",
        "0020|000D": "StudyInstanceUID",
        "0020|000E": "SeriesInstanceUID",
        "0008|0060": "Modality"
    }
    
    # Set DICOM tags
    for tag, value in series_tag_values.items():
        dicom_image.SetMetaData(tag, value)
    
    # Write each slice as a separate DICOM file
    for i in range(dicom_image.GetDepth()):
        slice_ = dicom_image[:, :, i]
        writer.SetFileName(os.path.join(dicom_dir, f"slice_{i:03d}.dcm"))
        writer.Execute(slice_)
    
    print(f'NRRD file {nrrd_file} has been converted to DICOM series in directory {dicom_dir}')

def main():
    parser = argparse.ArgumentParser(description="Convert NRRD file to DICOM format")
    parser.add_argument('--input', type=str, required=True, help='Path to the input NRRD file')
    parser.add_argument('--output', type=str, required=True, help='Directory to save the output DICOM files')
    args = parser.parse_args()

    convert_nrrd_to_dicom(args.input, args.output)

if __name__ == "__main__":
    main()
