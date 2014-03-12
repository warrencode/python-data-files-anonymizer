import os, sys, random
import xlrd, openpyxl, xlsxwriter, pandas
import ConfigParser, time, shutil, os
from collections import OrderedDict

class dataworksheet:
    """
    Simple object for storing information for a worksheet or CSV file;
    each sheet has a name (String name), data (pandas.DataFrame data)
    and columns categorized (List of Strings column_types) 

    Each Excel files is read into a list of dataworksheets.

    Each CSV files is read into a list of just one dataworksheet.
    """
    pass

def contains_one_of(stringtofind, listtocheck):
    """
    Checks for membership of a string in a list of strings (case-insensitive).

    Keyword arguments:
    stringtofind -- string to look for in the list
    listtocheck -- list of strings that stringtofind will be compared with
    """
    lowerlisttocheck = []
    for listitem in listtocheck:
        lowerlisttocheck.append(listitem.lower())
    return any(stringclue in stringtofind.lower() for stringclue in lowerlisttocheck)

def guess_column_data_type_from_name(columnnamelist):
    """
    Given list of column names, return OrderedDict of guessed column types with those names as keys.
    """
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

def read_in_data_from_file(mydatafilename):
    """
    Determine file format (.xls, .xlsx or .csv) and read, return list of dataworksheet objects.
    """
    # Determine sheet names and empty sheets (these are not handled well by pandas).
    sheet_collection_to_return = [] # OrderedDict()
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
        preworkbook.release_resources()
        # Now read again but into pandas DataFrames, except empty sheets which are handled separately.
        workbook = pandas.ExcelFile(mydatafilename)
        for worksheet_name in all_worksheets:
            worksheet = dataworksheet()
            worksheet.name = worksheet_name
            if worksheet_name in nonempty_worksheets:
                print " "
                print worksheet_name
                worksheet.data = workbook.parse(worksheet_name)
                #worksheet.column_types = guess_column_data_type_from_name(worksheet.data.columns)
                print worksheet.data.head()
            else:
                worksheet.data = None
                #worksheet.column_types = None
            sheet_collection_to_return.append(worksheet)
    elif mydatafilename.lower().endswith('.csv'):
        worksheet = dataworksheet()
        worksheet.name = mydatafilename
        worksheet.data = pandas.read_csv(mydatafilename)
        #worksheet.column_types = guess_column_data_type_from_name(worksheet.data.columns)
        sheet_collection_to_return.append(worksheet)
    else:
        print "Data file", mydatafilename, "not recognized; looking for xls, xlsx and csv files only."
    return(sheet_collection_to_return)

def retrieve_data_collection(datadirectory):
    """
    Converts data files in provided directory to dictionary of filename: dataworksheet list pairs.
    """
    data_collection = {}
    for datafilename in os.listdir(datadirectory):
        print datafilename, "\n"
        data_collection[datafilename] = read_in_data_from_file(datadirectory + datafilename)
        print "-----------------------------------------------------------"
    return(data_collection)

def confirm_data_column_types(worksheetcollection):
    """
    Interactive confirmation of dataworksheet column types across all data files.
    """
    # check metafiles for existing column types; 
    # if none exist, guess from column names and flag as needing review;
    # if some are invalid, flag for review as well
    for filename, mydataworksheets in worksheetcollection.iteritems():
        for mydataworksheet in mydataworksheets:
            pass
    #worksheet.column_types = guess_column_data_type_from_name(worksheet.data.columns)

