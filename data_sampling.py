import pandas as pd

def stratify_data():
    df = pd.read_csv('AudioMoth_Data.csv', dtype={'AudioMothID' : str, 'Duration' : float, 'StartDateTime' : str, 'Artist' : str}, parse_dates=['StartDateTime'])
    df.drop(df[~((df.Duration <= 60.5) & (df.Duration >= 59.5))].index, inplace=True)
    failed_audiomoths = ["AM-18", "AM-19", "AM-21", "AM-28"]
    df.drop(df[df.AudioMothCode.isin(failed_audiomoths)].index, inplace=True)
    df = df.reset_index(drop=True)
    df = df.groupby(["AudioMothCode", lambda index : df.loc[index, "StartDateTime"].hour]).apply(lambda grp : grp.sample())
    df.to_csv('Stratified_Data.csv', index=False)

stratify_data()