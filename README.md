python-data-files-anonymizer
============================

Replace sensitive identification information in a group of CSV and Excel files with a random list of unique identifiers.

Intended to run using Portable Python (currently testing with 2.7.5.1).  Ideally, run everything on an encrypted USB stick, including Portable Python (plus a few extra packages, so far xlrd, openpyxl, xlsxwriter, xlutils and xlwt; may add R later if needed but may be able to get by with pandas/numpy) for Windows users; other OSes are more likely to have their own Python distribution (though additional packages may be needed).  A simple workflow for end users across platforms is important.

Each project has a few standard directories including one for raw data (which contains sensitive identifiers).  Raw data is processed and a parallel output directory ends up with the same files all matched up with some alternate project-specific identification scheme. These can be downloaded, put in a database, etc. but no longer have the identifying information.  Note that, depending on what data is left over (particularly combinations of demographic information) this is not a guarantee of anonymity.  Adding new raw data would produce new processed files with the same identifier scheme, so could be matched up with existing work in subsequent analysis. To achieve this, likely want all relevant raw data in same specific directory.

May require metadata file describing the ID columns, may attempt some sort of check on whether formulas are in use and how unique the column is (e.g. how similar is a unique count compared to total number of entries).  Categorize columns as ID, demographic; can estimate identifiably from demographic info; e.g. Look for smallest unique sets.

For each file, column names are grabbed, and each is categorized as needing conversion, drop or keep as-is.  Produces a key/dictionary in another file that is the translation from the raw to the processed form.

A master list will be generated and is to remain in a directory alongside with the raw data in a secure location.  Since the new identifiers are not derived from the old ones, this list would be the only way to convert back to the original identifiers.

For files and worksheets within Excel workbooks that are not read easily into pandas DataFrames (containing formulas or are not table-shaped), the system will direct copy with a warning.
