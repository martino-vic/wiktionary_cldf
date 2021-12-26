# version 0.1.
# disambiguate homographs of differnet lgs,
# homonyms within the same lg
# overall more precise scraping
# remove col "links" - takes up too much space on disk.

import argparse
import ast
import concurrent.futures
import logging
import os
import re
import shutil

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from requests import get
from tqdm import tqdm

logging.basicConfig(filename='parser.log',
                    encoding='utf-8', level=logging.WARNING)
parser = argparse.ArgumentParser(description="No arguments needed to specify. \
This parser looks at the languages in lglist.txt and scrapes them one by \
one from Wiktionary. Proto and ancient languages will be skipped for now \
and the solution goes to the folder dfs. There's a copy of lglist.txt named \
lglist_full.txt so that you can tinker around and specify which languages to \
parse in lglist.txt without data loss. Enjoy. License: MIT")
parser.parse_args()


class Scrape():

    def __init__(self):
        self.maxthreads = 100
        self.gloss = []
        self.ipa = []
        self.etym = []
        self.l1 = ""

    def download_url(self, url):
        html = get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        word = url.rsplit('/', 1)[1]
        gloss = []
        ipa = []
        etym = []
        addcut = 0
        ety = ""
        theipa = ""

        for h2 in soup.find_all("h2"):  # Language headers e.g. "Hawaiian", etc
            h2L1 = h2.find("span", {"id": self.l1})  # find target lg's header
            if h2L1:
                for sib in h2L1.parent.next_siblings:  # loop thr all siblings
                    # ("next sibling doesnt work")
                    if sib.name == 'h2':  # dont look for siblings beyond...
                        break  # ...the next header (= the next language)

                    if sib.name == "h3":

                        if "Pronunciation" in sib.text:
                            # pro = sib.find_next_sibling("ul")
                            for pro in sib.next_siblings:
                                if len(ipa) == 1:
                                    break
                                if pro.name == "ul":
                                    for li in pro.find_all("li"):
                                        theipa = li.find("span",
                                                         {"class": "IPA"})
                                        if theipa:
                                            ipa.append(theipa.text)
                                            break

                                elif pro.name == "h2":
                                    ipa.append("")
                                    break

                        if "Etymology" in sib.text:
                            # glo = sib.find_next_sibling("ol")
                            # if glo:
                            for glo in sib.next_siblings:

                                if glo.name == "p":
                                    if "English" in glo.text:
                                        # some etymons occure twice, make sure
                                        # to grab the one that is an English LW
                                        try:
                                            ety = glo.i.text
                                        except:
                                            pass

                                elif glo.name == "ol":
                                    try:
                                        glo = re.sub(r"\n", ", ", glo.text)
                                        addcut = glo[50:].find(" ")
                                        if addcut == -1:
                                            gloss.append(glo)
                                            etym.append(ety)
                                        else:
                                            gloss.append(glo[:50+addcut])
                                            etym.append(ety)
                                    except AttributeError:
                                        gloss.append("")
                                        etym.append(ety)
                                elif glo.name == "h2":
                                    break
                if ipa == []:
                    ipa = [""]

                if gloss == []:
                    for sib in h2L1.parent.next_siblings:
                        # loop thr all siblings ("next sibling doesnt work")
                        if sib.name == "h2":
                            break
                        if sib.name == "ol":
                            gloss.append(sib.li.text)
                            etym.append(ety)
                if gloss == []:
                    # if word == "hana":
                    # print("yup, entered this weird spot here")
                    gloss = [""]
                    etym = [""]

                ipa = ipa*len(gloss)
                self.gloss.append((gloss, word))
                self.ipa.append((ipa, word))
                self.etym.append((etym, word))

    def download_info(self, lg, url_list):
        threads = min(self.maxthreads, len(url_list))
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
            ex.map(self.download_url, url_list)

    def main(self, lg, url_list):
        self.download_info(lg, url_list)


def main(lglist):
    scr = Scrape()
    if not os.path.isdir(os.path.join(os.getcwd(), "dfs")):
        os.mkdir("dfs")
    if not os.path.isdir(os.path.join(os.getcwd(), "lgs", "empty_lists")):
        os.mkdir(os.path.join(os.getcwd(), "lgs", "empty_lists"))
    if not os.path.isdir(os.path.join(os.getcwd(), "lgs", "proto_lgs")):
        os.mkdir(os.path.join(os.getcwd(), "lgs", "proto_lgs"))

    lglist = [i for i in lglist if i != "English"]  # just in case

    for lg in lglist:
        scr.ipa = []
        scr.gloss = []
        scr.etym = []
        scr.l1 = re.sub(" ", "_", lg)
        lg = scr.l1.lower()
        print(lg)
        file = f"lgs\\{lg}.txt"

        if "proto" in lg or "ancient" in lg:
            shutil.move(file, f"lgs\\proto_lgs\\{lg}.txt")
            continue

        try:
            dflg = pd.read_csv(file, header=None, sep="\n")
        except pd.errors.EmptyDataError:
            shutil.move(file, f"lgs\\empty_lists\\{lg}.txt")
            continue
        except FileNotFoundError:
            logging.warning(f'{file} was not found')
            continue

        dflg.columns = ["L2_orth"]
        dflg["L2_orth"] = [str(i) for i in dflg["L2_orth"]]
        dflg = dflg[~dflg["L2_orth"].str.contains(lg)].reset_index(drop=True)
        dflg = dflg.replace(r'^\s*$', np.nan, regex=True).dropna()
        url_list = [re.sub(" ", "_", f"https://en.wiktionary.org/wiki/{i}")
                    for i in dflg["L2_orth"]]
        scr.main(lg, url_list)

        dfipa = pd.DataFrame(scr.ipa, columns=['L2_ipa', 'L2_orth'])
        dfgloss = pd.DataFrame(scr.gloss, columns=['L2_gloss', 'L2_orth'])
        dfetym = pd.DataFrame(scr.etym, columns=['L2_etym', 'L2_orth'])

        dflg = dflg.merge(dfipa, left_on='L2_orth', right_on='L2_orth')
        dflg = dflg.merge(dfgloss, left_on='L2_orth', right_on='L2_orth')
        dflg = dflg.merge(dfetym, left_on='L2_orth', right_on='L2_orth')

        try:  # usually this works, but sometimes there are 5-20 wrong rows
            dflg = dflg.explode(["L2_ipa", "L2_gloss", "L2_etym"])
        except ValueError:  # pad wrong lengths
            ip, gl, et = [], [], []
            for nr, (i, g, e) in enumerate(zip(dflg.L2_ipa,
                                               dflg.L2_gloss, dflg.L2_etym)):
                if len(i) == len(g) and len(g) == len(e):
                    ip.append(i)
                    gl.append(g)
                    et.append(e)
                else:
                    padi = [i[0]]+[""]*(len(g)-1)
                    pade = [e[0]]+[""]*(len(g)-1)
                    ip.append(padi)
                    gl.append(g)
                    et.append(pade)
                    logging.warning(f'different len in {lg}.txt for gloss {g} \
in row {nr}. Turned {i} to {padi} and {e} to {pade}')

            dflg["L2_ipa"], dflg["L2_gloss"], dflg["L2_etym"] = ip, gl, et
            dflg = dflg.explode(["L2_ipa", "L2_gloss", "L2_etym"])

        dflg.to_csv(f"dfs\\{lg}.csv", encoding="utf-8", index=False)

if __name__ == "__main__":
    with open('lglist.txt', 'r', encoding="utf-8") as f:
        lglist = ast.literal_eval(f.read())
        main(lglist)
