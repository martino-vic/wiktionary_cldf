"""convert csv-files to cldf and validate"""

import pandas as pd
import os
import json
import subprocess
import logging
import ast

logging.basicConfig(filename='cldf.log',
                    encoding='utf-8', level=logging.WARNING)


class Csv2cldf:
    """in: path to file, out: written cldf files"""

    def __init__(self, folder: "'raw1' or 'raw2'", lang: str) -> None:
        """initiate variables that are used by the class methods"""

        glotto = "https://raw.githubusercontent.com/glottolog/glottolog-cldf"
        self.dfglotto = pd.read_csv(f"{glotto}/master/cldf/languages.csv")
        self.dfe = self.dfglotto[self.dfglotto["Name"] == "English"]\
            .assign(Language_ID=0)
        self.lg = lang.lower()
        self.rp = "https://raw.githubusercontent.com/martino-vic/en_borrowings"
        self.rpblob = "https://github.com/martino-vic/en_borrowings/blob"
        self.path = f"{self.rp}/master/{folder}/{self.lg}.csv"
        self.meta = os.path.join(os.getcwd(), self.lg, "metadata.json")

    def main(self) -> None:
        """
        create and write forms.csv, borrowings.csv, \
        languages.csv, metadata.json, readme.md and validate.
        """

        self.metadata(self.forms(), self.borrowings())
        self.lgs()
        self.readme()

    def readme(self) -> None:
        """
        Validate metadata.json. If validation passes write readme.md, \
        else write error message to logfile cldf.log
        """

        rdm = os.path.join(os.getcwd(), self.lg, "readme.md")
        try:  # check pycldf's documentation. write readme if validation passes
            subprocess.run(f"cldf validate {self.meta}").check_returncode()
            with open(rdm, 'w') as f:  # convert to readme
                badge = "[![CLDF validation]"
                badge += f"({self.rp}/master/cldf/badge.svg)]"
                badge += f"({self.rpblob}/master/cldf/dfs2cldf.py#L47)\n\n"
                print(badge)
                f.write(badge + subprocess.run(f"cldf markdown {self.meta}",
                        capture_output=True).stdout.decode("utf-8")
                        .replace("\r\n", "\n"))
        except subprocess.CalledProcessError:  # else write error to logfile
            logging.warning(subprocess.run(f"cldf validate {self.meta}",
                            capture_output=True).stdout.decode("utf-8")
                            .replace("\r\n", "\n"))

    def lgs(self) -> None:
        """generate and write languages.csv"""

        dfelocal = self.dfe
        dflg = self.dfglotto[self.dfglotto["Name"] == self.lg]
        if dflg.empty:
            dfelocal = dfelocal.append(
                pd.DataFrame([["", self.lg.capitalize()] +
                              [""]*(len(self.dfe.columns)-3) + [1]],
                             columns=self.dfe.columns))
        else:
            dfelocal = dfelocal.append(dflg.assign(Language_ID=1))

        languages = os.path.join(os.getcwd(), self.lg, "languages.csv")
        dfelocal.to_csv(languages, encoding="utf-8", index=False)

    def metadata(self, lenform: int, lenborr: int) -> None:
        """write metadata.json by inserting missing data into template"""

        with open("metadata_template.json") as json_data:
            data = json.load(json_data)

        data['dc:title'] = data['dc:title'] + self.lg.capitalize()
        data['rdf:ID'] = data['rdf:ID'] + self.lg
        data['tables'][0]['dc:extent'] = lenform
        data['tables'][2]['dc:extent'] = lenborr

        with open(self.meta, "w") as j:
            json.dump(data, j)

    def forms(self) -> int:
        """Generate and write forms.csv"""

        dfm = pd.read_csv(self.path).rename(
            columns={"L2_orth": "Form", "L2_ipa": "IPA", "L2_gloss": "Gloss"})
        dfm["_1"] = ["" if isinstance(i, str) else i for i in dfm["L2_etym"]]
        dfm["_2"] = dfm["_1"]  # two dummy cols for the loop

        dfforms = pd.DataFrame()  # this will be the output
        for form, donor in zip(["Form", "IPA", "Gloss"],
                               ["L2_etym", "_1", "_2"]):
            dfforms[form] = list(dfm[form]) + [i for i in dfm[donor]
                                               if isinstance(i, str)]
        dfforms["Language_ID"] = ["0"]*len(list(dfm[donor]))\
            + ["1" for i in dfm[donor] if isinstance(i, str)]
        dfforms.insert(0, "ID", dfforms.index)

        try:
            os.mkdir(self.lg)
        except FileExistsError:
            pass
        fms = os.path.join(os.getcwd(), self.lg, "forms.csv")
        dfforms.to_csv(fms, encoding="utf-8", index=False)

        return len(dfforms)

    def borrowings(self) -> int:
        """Generate and write borrowings.csv"""

        dfm = pd.read_csv(self.path)
        dfm["ID"] = dfm.index

        dfborr = pd.DataFrame()
        dfborr["Target_Form_ID"] = [i for i, j in zip(dfm.ID, dfm.L2_etym)
                                    if isinstance(j, str)]
        dfborr["Source_Form_ID"] = [i for i in range(len(dfm),
                                                     len(dfm)+len(dfborr))]
        dfborr.insert(0, "ID", dfborr.index)

        brr = os.path.join(os.getcwd(), self.lg, "borrowings.csv")
        dfborr.to_csv(brr, encoding="utf-8", index=False)

        return len(dfborr)


def loop():
    lglist = os.path.join(os.path.dirname(os.getcwd()), "lglist.txt")
    ast.literal_eval(open(lglist, encoding="utf-8").read())
    for lang, _ in zip(lglist, range(1000)):
        try:
            Csv2cldf(lang)
        except:
            pass

if __name__ == "__main__":
    Csv2cldf("raw1", "Greenlandic").main()
