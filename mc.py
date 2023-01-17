import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


maps = [['S348', 'S356', 'S143'],
       ['S229', 'S361'],
       ['S282', 'S329', 'S275', 'S114', 'S208', 'S352', 'S007', 'S189', 'S005', 'S123', 'S266', 'S273']]

if __name__ == '__main__':
    convertes = np.loadtxt('3converters.txt', delimiter='\t', encoding='utf-8')
    print(len(convertes))
    suppliers = pd.read_csv('3.csv', header=0, index_col=0)
    print(len(suppliers))

    mc_times = 100
    means = []
    stds = []
    for i in range(mc_times):
        weeks = []
        materials = []
        for week, converter in enumerate(convertes):
            material = 0
            for i, supplier_group in enumerate(maps):
                for supplier in supplier_group:
                    lower = suppliers.loc[supplier, 'lower']
                    upper = suppliers.loc[supplier, 'upper']
                    ratio = suppliers.loc[supplier, 'ratio']
                    capacity = np.random.uniform(lower, upper)
                    material += capacity / ratio * (1 - converter[i] / 100)
            weeks.append(week + 1)
            materials.append(material)
        
        print(weeks, materials)
        
        # fig = plt.figure(figsize=(8, 4))
        # plt.plot(weeks, materials)
        # plt.plot(weeks, [28200] * 24)
        # plt.xlabel('week')
        # plt.ylabel('capacity')
        # plt.ylim([26000, 29000])
        # plt.xticks(range(1, 25, 2))
        # plt.legend(['supply capacity', 'demand capacity'])
        # plt.show()

        mean = np.mean(materials)
        std = np.std(materials)
        print(mean, std)

        means.append(mean)
        stds.append(std)
    
    print(means, stds)
    df = pd.DataFrame(columns=['mean', 'std'])
    df['mean'] = means
    df['std'] = stds
    print(df)
    df.to_csv('mc.txt', index=False, sep='\t')