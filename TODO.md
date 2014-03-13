# To-Do List for python-data-files-anonymizer

Here is an attempt to list the work needed on this project, and collect ideas for how to accomplish things.

## Major: critical items

### Handling non-data sheets
* Blank sheets are ignored and currently not copied to output files.
* Sheets that would not read into Dataframe would probably cause an error.

### Anonymization routine 
* Column information
    * To obtain Primary ID, ask for number of column or to see column headers, or read from existing metafile.
    * *process_columns* or similar: Either reads from an existing metafile that describes the column names and types, or interactively confirms column types primed with guesses then writes a new metafile.
    * Probably need a metafile for each sheet with this information, needing confirmation when anything changes.  Could have interactive script that asks for which of these to edit/confirm (and always require this for new data files that uses *guess_column_data_type_from_name* for initial guesses)

### Project setup and installation 
* Project setup script: Argument (or interactive) name of project, with confirmation and list of directories created.  Optional: set own seed or use random seed.
    * Create appropriate tree of standard directories for a project.
        * projects
            * project_name
                * rawdata
                * output
                * metafiles
                * reports
        * scripts
    * Creates master ID list file with seed but no actual entries, maybe a placeholder message in case anyone looks at it.
    * maybe confirm that appropriate packages are installed?
* Test installations
    * Windows (using Portable Python)
    * Mac (need reasonable way of ensuring all packages are available)
    * Linux (not aware of any current users; similar to Mac issue but likely less support needed for these people)


## Minor: would be nice to get to these eventually
* Check date of input file; only write if target file is absent, prompt if input file has changed.
* Better column type guessing, perhaps digging into a sample of data (or whole column if ) from the column; could check for uniqueness, names, 8-digit numbers (student IDs at our institution; could make this a setting for wider distribution) to guess if the column is Primary Key, demographic, ID, or data.
* Aggregate data by joining all files (and sheets within files) using the primary ID key.  
    * Probably output as a CSV.  
    * Given as option for users.  
    * Fill in appropriate NA for missing data. 
    * If column names are duplicated, use file/sheet name or prompt for prefix/suffix.
* Data summaries
    * Discover/confirm data type in a column: Some interaction of column type and the data type inside (e.g. numerical, categorical); may be handled by categories confirmed by user. 
    * Figure out sensible summary strategy for each column. 
    * Could correlate between numerical columns.
    * Pivot tables, etc. in a set of report files relating all the variables.
* estimate_unique_identification: Using the demographic information and data (may need a way to exclude free text response data) find the smallest n unique bunches and report back; may want a reference to how identifiable this makes people.


