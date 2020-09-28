# pip install pandas
import pandas as pd

## define label categories for modularity
categories = {
    'overall': ['android', 'iphone', 'web'], 
    'mobile': ['android', 'iphone'], 
    'rollup': ['overall', 'mobile']  
}

## create a dataframe with input data
## and process for 'overall' and 'mobile'
df = pd.DataFrame(day_value)
df['overall'] = df[categories['overall']].sum(axis=1) > 0
df['mobile'] = df[categories['mobile']].sum(axis=1) > 0

## evaluate totals of all columns in df
total = df.sum(axis=0).astype(int)

## update device_rollup
device_rollup = {'overall': [], 'mobile': []}
for k, v in total[categories['overall']].to_dict().items(): 
    print(k, v)
    if v > 0:
        device_rollup['overall'].append(k)
        if k in categories['mobile']:
            device_rollup['mobile'].append(k) 

## update rollup_l7
rollup_l7 = df[categories['rollup']].sum(axis=0).to_dict()

if __name__ == '__main__':
    ## Data
    day_value = {
        'android': [1,0,0,0,0,0,1],
        'iphone':  [0,1,0,1,0,0,0],
        'web':     [0,1,1,0,1,0,0],
    }
    
    ## Generate output
    s = '\n{}:\n' # common header print-string
    
    # df: dataframe
    print(s.format(df))
    print(df)

    # total
    print(s.format(total))
    print(total.to_dict())

    # device_rollup
    print(s.format(device_rollup))
    print(device_rollup)

    # rollup_l7
    print(s.format(rollup_l7))
    print(rollup_l7)