def choose_column_to_adjust_type(worksheet):
    """
    Interactive choice of column in a dataworksheet.
    """
    column_types_copy = (worksheet.column_types).copy()
    confirmed_column_types = (worksheet.column_types).copy()
    while len(column_types_copy) > 0:
        currentliststart = len(confirmed_column_types) - len(column_types_copy) + 1
        # Build choice text, including list of options.
        columnchoicestring = "Showing columns " + str(currentliststart) + "-" + str(currentliststart + min(len(confirmed_column_types)-currentliststart, 9)) + " out of " + str(len(confirmed_column_types)) + " total\n"
        currentchoicelist = list()
        for columnchoicenumber in ['1','2','3','4','5','6','7','8','9','0']:
            currentchoicelist.append(columnchoicenumber)
            currentcolumn = column_types_copy.popitem(last=False)
            columnchoicestring += "  [" + columnchoicenumber + "] " + currentcolumn[0] + ": " + currentcolumn[1] + "\n"
            if len(column_types_copy) == 0:
                break
        columnchoicestring += "-------------------------"
        # Display choices and request input
        print columnchoicestring
        usercolumnchoice = raw_input("Choose a column to change from the list above \nor press [Enter] to continue.\n")
        # Until [Enter] is given as the input, keep requesting and processing choices.
        while usercolumnchoice:
            if usercolumnchoice in currentchoicelist:
                chosen_column_number = int(usercolumnchoice) + currentliststart - 2 # added two 1-based indices
                chosen_column_name = confirmed_column_types.keys()[chosen_column_number]
                #chosen_column_current_type = confirmed_column_types.values()[chosen_column_number]
                print "-------------------------------------"
                confirmed_column_types[chosen_column_name] = choose_column_type(chosen_column_name, confirmed_column_types[chosen_column_name], random.sample(worksheet.data[chosen_column_name],5))
            else:
                print "Invalid choice - please try again.\n\n"
            print columnchoicestring
            usercolumnchoice = raw_input("Choose a column type to change from the list above \nor press [Enter] to continue.\n")
    return(confirmed_column_types)

def choose_column_type(columnname, currentcolumntype, samplecolumnentries):
    """
    Interactive choice of column type.
    """
    newcolumntype = currentcolumntype
    typechoicestring = "Five random entries from " + chosen_column_name + ":\n"
    for entry in samplecolumnentries:
        typechoicestring += entry
        typechoicestring += "\n"
    typechoicestring += "\nCurrently, " + chosen_column_name + " is " + chosen_column_current_type
    typechoicestring += "[p] PrimaryID - incorporated into master ID list, will be replaced by anon. identifiers\n"
    typechoicestring += "[i] ID - will be replaced by anon. identifiers\n"
    typechoicestring += "[d] Drop - column will be dropped in output files\n"
    typechoicestring += "[a] Data - non-ID data, will be kept as-is\n"
    #typechoicestring += "[g] Demographic (assumes categorical)\n"
    #typechoicestring += "[c] Categorical (non-demographic) data\n"
    #typechoicestring += "[n] Numerical data\n"
    #typechoicestring += "[t] Text data (e.g. free response survey item)\n"
    typechoicestring += "-------------------------"
    typechoices = {'p':"PrimaryID", 'i':"ID", 'd':"Drop", 'a':"Data"}
    print typechoicestring
    usertypechoice = raw_input("Choose a column type from the list above\nor press [Enter] to keep the current type.\n")
    while usertypechoice:
        if contains_one_of(usertypechoice, typechoices.keys()):
            newcolumntype = typechoices[usertypechoice]
        else:
            print "Invalid choice - please try again.\n\n"
    return(newcolumntype)

def read_masterIDdataframe(masterIDkeyfilename):
    """
    Read master ID key into a DataFrame.
    """
    return(pandas.read_csv(masterIDkeyfilename, dtype=object))

def write_masterIDdataframe(masterIDdataframe, masterIDkeyfilename):
    """
    Write master ID DataFrame to file.
    """
    masterIDdataframe.to_csv(masterIDkeyfilename, index=False)
    print "Wrote", os.path.basename(masterIDkeyfilename)

def blend_with_masterIDkey(currentprimaryIDlist, masterIDkeyfilename, randomseedtouse):
    """
    If any IDs are not in current master list, generate new alternates and extend master list.
    """
    oldmasterIDkey = read_masterIDdataframe(masterIDkeyfilename)
    oldalternateidlist = oldmasterIDkey["AnonID"].tolist()
    newalternateidlist = generate_alternate_ids(currentprimaryIDlist, oldalternateidlist, randomseedtouse)
    newmasterIDkey = pandas.concat(pandas.DataFrame(pandas.Series(data=currentprimaryIDlist, name="OriginalID")), pandas.DataFrame(pandas.Series(data=newalternateidlist, name="AnonID")), axis=1)
    write_masterIDdataframe(newmasterIDkey, masterIDkeyfilename)

