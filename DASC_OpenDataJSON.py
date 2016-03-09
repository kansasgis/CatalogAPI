#-------------------------------------------------------------------------------
# Name:        DASC_OpenDataJSON
# Purpose:     Add an entry to the DASC JSON catalog in Open Data format
#
# Author:      kristen
#
# Created:     18/02/2016
#-------------------------------------------------------------------------------
from arcpy import GetParameterAsText, AddMessage

class jsonEntry(object):
    title = ""
    description = ""
    distribution = ""
    theme = ""
    keyword = ""

    def __init__(self, title, description, distribution, theme, keyword):
        self.title = title
        self.distribution = distribution
        self.description = description
        self.theme = theme
        self.keyword = keyword


def main():
    #get parameters from a tool interface
    title = GetParameterAsText(0)
    description = GetParameterAsText(1)
    dataTitles = GetParameterAsText(2)
    dataTypes = GetParameterAsText(3)
    dataDownloads = GetParameterAsText(4)
    dataFormats = GetParameterAsText(5)
    theme = GetParameterAsText(6)
    accessURL = GetParameterAsText(7)
    keyword = GetParameterAsText(8)
    existingfile = GetParameterAsText(9)

    #create download list in proper format
    DL_list = ""
    if dataTitles != "" or accessURL != "":
        lists = 0
        try:
            dataTitlesList = dataTitles.split(",")
            dataTypesList = dataTypes.split(",")
            dataDownloadsList = dataDownloads.split(",")
            dataFormatList = dataFormats.split(",")
            lists = 1
        except:
            print "one or more lists could not be split"

        DL_list = '"distribution": ['
        if lists == 1:
            for dt in dataTitlesList:
                i = dataTitlesList.index(dt)
                DL_list += '{"downloadURL":"' + dataDownloadsList[i].strip() + '","mediaType":"' + dataTypesList[i].strip() + '","format":"' + dataFormatList[i].strip() + '","title":"' + dt.strip() + '"},'

        #if there's a permalink, add it
        if accessURL != "":
            DL_list += '{"accessURL":"' + accessURL + '"}'

        #if the last character is a comma, remove it
        if DL_list[:-1] == ",":
            DL_list = DL_list[:-1]

        #make a pretty close to the
        DL_list += "]"

    #format tags
    keyword_list = '"keyword": ['
    if keyword != "":
        #create some error trapping
        if "," in keyword:
            keywordList = keyword.split(",")
        else:
            keywordList =[keyword]

        for k in keywordList:
            keyword_list += '"' + k.strip() + '",'

        keyword_list = keyword_list[:-1] + ']'

    entryObject = jsonEntry(title, description, DL_list, theme, keyword_list)

    jsonText = object2Json(entryObject)

    addEntry(existingfile, jsonText)

def object2Json(entryObject):

    jsonFormat = '{"accessLevel":"public","contactPoint": {"fn":"Kansas Data Access and Support Center","hasEmail": "mailto:dasc@kgs.ku.edu"},'

    jsonFormat += '"description":"' + entryObject.description + '",'

    jsonFormat += entryObject.distribution + ","

    jsonFormat += '"theme":"' + entryObject.theme + '",' + entryObject.keyword + ','

    jsonFormat += '"publisher": { "name": "Kansas Data Access and Support Center","subOrganizationOf": {"name":"State of Kansas"}},'

    jsonFormat += '"title": "' + entryObject.title + '"}'

    return jsonFormat


def addEntry(existingfile, jsonText):

    #read existing file
    with open(existingfile, "r") as f:
        previous = f.read()

    #take off the end characters, make the new text
    newStuff = previous.replace("}]}","}," + jsonText + "]}")
##    newStuff = previous.replace("]}}","!!!")
    with open(existingfile, "w") as g:
        #save a copy
        g.write(newStuff)

if __name__ == '__main__':
    main()
