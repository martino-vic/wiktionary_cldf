[![CLDF validation](https://raw.githubusercontent.com/martino-vic/en_borrowings/master/cldf/badge.svg)](https://github.com/martino-vic/en_borrowings/blob/master/cldf/dfs2cldf.py#L53) [![DOI](https://zenodo.org/badge/441361769.svg)](https://zenodo.org/badge/latestdoi/441361769)

# Wiktionary as CLDF

## Content

- cldf1 and cldf2 contain [cldf](https://cldf.clld.org/)-conform data sets with a total of 2 377 756 entries about the vocabulary of all 1403 languages of the English Wiktionary.
- raw1 and raw2 together contain 1403 csv-files of 125MB size in total. File names are languages as they appear on the English Wiktionary. Each file consist of 4 columns: 'L2_orth' representing the orthographical form of the word, 'L2_ipa' its IPA-transcription, 'L2_gloss' its English explanation and 'L2_etym' its etymology iff it is borrowed from English
- lgs contains text-files with wordlists for every language that appears on the English Wiktionary. Files were created with WiktionaryParser.java.
- WiktionaryParser.java is a courtesy of [Tomasz Jastrząb](https://scholar.google.com/citations?user=p2EcxaMAAAAJ&hl=pl) and was used to retrieve the wordlists found in the folder lgs 
- lglist.txt is a [complete list of languages that appear on the English Wiktioanry](https://en.wiktionary.org/wiki/Wiktionary:List_of_languages).
- lglist_full.txt is a copy of lglist.txt - since the latter serves as input for makedfs.py it can be modified according to one's needs without losing the full list.
- LICENSE: MIT
- makedfs.py - The parser with which the csv files where obtained. With a download speed of 144Mbps it needed 58 hours to parse all the languages from aari until zuni.
- makedfs.ipynb - Some notes, documenting the making-of of the parser
- parser.log - Documenting corrupted file names and handling of errors that occured while squeezing parsed data into data frames
- dfs is an empty folder into which the parser writes its results. Generated outputs were migrated to raw1 and raw2 due to Git's limitation of maximum 1000 files per directory
- changelog.txt - documenting manual deletion of false positive and insertion of false negative English loanwords
- cldf is an empty folder to which ```dfs2cldf.py``` writes it output. Generated output had to be migrated to folders cldf1 and cldf2 due to Github's limit of 1000 files per directory

# remarks
- Sometimes the column "L2_etym" is not displayed by the csv-viewer in Github. This is likely the case whenever the first 100 lines of the column are empty. Clicking on "raw", the column can be seen again.
- The reason why columns have the "L2_" prefix is that this data was first used for baseline tests, where they served as pseudo-donor words (hence "L2" ~ second language ~ donor language), even though
in the current setting they represent the recipient language (L1). The distinction L1-L2 is only internal.

# Todo
- add missing IPA transcriptions using [epitran](https://pypi.org/project/epitran/), [copius_api](https://github.com/martino-vic/copius_api), [espeak-ng](https://github.com/espeak-ng/espeak-ng) and potential other software
- Try to contribute those new IPA transcriptions to Wiktionary