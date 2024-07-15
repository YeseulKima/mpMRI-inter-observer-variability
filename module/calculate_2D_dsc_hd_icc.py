import numpy as np
from scipy.spatial.distance import directed_hausdorff
from skimage import measure
import statsmodels.api as sm

# 샘플 2D 영역 생성 (예: 3개의 이진 이미지)
region1 = np.array([[0, 0, 0, 1, 1, 0, 0],
                    [0, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 0],
                    [0, 0, 1, 1, 1, 0, 0]])

region2 = np.array([[0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 0],
                    [0, 0, 1, 1, 0, 0, 0]])

region3 = np.array([[0, 0, 0, 1, 1, 0, 0],
                    [0, 1, 1, 1, 1, 1, 0],
                    [0, 1, 0, 1, 1, 1, 0],
                    [0, 0, 0, 1, 1, 0, 0]])

regions = [region1, region2, region3]

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

# 각 영역 사이의 지표 계산
for i in range(len(regions)):
    for j in range(i + 1, len(regions)):
        dsc = dice_coefficient(regions[i], regions[j])
        hd = hausdorff_distance(regions[i], regions[j])
        print(f'Region {i + 1} vs Region {j + 1} - DSC: {dsc:.4f}, Hausdorff Distance: {hd:.4f}')

# ICC 계산 (여기서는 각 영역의 픽셀 값을 관찰값으로 사용)
icc_value = icc([region1.flatten(), region2.flatten(), region3.flatten()])
print(f'ICC: {icc_value:.4f}')
