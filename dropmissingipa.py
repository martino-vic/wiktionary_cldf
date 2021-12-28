"""read raw files, ignore files with no English borrowings and missing IPA-transcriptions"""

import os
from functools import cache

from espeakng import ESpeakNG
import pandas as pd
from tqdm import tqdm

from loanpy import helpers

REPO = os.path.dirname(os.getcwd())
hp = helpers.Help()

def en2ipa(df):   
    def no_tiebar_4vow(func, word, ipa):
        def removebar(func, word, ipa):
            #print(word)
            ipaword = func(word.replace("-",""), ipa)
            ipa_cln= []
            for nr, i in enumerate(ipaword):
                if i != chr(865):
                    ipa_cln.append(i)
                elif hp.phon2cv.get(ipaword[nr-1], "") == "V" or hp.phon2cv.get(ipaword[nr+1], "") == "V":
                    continue
                else:
                    ipa_cln.append(i)
            ipa_cln = "".join(ipa_cln)
            return ipa_cln   
        return removebar(func, word, ipa)
    
    @cache
    def g(word, ipa):
        return no_tiebar_4vow(esng.g2p, word, ipa)

    esng = ESpeakNG()
    esng.voice ="en-us"
    ipalist = []
    for word in tqdm(df["L2_etym"]):
        if not isinstance(word, float):
            try:
                ipalist.append(g(word, ipa=2))
            except UnicodeDecodeError:
                print(word)
                ipalist.append(None)
                pass
                
        else:
            ipalist.append(None)
    df["en_ipa"] = ipalist
    return df

for folder in ["raw2", "raw1"]:
    for file in os.listdir(os.path.join(REPO, folder)):
        print(file)
        if os.path.exists(file):
            #print("skip")
            continue
        df = pd.read_csv(f"{REPO}\{folder}\{file}")
        if len(df.dropna(subset=["L2_etym"])) == 0:
            continue
        df = df.dropna(subset=["L2_ipa"])
        if len(df.dropna(subset=["L2_etym"])) == 0:
            continue
        en2ipa(df)
        print(f"writing {file}")
        df.to_csv(file, encoding="utf-8", index=False)
        #check fuckups in encoding
        df = pd.read_csv(file).dropna(subset=["L2_orth", "L2_ipa"])
        df["en_ipa"] = ["DELETETHIS" if not isinstance(etym, float) and isinstance(ipa, float) else ipa
                        for etym,ipa in zip(df["L2_etym"], df["en_ipa"])]
        df = df[df["en_ipa"]!="DELETETHIS"]
        
        if len(df) != 0:
            df.to_csv(file, encoding="utf-8", index=False)
        else:
            os.remove(file)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            