import os, sys, ConfigParser, time, shutil
import xlrd, openpyxl, xlsxwriter, pandas
from collections import OrderedDict

# checks lower-case inclusions
def contains_one_of(mystring, listtocheck):
	lowerlisttocheck = []
	for listitem in listtocheck:
		lowerlisttocheck.append(listitem.lower())
	return any(stringclue in mystring.lower() for stringclue in lowerlisttocheck)


# Guess column type, so far only based on the column name.
# Could check for uniqueness, names, 8-digit numbers (UBC student IDs) to guess if the column is Primary Key, demographic, ID, or data.
def guess_column_data_type_from_name(columnnamelist):
	print "Column data types:"
	print "------------------"
	guess_list = OrderedDict()
	for column_name in columnnamelist:
		data_type_guess = "Data"
		if contains_one_of(column_name, ['gender','sex','section','course']):
			data_type_guess = "Demographic"
		elif contains_one_of(column_name, ['name']):
			data_type_guess = "ID"
		elif contains_one_of(column_name, ['stdid','student']):
			data_type_guess = "PrimaryID"
		guess_list[column_name] = data_type_guess
		print column_name,"-",data_type_guess
	return guess_list

# return an ordered dictionary of sheets
def read_in_data_from_file(mydatafilename):
    sheet_collection_to_return = OrderedDict()
    if mydatafilename.lower().endswith(('.xls', '.xlsx')):
        preworkbook = xlrd.open_workbook(mydatafilename)
        print "The number of worksheets is", preworkbook.nsheets
        print "Worksheet name(s):", preworkbook.sheet_names()
        all_worksheets = preworkbook.sheet_names()
        nonempty_worksheets = []
        for worksheet_name in all_worksheets:
            print " "
            worksheet = preworkbook.sheet_by_name(worksheet_name)
            if worksheet.nrows>0:
            	print mydatafilename, worksheet.name, "has", worksheet.nrows, "rows,", worksheet.ncols, "columns"
                nonempty_worksheets.append(worksheet_name)
            else:
            	print mydatafilename, worksheet.name, "is empty."
            	continue

        workbook = pandas.ExcelFile(mydatafilename)
##        print workbook.sheet_names
##        sheet_set = {sheet_name: workbook.parse(sheet_name) for sheet_name in nonempty_worksheets}

        for worksheet_name in all_worksheets:
            if worksheet_name in nonempty_worksheets:
                print " "
                print worksheet_name
                worksheet = workbook.parse(worksheet_name)
                print worksheet.head()
                sheet_collection_to_return[worksheet_name] = worksheet
            else:
                sheet_collection_to_return[worksheet_name] = None

##            column_names = []
##            for cx in range(worksheet.ncols):
##            	if (len(worksheet.col_values(cx))>4):
##            		print worksheet.col_values(cx)[0],"=",worksheet.col_values(cx)[1:4],"..."
##            	else:
##            		print worksheet.col_values(cx)[0],"="
##            	column_names.append(worksheet.col_values(cx)[0])
##            column_data_types = guess_column_data_type_from_name(column_names)
##            #print "Column data types:",column_data_types
    elif mydatafilename.lower().endswith('.csv'):
        worksheet = pandas.read_csv(mydatafilename)
        print worksheet
        sheet_collection_to_return[mydatafilename] = worksheet
##		csv_data = []
###		data_to_return = []
##		with open(mydatafilename, 'rb') as csvfile:
###			dialect = csv.Sniffer().sniff(csvfile.read(1024))
###			csvfile.seek(0)
##			myreader = csv.DictReader(csvfile, delimiter=',')
##			for row in myreader:
##				csv_data.append(row)
##		print csv_data
##
##		column_names = csv_data[0].keys()
##		column_data_types = guess_column_data_type_from_name(column_names)
##
###		data_to_return[mydatafilename] = csv_data
    else:
		print "Data file", mydatafilename, "not recognized; looking for xls, xlsx and csv files only."

    return(sheet_collection_to_return)


