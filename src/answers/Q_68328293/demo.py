import pandas as pd

def dummydata():
    return pd.DataFrame(
        [
            '19:05',
            '20:18',
            '20:44',
            '20:51',
            '06:11',
            '06:23',
            '08:37',
            '11:59',
            '02:22',
            '23:58',
            '23:18',
            '03:35',
        ],
        columns=['Time'],
    )

def prepare_data(df: pd.DataFrame,
                 time_column: str = 'Time',
                 day_time_start: int = 7,
                 day_time_end: int = 23,
                 prune: bool = True):
    """Returns processed data (as a dataframe) for a given time-column."""

    _df2 = (df[time_column]
                .str.split(':', expand=True)
                .rename(columns={0: 'HH', 1: 'MM'})
                .astype(int))
    dfx = pd.concat([df[time_column], _df2], axis=1)
    dfx['Hour'] = dfx.HH + dfx.MM.between(30, 59)
    dfx['Hour'] = dfx.Hour + (dfx.Hour // 24) * (-24)
    dfx['AdjustedTime'] = dfx.Hour.astype(str).apply(lambda x: x.zfill(2)) + ':00'
    dfx['DayOrNight'] = (dfx.Hour
                         .between(day_time_start, day_time_end)
                         .apply(lambda x: 'Day' if x else 'Night'))
    if prune:
        return dfx.loc[:, [time_column, 'AdjustedTime', 'DayOrNight']]
    return dfx

if __name__ == "__main__":
    df = dummydata()
    dfx = prepare_data(df, time_column='Time')
    print(dfx.to_markdown())

    ## Output
    # |    | Time   | AdjustedTime   | DayOrNight   |
    # |---:|:-------|:---------------|:-------------|
    # |  0 | 19:05  | 19:00          | Day          |
    # |  1 | 20:18  | 20:00          | Day          |
    # |  2 | 20:44  | 21:00          | Day          |
    # |  3 | 20:51  | 21:00          | Day          |
    # |  4 | 06:11  | 06:00          | Night        |
    # |  5 | 06:23  | 06:00          | Night        |
    # |  6 | 08:37  | 09:00          | Day          |
    # |  7 | 11:59  | 12:00          | Day          |
    # |  8 | 02:22  | 02:00          | Night        |
    # |  9 | 23:58  | 00:00          | Night        |
    # | 10 | 23:18  | 23:00          | Day          |
    # | 11 | 03:35  | 04:00          | Night        |