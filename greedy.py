import numpy as np
import pandas as pd


requirement = 28200
transmit_capacity = 6000
transmiters = 3
capacity_threshold = 318
ratio_map = {'A': 0.6, 'C': 0.72}

def getTransmitPlan(supplier):
    supplier['used'] = [0] * 34
    buckets = []
    ts = []
    cnt = 0
    while cnt < transmiters:
        capacity = 0
        bucket = []
        t = []
        idx = 0
        while capacity < transmit_capacity:
            supplier_capacity = supplier[supplier.used == 0].capacity[idx]
            supplier_t = supplier[supplier.used == 0].type[idx]
            if capacity + supplier_capacity < transmit_capacity:
                capacity += supplier_capacity
                pos = supplier[supplier.capacity == supplier_capacity].index[0]
                supplier.loc[pos, 'used'] = 1
                bucket.append(supplier_capacity)
                t.append(supplier_t)
                if transmit_capacity - capacity < capacity_threshold:
                    buckets.append(bucket)
                    ts.append(t)
                    cnt += 1
                    break
            else:
                idx += 1
                if idx >= len(supplier[supplier.used == 0]):
                    buckets.append(bucket)
                    ts.append(t)
                    cnt += 1
                    break
    return buckets, ts

def getRemaining(buckets, ts, forwarder):
    converted = []
    converters = []
    converter_loss = []
    for bucket, t in zip(buckets, ts):
        c = 0
        for supplier_capacity, supplier_t in zip(bucket, t):
            c += supplier_capacity / ratio_map[supplier_t]
        converted.append(c)

    sums = sorted(converted, reverse=True)
    remainings = []
    for column in forwarder.columns:
        loss = sorted(forwarder[column])
        lowests = [loss[0], loss[1], loss[2]]
        remaining = 0
        converter = []
        for lowest, s in zip(lowests, sums):
            remaining += lowest * s / 100
            converter.append(forwarder[column].where(forwarder[column] == lowest).dropna().index[0])
        converter.append(forwarder[column].where(forwarder[column] == loss[3]).dropna().index[0])
        remaining += requirement - sum(sums)
        remainings.append(remaining)
        converters.append(converter)
        converter_loss.append(loss[3])
    print(remainings)
    print(converters)
    print(converter_loss)
    return remainings, converters, converter_loss

    
if __name__ == '__main__':
    supplier = pd.read_csv('2.csv', header=0, index_col=0)
    buckets, ts = getTransmitPlan(supplier)
    print(supplier)
    print(buckets)
    print(ts)

    forwarder = pd.read_csv('forwarder.csv', header=None, index_col=0)
    remainings, converters, converter_loss = getRemaining(buckets, ts, forwarder)
    np.savetxt('2remainings.txt', remainings, delimiter='\t', fmt='%s', encoding='utf-8')
    np.savetxt('2converters.txt', converters, delimiter='\t', fmt='%s', encoding='utf-8')
    np.savetxt('2converter_loss.txt', converter_loss, delimiter='\t', fmt='%s', encoding='utf-8')