def collect_Primary_IDs(datacollection):
    return(set())


def anonymize_collection_IDs(datacollection, masterIDkeyfilename):
    update_masterIDkey(datacollection, masterIDkeyfilename)
    masterIDkey = read_masterIDdataframe(masterIDkeyfilename)
    cleandatacollection = {}
    # iterate through all worksheets, replacing PrimaryID and ID columns with the AnonID via joins.
    for filename, mydataworksheets in datacollection.iteritems():
        cleandatacollection[filename] = []
        for mydataworksheet in mydataworksheets:
            if mydataworksheet.column_types:
                # iterate over columns, replace or drop as needed
                #revised_col_types = confirm_data_column_types(mydataworksheet)
                cleandatacollection[filename].append(mydataworksheet)
            else:
                cleandatacollection[filename].append(mydataworksheet)
    # return the new datacollection
    return(cleandatacollection)


def update_masterIDkey(datacollection, masterIDkeyfilename, randomseedtouse):
    oldmasterIDkey = read_masterIDdataframe(masterIDkeyfilename)
    oldPrimaryIDlist = oldmasterIDkey["OriginalID"].tolist()
    oldPrimaryIDset = set(oldPrimaryIDlist)    
    fullPrimaryIDset = collect_Primary_IDs(data_collection)
    newPrimaryIDset = fullPrimaryIDset.difference(oldPrimaryIDset)
    if newPrimaryIDset:
        fullPrimaryIDlist = oldPrimaryIDlist + list(newPrimaryIDset)
        blend_with_masterIDkey(fullPrimaryIDlist, masterIDkeyfilename, randomseedtouse)
    else:
        print "No new IDs; master ID key unchanged."

def create_anonymous_worksheet(originalworksheet, masterIDdataframe):
    """
    Return an anonymized version of this worksheet using column types and anonymous ID list.

    The column of PrimaryID type is replaced by elements from the masterIDdataframe.

    Columns of other ID type and those set to "drop" type are dropped.

    Other columns (demographics and data) are left as they are.

    Keyword arguments:
    originalworksheet -- dataworksheet containing original data and identifiers
    masterIDdataframe -- keys are original IDs, values are anonymous replacements.
    """
    pass

def write_cleaned_data_file(originalfilename, cleaneddata, outputdir):
    """
    For .xls, .xlsx or .csv files, write out list of dataworksheet objects; otherwise just copy.

    Files that have been anonymized will have the same filename as the originals
    except that '_anon' is appended to the end of the name before the extension. 

    Keyword arguments:
    originalfilename -- same file name used by read_in_data_from_file to extract data
    cleaneddata -- list of dataworksheet objects
    outputdir -- where the output files will be created
    """
    fileextension = os.path.splitext(originalfilename)[1]
    outputfilename = outputdir + os.path.splitext(os.path.basename(originalfilename))[0] + "_anon" + fileextension
    if originalfilename.lower().endswith(('.xls', '.xlsx')):
        # Currently ignores any empty or otherwise nonregular sheets; they are not copied over.
        ewriter = pandas.ExcelWriter(outputfilename)
        for worksheet in cleaneddata:
            if not worksheet.data is None:
                worksheet.data.to_excel(ewriter, worksheet.name, index=False)
        ewriter.save()
        print "Wrote", os.path.basename(originalfilename)
    elif originalfilename.lower().endswith('.csv'):
        cleaneddata[0].data.to_csv(outputfilename, index=False)
        print "Wrote", os.path.basename(originalfilename)
    else:
        # copy directly with name unchanged (no anonymizing performed)
        outputfilename = outputdir + os.path.basename(originalfilename)
        if (not os.path.exists(outputfilename)) or (os.stat(originalfilename).st_mtime - os.stat(outputfilename).st_mtime > 1):
            shutil.copy2(originalfilename, outputfilename)
            print "Copied", os.path.basename(originalfilename)
        else:
            print os.path.basename(originalfilename),"is the same in the source and target directories (not copied)."

