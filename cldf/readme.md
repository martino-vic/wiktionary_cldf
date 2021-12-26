# Content

- explore the folders to find data for your next project
- ```dfs2cldf.py``` was run from the command line to convert all raw data frames to cldf. Validation happens in line 53:  
```subprocess.run(f"cldf validate {self.meta}").check_returncode()```
- ```metadata_template.json``` serves as a template to create ```metadata.json``` for each language
- If a file doesn't pass the validation, the logger will log the error message to ```cldf.log```
