import deidentify_methods
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

data_collection = {}

for datafilename in os.listdir(RAWDATA_DIR):
    print datafilename, "\n"
    data_collection[datafilename] = read_in_data_from_file(RAWDATA_DIR + datafilename)
    print "-----------------------------------------------------------"

print data_collection
print "*** Anonymization process happens here. ***"

print "Collect ID list"
# primaryIDlist = 

# for filename, mydataworksheets in data_collection.iteritems():
#     for mydataworksheet in mydataworksheets:
#         if mydataworksheet.column_types:
#             revised_col_types = confirm_data_column_types(mydataworksheet)

print "-----------------------------------------------------------"

for datafilename in os.listdir(RAWDATA_DIR):
    write_cleaned_data_file(RAWDATA_DIR + datafilename, data_collection[datafilename], OUTPUTDATA_DIR)

print "-----------------------------------------------------------"
