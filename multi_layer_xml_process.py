import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
import operator
import itertools


# target xml file is shown below

#mypath = "/Users/user/Euan_freelancing/Yara_project/new_data_source/Archive/FutureFarm-CropPlan-2020.xml"
#mypath = "/Users/user/PycharmProjects/xml_manipulation_v/sample.xml"
mypath = "INSERT_PATH_TO_FILE_DIRECTORY"


path_to_xml_file = mypath

# Load xml file data
tree = ET.parse(path_to_xml_file)

data = []
level = []

# Specific tag here chosen which we will be iterated over. e.g. tag='{http://tempuri.org/Export.xsd}Skifte'
for top in tree.iter():

    # following loop appends preceding layer information to the list data.
    # Additional level list is utilised for future removal of data that has further levels.

    x1 = top.items()
    print(x1)
    z = x1
    data.append(z)
    level.append(3)
    for middle in top.iterfind('*'):
        x2 = middle.items()
        z = x1 + x2
        data.append(z)
        level.append(2)
        for bottom in middle.iterfind('*'):
            x3 = bottom.items()
            z = x1 + x2 + x3
            data.append(z)
            level.append(1)

columns = ([[y[0] for y in  z] for z in data])
columns = set(x for l in columns for x in l)
columns = list(columns)
columns.sort()

# removal of data at intermediary stages that has further levels of data.

to_remove = []
x = level[:1]
for i in level[1:]:
    if i < x[-1]:
        x.append(i)
        to_remove.append(False)
    else:
        x.append(i)
        to_remove.append(True)

to_remove.append(True)

data = np.array(data)
filter = np.array(to_remove)
data = data[filter]

print(data)

# for each point of scraped data the missing columns are added
# for the purposes of adding them to the dataframe.

list_to_df = []
i = 0
while i < len(data):
    data_x = [[y for y in z] for z in data[i]]

    main_list = np.setdiff1d(columns, data_x)

    main_list = [[x, ''] for x in main_list]

    list_1_final = data_x + main_list
    list_1_final.sort(key=lambda x: x[0])

    list_1_final.sort()
    list_1_final = list(k for k, _ in itertools.groupby(list_1_final))
    list_to_df.append(list_1_final)
    i += 1

sorted(list_to_df, key=operator.itemgetter(0))


df1 = pd.DataFrame([[y[1] for y in  z] for z in list_to_df])

print(df1)


df1.to_csv('INSERT_CSV_NAME')
