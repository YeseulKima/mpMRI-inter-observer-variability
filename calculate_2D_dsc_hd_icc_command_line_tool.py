import numpy as np
from scipy.spatial.distance import directed_hausdorff
from skimage import measure
import statsmodels.api as sm
import argparse
import os


# Dice Similarity Coefficient (DSC)
def dice_coefficient(region_a, region_b):
    intersection = np.sum(region_a * region_b)
    return 2.0 * intersection / (np.sum(region_a) + np.sum(region_b))


# Hausdorff Distance
def hausdorff_distance(region_a, region_b):
    a_coords = np.argwhere(region_a)
    b_coords = np.argwhere(region_b)
    return max(directed_hausdorff(a_coords, b_coords)[0], directed_hausdorff(b_coords, a_coords)[0])


# Intraclass Correlation Coefficient (ICC)
def icc(data):
    data = np.asarray(data)
    mean_raters = np.mean(data, axis=1)
    mean_targets = np.mean(data, axis=0)
    mean_total = np.mean(data)
    msr = np.sum((mean_raters - mean_total) ** 2) * data.shape[1]
    msw = np.sum((data - mean_raters[:, None] - mean_targets[None, :] + mean_total) ** 2) / (data.shape[0] - 1)
    msb = np.sum((mean_targets - mean_total) ** 2) * data.shape[0]
    return (msr - msw) / (msr + (data.shape[1] - 1) * msw)


# Load 2D region data from file
def load_region(file_path):
    return np.load(file_path)


# Save results to file
def save_results(output_dir, results):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for key, value in results.items():
        with open(os.path.join(output_dir, f'{key}.txt'), 'w') as f:
            f.write(f'{value:.4f}\n')


def main(args):
    region1 = load_region(args.region1)
    region2 = load_region(args.region2)
    region3 = load_region(args.region3)

    regions = [region1, region2, region3]
    results = {}

    # 각 영역 사이의 지표 계산
    for i in range(len(regions)):
        for j in range(i + 1, len(regions)):
            dsc = dice_coefficient(regions[i], regions[j])
            hd = hausdorff_distance(regions[i], regions[j])
            results[f'Region_{i + 1}_vs_Region_{j + 1}_DSC'] = dsc
            results[f'Region_{i + 1}_vs_Region_{j + 1}_Hausdorff_Distance'] = hd

    # ICC 계산 (여기서는 각 영역의 픽셀 값을 관찰값으로 사용)
    icc_value = icc([region1.flatten(), region2.flatten(), region3.flatten()])
    results['ICC'] = icc_value

    # 결과 저장
    save_results(args.output_dir, results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate DSC, Hausdorff Distance, and ICC for 2D regions.")
    parser.add_argument('--region1', type=str, required=True, help='Path to the first region file (npy format)')
    parser.add_argument('--region2', type=str, required=True, help='Path to the second region file (npy format)')
    parser.add_argument('--region3', type=str, required=True, help='Path to the third region file (npy format)')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save the results')

    args = parser.parse_args()
    main(args)
