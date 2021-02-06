import pandas as pd

def stratify_data():
    # Reads from AudioMoth_Data.csv.
    df = pd.read_csv('AudioMoth_Data.csv', dtype={'AudioMothID' : str, 'Duration' : float, 'StartDateTime' : str, 'Artist' : str, 'Comment' : str})
    # Removes audio clips that are not a minute in length.
    df.drop(df[~((df.Duration <= 60.5) & (df.Duration >= 59.5))].index, inplace=True)
    failed_audiomoths = ["AM-18", "AM-19", "AM-21", "AM-28"]
    # Removes audio clips from failed audiomoths.
    df.drop(df[df.AudioMothCode.isin(failed_audiomoths)].index, inplace=True)
    df = df.reset_index(drop=True)
    # Splits data into groups based on audiomoth and recorded hour. Selects one random audio clip from each group.
    df = df.groupby(["AudioMothCode", lambda index : df.loc[index, "Comment"][12:14]]).apply(lambda grp : grp.sample())
    # Write stratified data into Stratified_Data.csv
    df.to_csv('Stratified_Data.csv', index=False)

stratify_data()