# Uses filename to choose from xls, csv, etc.
# Later, should check date of input file; only write if target file is absent, prompt if input file has changed.
def write_cleaned_data_file(originalfilename, cleaneddata, outputdir):
    print cleaneddata
    fileextension = os.path.splitext(originalfilename)[1]
    outputfilename = outputdir + os.path.splitext(os.path.basename(originalfilename))[0] + "_anon" + fileextension
    if originalfilename.lower().endswith(('.xls', '.xlsx')):
        # Currently ignores any empty or otherwise nonregular sheets; they are not copied over.
        ewriter = pandas.ExcelWriter(outputfilename)
        for sheet_name,sheet_data in cleaneddata.iteritems():
            if not sheet_data is None:
                sheet_data.to_excel(ewriter, sheet_name)
        ewriter.save()
        print "Wrote", os.path.basename(originalfilename)
    elif originalfilename.lower().endswith('.csv'):
        cleaneddata[originalfilename].to_csv(outputfilename)
        print "Wrote", os.path.basename(originalfilename)
    else:
        # copy directly with name unchanged (no anonymizing performed)
        outputfilename = outputdir + os.path.basename(originalfilename)
        if (not os.path.exists(outputfilename)) or (os.stat(originalfilename).st_mtime - os.stat(outputfilename).st_mtime > 1):
            shutil.copy2(originalfilename, outputfilename)
            print "Copied", os.path.basename(originalfilename)
        else:
            print os.path.basename(originalfilename),"is the same in the source and target directories (not copied)."



##----------------------------------------------------------------------------------------------------------------------
## Main script starts here
##----------------------------------------------------------------------------------------------------------------------

config = ConfigParser.ConfigParser()
config.read("../metafiles/project_settings.txt")

print "Run of project", config.get("Project","name"), "started on", time.strftime('%Y-%m-%d')
RAWDATA_DIR = config.get("Data","Raw data directory")
OUTPUTDATA_DIR = config.get("Data","Output data directory")

data_collection = {}

for datafilename in os.listdir(RAWDATA_DIR):
	print datafilename, "\n"
	data_collection[datafilename] = read_in_data_from_file(RAWDATA_DIR + datafilename)
	print "-----------------------------------------------------------"

print data_collection
print "*** Anonymization process happens here. ***"
print "-----------------------------------------------------------"


for datafilename in os.listdir(RAWDATA_DIR):
	write_cleaned_data_file(RAWDATA_DIR + datafilename, data_collection[datafilename], OUTPUTDATA_DIR)

print "-----------------------------------------------------------"


# guess_data_type
# Figure out sensible summary strategy for the column. Could correlate between numerical ones.

# read_master_id_list
# Returns the existing master list from the relevant metadata directory. Also reads the randomizing seed for the list and the anonymous ID style (default is project name string plus 10-digit number).

# write_master_id_list
# Compare with existing list; updates should effectively only append new primary IDs.

# project_setup.py
# Argument (or interactive) name of project, with confirmation and list of directories created.  Optional set own seed or use random seed, creates master ID list file with seed but no actual entries, maybe a placeholder message in case anyone looks at it.

# To obtain Primary ID, ask for number of column or to see column headers, or read from existing metafile.

# process_columns
# Either reads from an existing metafile that describes the column names and types, or interactively confirms column types primed with guesses then writes a new metafile.

# aggregate_across_sheets
# Optional, joins all available sheets using the Primary IDs, filling in appropriate NA for missing data. If column names are duplicated, use file/sheet name or prompt for prefix/suffix.


# generate_alternate_ids
# Accept a list of primary IDs; first iteration is just to use the length and the projects's random seed and new ID format to make random ones. Compare with previous alternate list (even if incomplete) to confirm that scheme has been preserved.

# blend_with_master_list
# Compares given list of IDs with existing master list and determines which are not present, then adds those to the bottom and generates new random list to match these.

# estimate_unique_identification
# Use the demographic information and data (may need a way to exclude free text response data) find the smallest five unique bunches and report back.
