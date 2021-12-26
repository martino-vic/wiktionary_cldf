# Wiktionary's English borrowings in the worlds languages

## Content

- dfs and dfs2 together contain 1403 csv-files of 125MB size in total. File names are languages as they appear on the English Wiktionary. Each file consist of 4 columns: 'L2_orth' representing the orthographical form of the word, 'L2_ipa' its IPA-transcription, 'L2_gloss' its English explanation and L2_etym the English word it originates from
- lgs contains text-files with wordlists for every language that appears on the English Wiktionary. These wordlists were obtained with a code written in Java, of which it is not clear yet whether it can be made publicly available, due to copy-right reasons.
- lglist.txt is a complete list of languages that appear on the English Wiktioanry. I don't remember anymore how I obtained it.
- lglist_full.txt is a copy of lglist.txt - since the latter serves as input for makedfs.py and needs to be modified sometimes.
- LICENSE: MIT
- makedfs.ipynb - The Parser with which the dfs were obtained from Wiktionary and assembled as data frames.
- makedfs.py - The same parser but as a .py file. It can be run from the commandline by cd-ing into the right folder and running ```makedfs.py```
With a download speed of 144Mbps the script needed 58 hours to parse all the languages from aari until zuni.
- parser.log - There are a few bugs that are smoothened out during parsing and are documented here.