# Content

- This is the folder to which ```dfs2cldf.py``` writes its output. Generated output was migrated to folders cldf1 and cldf2 since Git allows max. 1000 folders per directory
- ```dfs2cldf.py``` was run from the command line to convert raw data frames to cldf. Validation happens in line 54:  
```subprocess.run(f"cldf validate {self.meta}").check_returncode()```
- ```metadata_template.json``` serves as a template to create ```metadata.json``` for each language
- If a file doesn't pass the validation, the logger will log the error message to ```cldf.log```
- The corresponding URL of each word is ```https://en.wiktionary.org/wiki/WORDFORM```, whereas WORDFORM is the word as it appears in the column 'Form' in ```forms.csv```. If you need to distinguish it from homonyms in other languages ```https://en.wiktionary.org/wiki/WORDFORM#LANGUAGE``` also works, whereas LANGUAGE. An example for a valid URL is ```https://en.wiktionary.org/wiki/loll#Estonian```
- Sometimes the parser misinterprets information and misses out English loanwords or adds false positives. These have to be spotted, fixed and documented manually in the changelog. If you find any, plz open a new issue.