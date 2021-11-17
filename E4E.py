import sys
import pandas as pd


def stratify(path):
    df = pd.read_csv(path)

    # Drop rows with no start date
    df = df.dropna(subset=["StartDateTime"])

    # Drop rows with file size less than required limit
    df = df.drop(df[df["FileSize"] < 46080000].index)

    df["StartDateTime"] = pd.to_datetime((df["StartDateTime"]))
    codes = df["AudioMothCode"].unique()

    # First Strata
    first_strata = []
    for code in codes:
        samples = df[df["AudioMothCode"] == code]["StartDateTime"].reset_index(drop=True)
        initial = samples[0]
        count = 0
        for i in range(1, len(samples)):
            difference = abs(samples[i] - initial)
            if difference.seconds >= 3600:
                count += 1
                initial = samples[i]
        if count > 24:
            first_strata.append(code)

    df2 = pd.DataFrame(columns=df.columns)
    df3 = pd.DataFrame(columns=df.columns)

    # Second Strata
    for code in first_strata:
        samples = df[df["AudioMothCode"] == code]
        df2 = pd.DataFrame(columns=df.columns)

        randsample = samples.sample()
        randsample.reset_index(drop=True, inplace=True)
        df2 = df2.append(randsample, ignore_index=True)

        count = 1
        while count != 24:
            randsample = samples.sample()
            randsample.reset_index(drop=True, inplace=True)
            flag = 0
            for i in range(0, len(df2)):
                x = df2["StartDateTime"][i]
                y = randsample["StartDateTime"][0]
                difference = (x - y)
                if difference.seconds <= 3600:
                    flag = 1
                    break
            if flag == 0:
                df2 = df2.append(randsample).reset_index(drop=True)
                count += 1
        df2 = df2.sort_values(by=["StartDateTime"], ignore_index=True)
        df3 = df3.append(df2)

    df3.to_csv("stratified.csv")
    return len(df3) == len(first_strata) * 24

if __name__ == "__main__":
    path = input("Enter Path of Input File")
    print(stratify(path))