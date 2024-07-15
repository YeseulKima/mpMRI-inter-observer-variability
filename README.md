# mpMRI-inter-observer-variability


## Requirements
Before run the code, install packages from the requirements.txt file. 
- Python >= 3.9
- numpy, scipy, scikit-image, statsmodels


## Description

### 1) Inter-observer variability types
* Dice Similarity Coeffecient (DSC):It measures the overlap between two sets. It is 1 when the two sets are identical and 0 when there is no overlap.
    - Range: 0 (complete mismatch) - 1 (perfect match)
* Hausdorff Distance: The maximum distance between the farthest points of the two sets (a large value close to infinity).
    - Range: 0 (perfect match) - infinity (complete mismatch)
* Intraclass Correlation Coefficient (ICC): It measures the agreement between observers. It is 1 for perfect agreement, 0 for no agreement, and negative values indicate a lack of consistency.
    - Range: [-1, 1] / 0 (complete mismatch) - 1 (perfect match)

  
### 2) Usage
- Input: (More than 2) Contoured mask in nrrd or nifti or dicom format.
- Output: Inter-observer variability values. 


## Paper
For more details, please see our paper (to/be/updated) which has been accepted at XXXX on YYYY. 
If this code is useful for your work, please consider to cite our paper:
```
@inproceedings{
    kimXXXX,
    title={YYYY},
    author={ZZZZ},
    booktitle={AAAA},
    year={BBBB},
    url={CCCC}
}
```

## Authors
  - [YeseulKima](https://github.com/YeseulKima) - **Yeseul Kim** - <YKim23@mdanderson.org>
