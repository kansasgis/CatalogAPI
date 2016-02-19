#-------------------------------------------------------------------------------
# Name:        DASC_UpdateCatalogJSON
# Purpose:     Add an entry to the DASC JSON catalog
#
# Author:      kristen
#
# Created:     18/02/2016
#-------------------------------------------------------------------------------
from arcpy import GetParameterAsText, AddMessage

class jsonEntry(object):
    id = ""
    title = ""
    description = ""
    projection = ""
    downloadlink = ""
    servicelink = ""
    metadatalink = ""
    datacategory = ""
    documentation = ""
    datacreator = ""
    weblink = ""
    tags = ""
    geojsonlink = ""
    thumbnail = ""

    def __init__(self, id, title, description, projection, downloadlink, servicelink, metadatalink, datacategory, documentation, datacreator, weblink, tags, geojsonlink, thumbnail):
        self.id = id
        self.title = title
        self.description = description
        self.projection = projection
        self.downloadlink = downloadlink
        self.servicelink = servicelink
        self.metadatalink = metadatalink
        self.datacategory = datacategory
        self.documentation = documentation
        self.datacreator = datacreator
        self.weblink = weblink
        self.tags = tags
        self.geojsonlink = geojsonlink
        self.thumbnail = thumbnail


def main():
    #get parameters from a tool interface
    id1 = GetParameterAsText(0)
    title = GetParameterAsText(1)
    description = GetParameterAsText(2)
    projection = GetParameterAsText(3)
    dataTitles = GetParameterAsText(4)
    dataTypes = GetParameterAsText(5)
    dataDownloads = GetParameterAsText(6)
    services = GetParameterAsText(7)
    metadata = GetParameterAsText(8)
    dataCategory = GetParameterAsText(9)
    documentations = GetParameterAsText(10)
    dataCreator = GetParameterAsText(11)
    webLink = GetParameterAsText(12)
    tags = GetParameterAsText(13)
    geoJSONLink = GetParameterAsText(14)
    thumbnailUrl = GetParameterAsText(15)
    existingfile = GetParameterAsText(16)

    #create download list in proper format
    DL_list = ""
    if dataTitles != "":
        dataTitlesList = dataTitles.split(",")
        dataTypesList = dataTypes.split(",")
        dataDownloadsList = dataDownloads.split(",")

        DL_list = "["
        for dt in dataTitlesList:
            i = dataTitlesList.index(dt)
            DL_list += '{"DataTitle":"' + dt.strip() + '","DataType":"' + dataTypesList[i].strip() + '","url":"' + dataDownloadsList[i].strip() + '"},'

        DL_list = DL_list[:-1] + "]"

    #put services in a list
    service_list = ""
    if services != "":
        servicesList = services.split(",")
        for s in servicesList:
            service_list += '"' + s.strip() + '",'

        service_list = service_list[:-1]

    #put documentation in a list
    doc_list = ""
    if documentations != "":
        docList = documentations.split(",")
        for d in docList:
            doc_list += '"' + d.strip() + '",'

        doc_list = doc_list[:-1]

    #format tags
    tag_list = ""
    if tags != "":
        tagList = tags.split(",")
        for t in tagList:
            tag_list += '"' + t.strip() + '",'

        tag_list = tag_list[:-1]

    entryObject = jsonEntry(id1, title, description, projection, DL_list, service_list, metadata, dataCategory, doc_list, dataCreator, webLink, tag_list, geoJSONLink, thumbnailUrl)

    jsonText = object2Json(entryObject)

    addEntry(existingfile, jsonText)

def object2Json(entryObject):

    jsonFormat = '{"ID":"' + entryObject.id + '","Title":"' + entryObject.title + '","Description":"' + entryObject.description

    jsonFormat += '","Projection":"' + entryObject.projection

    jsonFormat += '","DownloadLink":' + entryObject.downloadlink + ',"ServiceLink":[' + entryObject.servicelink + '],"MetadataLink":"' + entryObject.metadatalink

    jsonFormat += '","DataCategory":"' + entryObject.datacategory + '","Documentation":[' + entryObject.documentation + '],"DataCreator":"'

    jsonFormat += entryObject.datacreator + '","WebLink":"' + entryObject.weblink + '","Tags":[' + entryObject.tags + '],"GeoJsonLink":"'

    jsonFormat += entryObject.geojsonlink + '","Thumbnail":"' + entryObject.thumbnail + '"}'

    return jsonFormat


def addEntry(existingfile, jsonText):

    #read existing file
    with open(existingfile, "r") as f:
        previous = f.read()

    #take off the end characters, make the new text
    newStuff = previous.replace("]}}","," + jsonText + "]}}")
##    newStuff = previous.replace("]}}","!!!")
    with open(existingfile, "w") as g:
        #save a copy
        g.write(newStuff)

if __name__ == '__main__':
    main()
