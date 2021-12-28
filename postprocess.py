import os

import pandas as pd

for file in os.listdir(os.getcwd()):
    print(file)
    if file[-3:] == "csv":
        df = pd.read_csv(file)#.dropna(subset=["L2_orth", "L2_ipa"])
        df["en_ipa"] = ["DELETETHIS" if not isinstance(etym, float) and isinstance(ipa, float) else ipa
                        for etym,ipa in zip(df["L2_etym"], df["en_ipa"])]
        df = df[df["en_ipa"]!="DELETETHIS"]
        
        if len(df) != 0:
            df.to_csv(file, encoding="utf-8", index=False)
        else:
            os.remove(file)