def write_data_collection_to_output_directory(data_collection, inputdir, outputdir):
    """
    For each input directory file, write data items to output file (or copy if not of this type).
    """
    for datafilename in os.listdir(inputdir):
        write_cleaned_data_file(inputdir + datafilename, data_collection[datafilename], outputdir)

def generate_alternate_ids(originalidlist, currentalternateidlist, randomseedtouse):
    """
    Extend list of alternate IDs to have a complete set anonymizing the originals.

    Given a list of original identifiers and an existing list of anonymous IDs (could be empty),
    extend the latter so that each original identifier has an anonymous ID based on a
    randomly-generated number.  The new identifiers are based only on the position of the
    original in the list, so there is no way to recover the original IDs without a master key.

    If the same random seed is used that was used to generate currentalternateidlist,
    the output list is an extended version (i.e. first len(currentalternateidlist) IDs
    are identical) of currentalternateidlist, preserving any previously generated IDs

    Keyword arguments:
    originalidlist -- List of primary identifiers to be anonymized (currently only length is used)
    currentalternateidlist -- list of dataworksheet objects
    randomseedtouse -- Number to use as random seed.
    """
    random.seed(randomseedtouse)
    fullaltidset = set(currentalternateidlist)
    newalternateidlist = list(currentalternateidlist)
    while len(fullaltidset) < len(originalidlist):
        newaltid = random.randint(100000000,999999999)
        if newaltid not in fullaltidset:
            newalternateidlist.append(newaltid)
            fullaltidset.add(newaltid)
    return(newalternateidlist)
    
def test_generate_alternate_ids():
    """
    Attempts creation and two extensions (generate_alternate_ids) of short list of anonymous IDs.
    """
    primaryIDlist = range(1,10)
    anonIDlist = generate_alternate_ids(primaryIDlist, list(), RANDOM_SEED)

    for i in range(1,9):
        print anonIDlist[i]
    print "----------------COMPARE---------------------"

    anonIDlist2 = generate_alternate_ids(range(1,20), anonIDlist, RANDOM_SEED)

    for j in range(1,15):
        print anonIDlist2[j]
    print "----------------COMPARE---------------------"

    anonIDlist3 = generate_alternate_ids(range(1,30), anonIDlist2, RANDOM_SEED)

    for k in range(1,25):
        print anonIDlist3[k]

print "-----------------------------------------------------------"

##----------------------------------------------------------------------------------------------------------------------
## Main script starts here
##----------------------------------------------------------------------------------------------------------------------

PROJECT_NAME = "sample_project"

print "Run of project", PROJECT_NAME, "started on", time.strftime('%Y-%m-%d')
RAWDATA_DIR = "../projects/" + PROJECT_NAME + "/rawdata/"
OUTPUTDATA_DIR = "../projects/" + PROJECT_NAME + "/output/"
METAFILE_DIR = "../projects/" + PROJECT_NAME + "/metafiles/"

config = ConfigParser.ConfigParser()
config.read("../projects/" + PROJECT_NAME + "/metafiles/project_settings.txt")
RANDOM_SEED = config.get("Project Settings", "Random Seed")

data_collection = retrieve_data_collection(RAWDATA_DIR)
# print data_collection
# confirm column types?

print "*** Anonymization process happens here. ***"

print "Collect ID list"

cleaned_data_collection = anonymize_collection_IDs(data_collection, METAFILE_DIR + "masterIDkey.csv", RANDOM_SEED)

print "-----------------------------------------------------------"

write_data_collection_to_output_directory(data_collection, RAWDATA_DIR, OUTPUTDATA_DIR)

print "-----------------------------------------------------------"

