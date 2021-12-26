# Wiktionary's English borrowings in the worlds languages

## Content

- dfs and dfs2 together contain 1403 csv-files of 125MB size in total. File names are languages as they appear on the English Wiktionary. Each file consist of 4 columns: 'L2_orth' representing the orthographical form of the word, 'L2_ipa' its IPA-transcription, 'L2_gloss' its English explanation and L2_etym the English word it originates from
- lgs contains text-files with wordlists for every language that appears on the English Wiktionary. Files were created with WiktionaryParser.java.
- WiktionaryParser.java is a courtesy of [Tomasz Jastrząb](https://scholar.google.com/citations?user=p2EcxaMAAAAJ&hl=pl) and was used to retrieve the wordlists found in the folder lgs 
- lglist.txt is a [complete list of languages that appear on the English Wiktioanry](https://en.wiktionary.org/wiki/Wiktionary:List_of_languages).
- lglist_full.txt is a copy of lglist.txt - since the latter serves as input for makedfs.py it can be modified according to one's needs without losing the full list.
- LICENSE: MIT
- makedfs.ipynb - The Parser with which the dfs were obtained from Wiktionary and assembled as data frames as an i-python-notebook.
- makedfs.py - The same parser as makedfs.ipynb but as a .py file that can be run from the commandline by cd-ing into the right folder and running ```makedfs.py```
With a download speed of 144Mbps the script needed 58 hours to parse all the languages from aari until zuni.
- parser.log - There are a few bugs that are smoothened out during parsing that are documented here.

# remarks
- Sometimes the column "L2_etym" is not displayed by the csv-viewer in Github. This is likely the case whenever the first 100 lines of the column are empty. Clicking on "raw" the column can be seen again.

# Todo
- convert raw data to cldf
- add missing IPA transcriptions using [epitran](https://pypi.org/project/epitran/), [copius_api](https://github.com/martino-vic/copius_api) and potential other software
- Try to add those new IPA transcriptions to Wiktionary