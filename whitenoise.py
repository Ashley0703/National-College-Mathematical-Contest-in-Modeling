import numpy as np
from matplotlib import pyplot as plt
from statsmodels.stats.diagnostic import acorr_ljungbox


# Ljung-Box检验白噪声
if __name__ == '__main__':
    # 读入csv文件，diffs存放残差减去均值的时间序列
    diffs = np.genfromtxt('diff.csv', delimiter=',', encoding='utf-8')
    # 存放各个供应商的白噪声程度
    p_values = []
    for diff in diffs:
        # 2~20阶滞后
        res = acorr_ljungbox(diff, lags=[2, 20], boxpierce=False)
        # 考虑最坏的情况下的白噪声程度
        max_p = max(res[1])
        p_values.append(max_p)

    fig, axes = plt.subplots(2, 1, figsize=(8, 8))

    axes[0].plot(range(1, 403), p_values, color='mediumseagreen')
    axes[0].set_xlabel('Supplier id')
    axes[0].set_ylabel('P-value')
    axes[0].set_title('P-value of supplier')

    p_bins = np.linspace(0, 1, 21)
    axes[1].hist(p_values, p_bins, color='skyblue')
    axes[1].set_xticks(p_bins)
    axes[1].set_xlabel('P-value')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('Frequency of P-value')

    plt.tight_layout()
    plt.show()

    # 保存各个供应商的p值
    np.savetxt('p_values.txt', p_values, fmt='%f')