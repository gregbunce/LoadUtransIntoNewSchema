'''
    @author: gbunce
    @contact: gbunce@utah.gov
    @company: State of Utah AGRC
    @version: 1.0.0
    @description: this scripts imports features from UTRANS Roads dataset into a file geodatabase containing AGRC's new schema - additionally you can assign certain fields spatially via road segment offset pnts and the identity tool
    @requirements: Python 2.7.x, ArcGIS 10.2.1 through ArcGIS 10.4.x
    @copyright: State of Utah AGRC, 2016
'''

import arcpy
from time import gmtime, strftime
import sys, os, datetime, traceback
from os.path import dirname, join, exists, splitext, isfile
from arcpy import env

# maybe make these imput parameters
utransRoads = r'Database Connections\DC_TRANSADMIN@UTRANS@utrans.agrc.utah.gov.sde\UTRANS.TRANSADMIN.Centerlines_Edit\UTRANS.TRANSADMIN.StatewideStreets'
#utransRoads = r'D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\UtransTesting'
newRoadsSchemaFGBpath = r'D:\SGID Roads New Schema\CenterLineSchema20161031_105124.gdb\RoadCenterlines'

# append SettyBetty method to the FieldMap object... to aviod the annoying output name pattern
def setOutputFieldName(self, name):
    """set the output field name of a fieldmap."""
    tempName = self.outputField
    tempName.name = name
    #tempName.aliasName = name
    self.outputField = tempName
arcpy.FieldMap.outputFieldSettyBetty = setOutputFieldName


def main(utransRoads, newRoadsSchemaFGBpath):
    try:
        #_add_global_error_handler()
        
        #createCountyNameDictionary()

        # testing raising exceptions
        # raise Exception('testing')

        # delete existing features in file geodatabase
        arcpy.management.TruncateTable(newRoadsSchemaFGBpath)
        print "Truncating the data in the new schema feature class"
        arcpy.management.TruncateTable(newRoadsSchemaFGBpath)

        # use field mapping to transfer the data over
        fieldmappings = arcpy.FieldMappings()

        ## create a field map-variable for each field in the new-schema-FGD roads feature class
        fldmap_CartoCode = arcpy.FieldMap()
        fldmap_FullName = arcpy.FieldMap()
        fldmap_LeftFrom = arcpy.FieldMap()
        fldmap_LeftTo = arcpy.FieldMap()
        fldmap_RightFrom = arcpy.FieldMap()
        fldmap_RightTo = arcpy.FieldMap()
        fldmap_Status = arcpy.FieldMap()
        fldmap_ParityL = arcpy.FieldMap()
        fldmap_ParityR = arcpy.FieldMap()
        fldmap_PreDir = arcpy.FieldMap()
        fldmap_Name = arcpy.FieldMap()
        fldmap_PostType = arcpy.FieldMap()
        fldmap_PostDir = arcpy.FieldMap()
        fldmap_AN_Name = arcpy.FieldMap()
        fldmap_AN_PostDir = arcpy.FieldMap()
        fldmap_A1_PreDir = arcpy.FieldMap()
        fldmap_A1_Name = arcpy.FieldMap()
        fldmap_A1_PostType = arcpy.FieldMap()
        fldmap_A1_PostDir = arcpy.FieldMap()
        fldmap_A2_PreDir = arcpy.FieldMap()
        fldmap_A2_Name = arcpy.FieldMap()
        fldmap_A2_PostType = arcpy.FieldMap()
        fldmap_A2_PostDir = arcpy.FieldMap()
        fldmap_AddrSystemQuad = arcpy.FieldMap()
        fldmap_StateL = arcpy.FieldMap()
        fldmap_StateR = arcpy.FieldMap()
        fldmap_CountyL = arcpy.FieldMap()
        fldmap_CountyR = arcpy.FieldMap()
        fldmap_AddrSystemL = arcpy.FieldMap()
        fldmap_AddrSystemR = arcpy.FieldMap()
        fldmap_PostalCommNameR = arcpy.FieldMap()
        fldmap_PostalCommNameL = arcpy.FieldMap()
        fldmap_ZipCodeL = arcpy.FieldMap()
        fldmap_ZipCodeR = arcpy.FieldMap()
        fldmap_IncMuniL = arcpy.FieldMap()  
        fldmap_IncMuniR = arcpy.FieldMap()
        fldmap_UnIncMuniL = arcpy.FieldMap()
        fldmap_UnIncMuniR = arcpy.FieldMap()
        fldmap_NeighbCommL = arcpy.FieldMap()
        fldmap_NeighbCommR = arcpy.FieldMap()
        fldmap_ER_CAD_Zones = arcpy.FieldMap()
        fldmap_EsnL = arcpy.FieldMap()
        fldmap_EsnR = arcpy.FieldMap()
        fldmap_MsagCommL = arcpy.FieldMap()
        fldmap_MsagCommR = arcpy.FieldMap()
        fldmap_OneWay = arcpy.FieldMap()
        fldmap_VertLevel = arcpy.FieldMap()
        fldmap_SpeedLimit = arcpy.FieldMap()
        fldmap_Access = arcpy.FieldMap()
        fldmap_Dot_HwyName = arcpy.FieldMap()
        fldmap_Dot_RtName = arcpy.FieldMap()
        fldmap_Dot_RtPart = arcpy.FieldMap()
        fldmap_Dot_F_Mile = arcpy.FieldMap()
        fldmap_Dot_T_Mile = arcpy.FieldMap()
        fldmap_Dot_F_Class = arcpy.FieldMap()
        fldmap_Dot_SurfType = arcpy.FieldMap()
        fldmap_Dot_Class = arcpy.FieldMap()
        fldmap_Dot_RDOWN = arcpy.FieldMap()
        fldmap_Dot_AADT = arcpy.FieldMap()
        fldmap_Dot_AADTYR = arcpy.FieldMap()
        fldmap_BikeL = arcpy.FieldMap()
        fldmap_BikeR = arcpy.FieldMap()
        fldmap_BikeNotes = arcpy.FieldMap()
        fldmap_BikeStatus = arcpy.FieldMap()
        fldmap_CustomTags = arcpy.FieldMap()
        fldmap_UniqueID = arcpy.FieldMap()
        fldmap_LocalUniqueID = arcpy.FieldMap()
        fldmap_RoadCL_UID = arcpy.FieldMap()
        fldmap_Source = arcpy.FieldMap()
        fldmap_Updated = arcpy.FieldMap()
        fldmap_Effective = arcpy.FieldMap()
        fldmap_Expire = arcpy.FieldMap()

        ## Add all fields from the input feature class (utrans) to the fieldmappings object. AddTable is the most efficient way.
        fieldmappings.addTable(utransRoads)

        ## define field maps for each field based on field names
        # comment key for field descriptions in new schema --> (FIELDNAME - datatype legnth domain)

        # STATUS - text 10 w/domain
        fldmap_Status.addInputField(utransRoads, "STATUS")
        fldmap_Status.outputFieldSettyBetty('STATUS')
        fieldmappings.addFieldMap(fldmap_Status)

        # CARTOCODE - text 10 w/domain
        fldmap_CartoCode.addInputField(utransRoads, "CARTOCODE")
        fldmap_CartoCode.outputFieldSettyBetty('CARTOCODE')
        fieldmappings.addFieldMap(fldmap_CartoCode)

        # FULLNAME - text 125
        fldmap_FullName.addInputField(utransRoads, "FULLNAME")
        fldmap_FullName.outputFieldSettyBetty('FULLNAME')
        fieldmappings.addFieldMap(fldmap_FullName)

        # FROMADDR_L - longint
        fldmap_LeftFrom.addInputField(utransRoads, "L_F_ADD") # double
        fldmap_LeftFrom.outputFieldSettyBetty('FROMADDR_L');
        fieldmappings.addFieldMap(fldmap_LeftFrom)

        # TOADDR_L - longint
        fldmap_LeftTo.addInputField(utransRoads, "L_T_ADD") # double
        fldmap_LeftTo.outputFieldSettyBetty('TOADDR_L')
        fieldmappings.addFieldMap(fldmap_LeftTo)

        # FROMADDR_R - longint
        fldmap_RightFrom.addInputField(utransRoads, "R_F_ADD") # double
        fldmap_RightFrom.outputFieldSettyBetty('FROMADDR_R')
        fieldmappings.addFieldMap(fldmap_RightFrom)

        # TOADDR_R - longint
        fldmap_RightTo.addInputField(utransRoads, "R_T_ADD") # double
        fldmap_RightTo.outputFieldSettyBetty('TOADDR_R')
        fieldmappings.addFieldMap(fldmap_RightTo)

        # PARITY_L - text 1

        # PARITY_R - text 1

        # PREDIR - text 2 w/domain
        fldmap_PreDir.addInputField(utransRoads, "PREDIR")
        fldmap_PreDir.outputFieldSettyBetty('PREDIR')
        fieldmappings.addFieldMap(fldmap_PreDir)

        # NAME - text 60
        fldmap_Name.addInputField(utransRoads, "STREETNAME")
        fldmap_Name.outputFieldSettyBetty('NAME')
        fieldmappings.addFieldMap(fldmap_Name)

        # POSTTYPE - text 4 w/domain
        fldmap_PostType.addInputField(utransRoads, "STREETTYPE")
        fldmap_PostType.outputFieldSettyBetty('POSTTYPE')
        fieldmappings.addFieldMap(fldmap_PostType)

        # POSTDIR - text 2 w/domain
        fldmap_PostDir.addInputField(utransRoads, "SUFDIR")
        fldmap_PostDir.outputFieldSettyBetty('POSTDIR')
        fieldmappings.addFieldMap(fldmap_PostDir)

        # AN_NAME - text 10
        fldmap_AN_Name.addInputField(utransRoads, "ACSNAME")
        fldmap_AN_Name.outputFieldSettyBetty('AN_NAME')
        fieldmappings.addFieldMap(fldmap_AN_Name)

        # AN_POSTDIR - text 2 w/domain
        fldmap_AN_PostDir.addInputField(utransRoads, "ACSSUF")
        fldmap_AN_PostDir.outputFieldSettyBetty('AN_POSTDIR')
        fieldmappings.addFieldMap(fldmap_AN_PostDir)

        # A1_PREDIR - text 2 w/domain
        fldmap_A1_PreDir.addInputField(utransRoads, "PREDIR")
        fldmap_A1_PreDir.outputFieldSettyBetty('A1_PREDIR')
        fieldmappings.addFieldMap(fldmap_A1_PreDir)

        # A1_NAME - text 60
        fldmap_A1_Name.addInputField(utransRoads, "ALIAS1")
        fldmap_A1_Name.outputFieldSettyBetty('A1_NAME')
        fieldmappings.addFieldMap(fldmap_A1_Name)

        # A1_POSTTYPE - text 4 w/domain
        fldmap_A1_PostType.addInputField(utransRoads, "ALIAS1TYPE")
        fldmap_A1_PostType.outputFieldSettyBetty('A1_POSTTYPE')
        fieldmappings.addFieldMap(fldmap_A1_PostType)

        # A1_POSTDIR - text 2 w/domain

        # A2_PREDIR - text 2 w/domain
        fldmap_A2_PreDir.addInputField(utransRoads, "PREDIR")
        fldmap_A2_PreDir.outputFieldSettyBetty('A2_PREDIR')
        fieldmappings.addFieldMap(fldmap_A2_PreDir)
        
        # A2_NAME - text 60
        fldmap_A2_Name.addInputField(utransRoads, "ALIAS2")
        fldmap_A2_Name.outputFieldSettyBetty('A2_NAME')
        fieldmappings.addFieldMap(fldmap_A2_Name)

        # A2_POSTTYPE - text 4 w/domain 
        fldmap_A2_PostType.addInputField(utransRoads, "ALIAS2TYPE")
        fldmap_A2_PostType.outputFieldSettyBetty('A2_POSTTYPE')
        fieldmappings.addFieldMap(fldmap_A2_PostType)

        # A2_POSTDIR - text 2 w/domain

        # ADDRSYS_QUAD - text 2
        fldmap_AddrSystemQuad.addInputField(utransRoads, "ADDR_QUAD")
        fldmap_AddrSystemQuad.outputFieldSettyBetty('QUADRANT')
        fieldmappings.addFieldMap(fldmap_AddrSystemQuad)

        # STATE_L - text 2 w/domain

        # STATE_R - text 2 w/domain

        # COUNTY_L - text 40 w/domain
        fldmap_CountyL.addInputField(utransRoads, "COFIPS")
        fldmap_CountyL.outputFieldSettyBetty('COUNTY_L')
        fieldmappings.addFieldMap(fldmap_CountyL)

        # COUNTY_R - text 40 w/domain
        fldmap_CountyR.addInputField(utransRoads, "COFIPS")
        fldmap_CountyR.outputFieldSettyBetty('COUNTY_R')
        fieldmappings.addFieldMap(fldmap_CountyR)

        # ADDRSYS_L - text 50 w/domain
        fldmap_AddrSystemL.addInputField(utransRoads, "ADDR_SYS")
        fldmap_AddrSystemL.outputFieldSettyBetty('ADDRSYS_L')
        fieldmappings.addFieldMap(fldmap_AddrSystemL)

        # ADDRSYS_R - text 50 w/domain
        fldmap_AddrSystemR.addInputField(utransRoads, "ADDR_SYS")
        fldmap_AddrSystemR.outputFieldSettyBetty('ADDRSYS_R')
        fieldmappings.addFieldMap(fldmap_AddrSystemR)

        # POSTCOMM_L - text 40 w/domain
        fldmap_PostalCommNameL.addInputField(utransRoads, "USPS_PLACE")
        fldmap_PostalCommNameL.outputFieldSettyBetty('POSTCOMM_L')
        fieldmappings.addFieldMap(fldmap_PostalCommNameL)

        # POSTCOMM_R - text 40 w/domain
        fldmap_PostalCommNameR.addInputField(utransRoads, "USPS_PLACE")
        fldmap_PostalCommNameR.outputFieldSettyBetty('POSTCOMM_R')
        fieldmappings.addFieldMap(fldmap_PostalCommNameR)

        # ZIPCODE_L - text 5 w/domain
        fldmap_ZipCodeL.addInputField(utransRoads, "ZIPLEFT")
        fldmap_ZipCodeL.outputFieldSettyBetty('ZIPCODE_L')
        fieldmappings.addFieldMap(fldmap_ZipCodeL)

        # ZIPCODE_R - text 5 w/domain
        fldmap_ZipCodeR.addInputField(utransRoads, "ZIPRIGHT")
        fldmap_ZipCodeR.outputFieldSettyBetty('ZIPCODE_R')
        fieldmappings.addFieldMap(fldmap_ZipCodeR)

        # INCMUNI_L - text 100 w/domain
        fldmap_IncMuniL.addInputField(utransRoads, "L_CITY")
        fldmap_IncMuniL.outputFieldSettyBetty('INCMUNI_L')
        fieldmappings.addFieldMap(fldmap_IncMuniL)

        # INCMUNI_R - text 10 w/domain
        fldmap_IncMuniR.addInputField(utransRoads, "R_CITY")
        fldmap_IncMuniR.outputFieldSettyBetty('INCMUNI_R')
        fieldmappings.addFieldMap(fldmap_IncMuniR)


        # UNINCCOM_L - text 100

        # UNINCCOM_R - text 100

        # NBRHDCOM_L - text 100

        # NBRHDCOM_R - text 100

        # ER_CAD_ZONES - text

        # ESN_L - text 5

        # ESN_R - text 5

        # MSAGCOMM_L - text 30

        # MSAGCOMM_R - text 30

        # ONEWAY - text 2 w/domain

        # VERT_LEVEL - text 1 w/domain

        # SPEED_LIMIT - shortint w/domain
        fldmap_SpeedLimit.addInputField(utransRoads, "SPEED")
        fldmap_SpeedLimit.outputFieldSettyBetty('SPEED_LMT')
        fieldmappings.addFieldMap(fldmap_SpeedLimit)

        # ACCESSCODE - text 1 w/domain (i removed the domian b/c we have too many characters in utrans)
        fldmap_Access.addInputField(utransRoads, "ACCESS")
        fldmap_Access.outputFieldSettyBetty('ACCESSCODE')
        fieldmappings.addFieldMap(fldmap_Access)

        # DOT_HWYNAME - text 15
        fldmap_Dot_HwyName.addInputField(utransRoads, "HWYNAME")
        fldmap_Dot_HwyName.outputFieldSettyBetty('DOT_HWYNAM')
        fieldmappings.addFieldMap(fldmap_Dot_HwyName)

        # DOT_RTNAME - text 11

        # DOT_RTPART - text 3

        # DOT_F_MILE - float

        # DOT_T_MILE - float

        # DOT_FCLASS - text 20 w/domain
        fldmap_Dot_F_Class.addInputField(utransRoads, "DOT_FUNC")
        fldmap_Dot_F_Class.outputFieldSettyBetty('DOT_FCLASS')
        fieldmappings.addFieldMap(fldmap_Dot_F_Class)

        # DOT_SRFTYP - text 30 w/domain
        fldmap_Dot_SurfType.addInputField(utransRoads, "SURFTYPE")
        fldmap_Dot_SurfType.outputFieldSettyBetty('DOT_SRFTYP')
        fieldmappings.addFieldMap(fldmap_Dot_SurfType)

        # DOT_CLASS - text 1 w/domain

        # DOT_RDOWN - text 30

        # DOT_AADT - longint

        # DOT_AADTYR - text 4

        # BIKE_L - text 4 w/domain

        # BIKE_R - text 4 w/domain

        # BIKE_NOTES - text 50

        # BIKE_STATUS - text 1 w/domain

        # CUSTOMTAGS - text 1000

        # UNIQUE_ID - text 75

        # LOCAL_UNQID - text 20

        # ROADCL_UID - text 100

        # SOURCE - text 75

        # UPDATED - date
        fldmap_Updated.addInputField(utransRoads, "MODIFYDATE")
        fldmap_Updated.outputFieldSettyBetty('UPDATED')
        fieldmappings.addFieldMap(fldmap_Updated)

        # EFFECTIVE - date

        # EXPIRE - date

        print "Mapping Local Roads data to New Schema"
        print "Roads update started, please be patient..."
        arcpy.AddMessage("Mapping Local Roads data to New Schema")
        arcpy.AddMessage("Roads update Started, please be patient...")

        ## append the local data to county's local copy of the sgid schema
        arcpy.Append_management(utransRoads, newRoadsSchemaFGBpath, "NO_TEST", fieldmappings)

        print "Finished Appending Data using the FieldMapping"
        arcpy.AddMessage("Finished Appending Data using the FieldMapping")

        print "Finished executing LoadUtransIntoNewSchema.py script."
        arcpy.AddMessage("Finished executing LoadUtransIntoNewSchema.py script.")

    except IndexError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print "*** print_exception:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stdout)
        print "*** print_exc:"
        traceback.print_exc()
        print "*** format_exc, first and last line:"
        formatted_lines = traceback.format_exc().splitlines()
        print formatted_lines[0]
        print formatted_lines[-1]
        print "*** format_exception:"
        print repr(traceback.format_exception(exc_type, exc_value,
                                              exc_traceback))
        print "*** extract_tb:"
        print repr(traceback.extract_tb(exc_traceback))
        print "*** format_tb:"
        print "*** tb_lineno:", exc_traceback.tb_lineno
        #print e
        #global_exception_handler()



#def global_exception_handler(ex_cls, ex, tb):

#    #log = logging.getLogger('forklift')

#    #last_traceback = (traceback.extract_tb(tb))[-1]
#    #line_number = last_traceback[1]
#    #file_name = last_traceback[0].split(".")[0]

#    #log.error(('global error handler line: %s (%s)' % (line_number, file_name)))
#    #log.error(traceback.format_exception(ex_cls, ex, tb))
#    print "Exception in user code:"
#    traceback.print_exc(ex_cls, ex, tb)
#    traceback.format_exception(ex_cls, ex, tb)


#def _add_global_error_handler():
#    sys.excepthook = global_exception_handler





#def createCountyNameDictionary():
#    CountyNamesDictionary = {}




#def make_attribute_dict(fc, key_field, attr_list=['*']):
#    ''' Create a dictionary of feature class/table attributes.
#        Default of ['*'] for attr_list (instead of actual attribute names)
#        will create a dictionary of all attributes. '''
#    attr_dict = {}
#    fc_field_objects = arcpy.ListFields(fc)
#    fc_fields = [field.name for field in fc_field_objects if field.type != 'Geometry']
#    if attr_list == ['*']:
#        valid_fields = fc_fields
#    else:
#        valid_fields = [field for field in attr_list if field in fc_fields]
#    # Ensure that key_field is always the first field in the field list
#    cursor_fields = [key_field] + list(set(valid_fields) - set([key_field]))
#    with arcpy.da.SearchCursor(fc, cursor_fields) as cursor:
#        for row in cursor:
#            attr_dict[row[0]] = dict(zip(cursor.fields, row))
#    return attr_dict



# this method spatially assisgns the municipality boundary attributes in the roads feture class 
def assignMuniBoundariesSpatial():
    try:

        ## create a feature class of the two offset points, so we can make a feature layer to pass that into the select by location tool
        # check if points layer exists, delete if exists
        if arcpy.Exists(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts"):
            arcpy.Delete_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts")
        arcpy.CreateFeatureclass_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb","OffsetRoadSegPnts","POINT",None,None,None, arcpy.SpatialReference(26912))

        # add a few fields to the newly created feature class
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts", "RdSegOID", "TEXT", 20)
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts", "LeftRight", "TEXT", 20)
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts", "Muni", "TEXT", 50)


        ## create a new feature class to hold all the polygon values for spatial queries - this fc will be used with the identity tool and the new offset points
        # check if points layer exists, delete if exists
        if arcpy.Exists(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPolygons"):
            arcpy.Delete_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPolygons")
        arcpy.CreateFeatureclass_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb","IdentityPolygons","POLYGON",None,None,None, arcpy.SpatialReference(26912))

        # add a few fields to the newly created feature class
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts", "MUNI", "TEXT", 50)
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts", "ZIP", "TEXT", 50)
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts", "COUNTY", "TEXT", 50)
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts", "ADDR_SYSTEM", "TEXT", 50)


        ## calculate muni values for segments that are completely within a muni polygon (not on the edge so don't need to check both sides of the road for munis)
        #arcpy.MakeFeatureLayer_management(r"Database Connections\agrc@sgid@sgid.agrc.utah.gov.sde\SGID10.BOUNDARIES.Municipalities", "lyr_Muni")
        arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\MuniTest", "lyr_Muni")
        arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\RoadCenterlinesTest", "lyr_Roads")

        print "Begin assigning municipality boundaries that are completely contained within a municipality..."
        
        with arcpy.da.SearchCursor("lyr_Muni", ["SHORTDESC", "NAME", "OID@"]) as cursor:
            for row in cursor:
                #print row[0]
                print "MuniName: " + row[1]
                #print row[2]
#UNCOMMENTED                # select each municipality one at a time, and then select all the roads in that muni and calculate the Incorporated fields
#THESE                #arcpy.SelectLayerByAttribute_management("lyr_Muni", "NEW_SELECTION", "\"OBJECTID\" = " + str(row[2]))
#LINES                #arcpy.SelectLayerByLocation_management("lyr_Roads", "COMPLETELY_WITHIN", "lyr_Muni", "", "NEW_SELECTION")
#WHEN LIVE                #arcpy.CalculateField_management("lyr_Roads", "INCMUNI_L", "'{0}'".format(str(row[0])), "PYTHON_9.3", "")
        arcpy.Delete_management("lyr_Muni")
        arcpy.Delete_management("lyr_Roads")


        ## calculate muni values for segments that are within 33 feet of another muni polygon 
        arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\MuniTest", "lyr_Muni2")
        arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\RoadCenterlinesTest", "lyr_Roads2")

        print "Begin assigning municipality boundaries that are within 33 feet of a municipality..."

        with arcpy.da.SearchCursor("lyr_Muni2", ["SHORTDESC", "NAME", "OID@"]) as cursor2:
            for row2 in cursor2:
                print "next time through :" + row2[1]
                #select each municipality one at a time, and then select all the roads in that muni and calculate the Incorporated fields

                # make a feature layer for the current muni
                arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\MuniTest", "lyr_Muni_Current", "OBJECTID = " + str(row2[2]))
                
                # buffer the current muni to expand the boundary to 12 meters (40 feet)
                arcpy.Buffer_analysis("lyr_Muni_Current", r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\buffer" + str(row2[2]), 12, "OUTSIDE_ONLY", "ROUND", "NONE", "")

                # make feature layer from the buffered results
                arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\buffer" + str(row2[2]), "lyr_Muni_Cur_Buff")

                # select segments that are within the buffer
                arcpy.SelectLayerByLocation_management("lyr_Roads2", "INTERSECT", "lyr_Muni_Cur_Buff", "12", "NEW_SELECTION", "") #12 meters (about 40 feet)
                #arcpy.CalculateField_management("lyr_Roads2", "INCMUNI_L", "'{0}'".format(str(row2[1])), "PYTHON_9.3", "")

                # loop through all the segments that are within the buffer and spatially assign the right/left muni values
                with arcpy.da.SearchCursor("lyr_Roads2", ["OID@","SHAPE@", "INCMUNI_L", "INCMUNI_R"]) as cursorBuffIntersect:
                    for row3 in cursorBuffIntersect:
                        print "OID: " + str(row3[0])
                        
                        # get the first point on the polyline
                        roadSegFirstPoint = row3[1].firstPoint
                        pnt1Geom = arcpy.PointGeometry(roadSegFirstPoint, arcpy.SpatialReference(26912)) 
                        #print pnt1Geom

                        # get the last point on the polyline
                        roadSegLastPoint = row3[1].lastPoint
                        pnt2Geom = arcpy.PointGeometry(roadSegLastPoint, arcpy.SpatialReference(26912))
                        #print pnt2Geom
                
                        # get the midpoint of the polyline
                        roadSegMidPoint = row3[1].positionAlongLine(0.5, True)
                        #pntMidGeom = arcpy.PointGeometry(roadSegMidPoint, arcpy.SpatialReference(26912))

                        # get the angle between the first and last point on the polyline
                        roadSegAngleDistTo = pnt1Geom.angleAndDistanceTo(pnt2Geom)[0] # use [0] to only return the angle tuple, without that it would need two variables one for the angle and one for the distance
                        #segmentAngleRight = roadSegAngleDistTo + 90
                        #print segmentAngleRight

                        # create two new point based on the midpoint of the segment, and the angle of the polyline, and an offset value (a point each for right and left sides)
                        pntRightOffset = roadSegMidPoint.pointFromAngleAndDistance(roadSegAngleDistTo + 90, 10.06) #15.24 meters is 50 feet, 10.0584 meters is 33 feet
                        #print pntRightOffset.centroid
                        pntGeomRightOffset = arcpy.PointGeometry(pntRightOffset.centroid, arcpy.SpatialReference(26912))
                        #print pntGeomRightOffset.centroid

                        pntLeftOffset = roadSegMidPoint.pointFromAngleAndDistance(roadSegAngleDistTo - 90, 10.06) #15.24 meters is 50 feet, 10.0584 meters is 33 feet
                        #print pntLeftOffset.centroid
                        pntGeomLeftOffset = arcpy.PointGeometry(pntLeftOffset.centroid, arcpy.SpatialReference(26912))
                        #print pntGeomLeftOffset.centroid


                        # insert the new points into temp feature class
                        with arcpy.da.InsertCursor(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts", ["SHAPE@X", "SHAPE@Y", "LeftRight", "RdSegOID"]) as insertCurPnts:
                            row_values = [pntRightOffset.centroid.X, pntRightOffset.centroid.Y, "RIGHT", row3[0]]
                            insertCurPnts.insertRow(row_values)

                            row_values = [pntLeftOffset.centroid.X, pntLeftOffset.centroid.Y, "LEFT", row3[0]]
                            insertCurPnts.insertRow(row_values)



                        ## load polgons into the scratch dataset for polygon boundaries - used for the identity tool and the new offset points

                        



                        # create feature layer for LEFT muni to query                        
                        # make feature layer from offset points feature class
                        arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts", "lyr_OffsetPntLeft", "RdSegOID = '" + str(row3[0]) + "' and LeftRight = 'LEFT'")
                        # for both points, do spatial query to see what muni boundaries they fall within (intersect)
                        arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\MuniTest", "lyr_Muni_AllLeft")
                        #arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\PntLeftOffset", "lyr_PntLeft")
                        arcpy.SelectLayerByLocation_management("lyr_Muni_AllLeft", "INTERSECT","lyr_OffsetPntLeft", "", "NEW_SELECTION", "")
                        #arcpy.CalculateField_management("lyr_Roads2", "INCMUNI_L", "'{0}'".format(str(row4[0])), "PYTHON_9.3", "")
                        #arcpy.CopyFeatures_management('lyr_PntLeft', r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\PntLeft_2")
                        #arcpy.CopyFeatures_management('lyr_Muni_All', r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\MuniTest_2")

                        # create search cursor to get value from the queried muni layer
                        with arcpy.da.SearchCursor("lyr_Muni_AllLeft", ["SHORTDESC", "NAME", "OID@"]) as cursorMuniIntersetLeft:
                            for row4 in cursorMuniIntersetLeft:
                                print "Left: " + str(row4[0])
                                arcpy.CalculateField_management("lyr_Roads2", "INCMUNI_L", "'{0}'".format(str(row4[0])), "PYTHON_9.3", "")
                        
                        arcpy.Delete_management("lyr_Muni_AllLeft")
                        arcpy.Delete_management("lyr_OffsetPntLeft")
                        #arcpy.Delete_management("lyr_Roads2_left")




                        # create feature layer for RIGHT muni query
                        # make feature layer from offset points feature class
                        arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts", "lyr_OffsetPntRight", "RdSegOID = '" + str(row3[0]) + "' and LeftRight = 'RIGHT'")
                        arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\MuniTest", "lyr_Muni_AllRight")
                        #arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\PntRightOffset", "lyr_PntRight")
                        arcpy.SelectLayerByLocation_management("lyr_Muni_AllRight", "INTERSECT", "lyr_OffsetPntRight", "", "NEW_SELECTION", "")

                        # create search cursor to get value from the queried muni layer
                        with arcpy.da.SearchCursor("lyr_Muni_AllRight",["SHORTDESC", "NAME", "OID@"]) as cursorMuniIntersetRight:
                            for row5 in cursorMuniIntersetRight:
                                print "Right: " + str(row5[0])
                                arcpy.CalculateField_management("lyr_Roads2", "INCMUNI_R", "'{0}'".format(str(row5[0])), "PYTHON_9.3", "")
                        
                        arcpy.Delete_management("lyr_Muni_AllRight")
                        arcpy.Delete_management("lyr_OffsetPntRight")
                        #arcpy.Delete_management("lyr_Roads2_right")


                arcpy.Delete_management("lyr_Muni_Current")
                arcpy.Delete_management("lyr_Muni_Cur_Buff")
                arcpy.Delete_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\buffer" + str(row2[2]))




        ### get angle between first and last point of segment and then midpoint on segment line, offset 50 feet from midpoint based on angle to get a right and left point for select by location
        ##with arcpy.da.UpdateCursor(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\RoadCenterlinesTest", ["OID@","SHAPE@"]) as cursor:
        ##    for row in cursor:
        ##        print row
                
        ##        # get the first point on the polyline
        ##        roadSegFirstPoint = row[1].firstPoint
        ##        pnt1Geom = arcpy.PointGeometry(roadSegFirstPoint, arcpy.SpatialReference(26912)) 
        ##        print pnt1Geom

        ##        # get the last point on the polyline
        ##        roadSegLastPoint = row[1].lastPoint
        ##        pnt2Geom = arcpy.PointGeometry(roadSegLastPoint, arcpy.SpatialReference(26912))
        ##        print pnt2Geom
                
        ##        # get the midpoint of the polyline
        ##        roadSegMidPoint = row[1].positionAlongLine(0.5, True)
        ##        #pntMidGeom = arcpy.PointGeometry(roadSegMidPoint, arcpy.SpatialReference(26912))

        ##        # get the angle between the first and last point on the polyline
        ##        roadSegAngleDistTo = pnt1Geom.angleAndDistanceTo(pnt2Geom)[0] # use [0] to only return the angle tuple, without that it would need two variables one for the angle and one for the distance
        ##        #segmentAngleRight = roadSegAngleDistTo + 90
        ##        #print segmentAngleRight


        ##        # create a new point based on the midpoint and the angle of the polyline
        ##        pntRightOffset = roadSegMidPoint.pointFromAngleAndDistance(roadSegAngleDistTo + 90, 15.24) #15.24 meters is 50 feet
        ##        print pntRightOffset.centroid

        ##        pntLeftOffset = roadSegMidPoint.pointFromAngleAndDistance(roadSegAngleDistTo - 90, 15.24) #15.24 meters is 50 feet
        ##        print pntLeftOffset.centroid

        ##        insertCurPnts = arcpy.da.InsertCursor(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\LeftRightPoints", ["SHAPE@X", "SHAPE@Y", "Left", "Right", "SegOID"])
        ##        #myx,myy = pntRightOffset[0]
        ##        row_values = [pntRightOffset.centroid.X, pntRightOffset.centroid.Y, "", "Right", row[0]]
        ##        insertCurPnts.insertRow(row_values)

        ##        row_values = [pntLeftOffset.centroid.X, pntLeftOffset.centroid.Y, "Left", "", row[0]]
        ##        insertCurPnts.insertRow(row_values)

        ##        #insertCurPnts.insertRow(pntLeftOffset)

        ##        del insertCurPnts

                


    except IndexError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print "*** print_exception:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stdout)
        print "*** print_exc:"
        traceback.print_exc()
        print "*** format_exc, first and last line:"
        formatted_lines = traceback.format_exc().splitlines()
        print formatted_lines[0]
        print formatted_lines[-1]
        print "*** format_exception:"
        print repr(traceback.format_exception(exc_type, exc_value,
                                              exc_traceback))
        print "*** extract_tb:"
        print repr(traceback.extract_tb(exc_traceback))
        print "*** format_tb:"
        print repr(traceback.format_tb(exc_traceback))
        print "*** tb_lineno:", exc_traceback.tb_lineno





def createPolygonBoundaries():
    try:
        print "BEGIN creating polygon boundaries for spatial queries..."

        ## create a new feature class to hold all the polygon values for spatial queries - this fc will be used with the identity tool and the new offset points
        # check if polygon layer exists, delete if exists
        if arcpy.Exists(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPolygons"):
            arcpy.Delete_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPolygons")
        arcpy.CreateFeatureclass_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb","IdentityPolygons","POLYGON",None,None,None, arcpy.SpatialReference(26912))

        # add a few fields to the newly created feature class
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPolygons", "MUNI_NAME", "TEXT", 50)
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPolygons", "MUNI_SHORTDESC", "TEXT", 50)
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPolygons", "ZIP_NUM", "TEXT", 50)
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPolygons", "ZIP_NAME", "TEXT", 50)
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPolygons", "CNTY_NAME", "TEXT", 50)
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPolygons", "CNTY_COFIPS", "TEXT", 50)
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPolygons", "ADDR_SYS", "TEXT", 50)
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPolygons", "ADDR_QUAD", "TEXT", 50)
        
        # get reference to new polygon fc
        indentityPolys = r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPolygons"


        # check if intersected polygon layer exists, delete if exists
        if arcpy.Exists(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdPoly_Intersected"):
            arcpy.Delete_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdPoly_Intersected")
        
        ## MUNI
        ## append muni boundaries (NAME, SHORTDESC)
         # use field mapping to transfer the data over
        fieldmappings = arcpy.FieldMappings()

        # create a field map-variable for each field
        fldmap_MuniName = arcpy.FieldMap()
        fldmap_ShortDesc = arcpy.FieldMap()

        # Add all fields from the input feature class to the fieldmappings object. AddTable is the most efficient way.
        #muniPolys = r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\Muni_sample"
        muniPolys = r"Database Connections\agrc@sgid@sgid.agrc.utah.gov.sde\SGID10.BOUNDARIES.Municipalities"
        fieldmappings.addTable(muniPolys)

        # define field maps for each field based on field names
        # NAME
        fldmap_MuniName.addInputField(muniPolys, "NAME")
        fldmap_MuniName.outputFieldSettyBetty('MUNI_NAME')
        fieldmappings.addFieldMap(fldmap_MuniName)

        # SHORTDESC
        fldmap_ShortDesc.addInputField(muniPolys, "SHORTDESC")
        fldmap_ShortDesc.outputFieldSettyBetty('MUNI_SHORTDESC')
        fieldmappings.addFieldMap(fldmap_ShortDesc)

        # append the data
        arcpy.Append_management(muniPolys, indentityPolys, "NO_TEST", fieldmappings)

        ## ZIPCODES
        # append zipcodes boundaries (ZIP5, NAME)
        # use field mapping to transfer the data over
        fieldmappings = arcpy.FieldMappings()

        ## create a field map-variable for each field
        fldmap_Zip5 = arcpy.FieldMap()
        fldmap_ZipName = arcpy.FieldMap()

        # Add all fields from the input feature class to the fieldmappings object. AddTable is the most efficient way.
        #zipPolys = r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\ZipCodes_sample"
        zipPolys = r"Database Connections\agrc@sgid@sgid.agrc.utah.gov.sde\SGID10.BOUNDARIES.ZipCodes"
        fieldmappings.addTable(zipPolys)

        # define field maps for each field based on field names
        # ZIP5
        fldmap_Zip5.addInputField(zipPolys, "ZIP5")
        fldmap_Zip5.outputFieldSettyBetty('ZIP_NUM')
        fieldmappings.addFieldMap(fldmap_Zip5)

        # NAME
        fldmap_ZipName.addInputField(zipPolys, "NAME")
        fldmap_ZipName.outputFieldSettyBetty('ZIP_NAME')
        fieldmappings.addFieldMap(fldmap_ZipName)

        # append the data
        arcpy.Append_management(zipPolys, indentityPolys, "NO_TEST", fieldmappings)

        ## COUNTIES
        # append counties boundaries (NAME, FIPS_STR)
        # use field mapping to transfer the data over
        fieldmappings = arcpy.FieldMappings()

        ## create a field map-variable for each field in the new-schema-FGD roads feature class
        fldmap_CountyName = arcpy.FieldMap()
        fldmap_Cofips = arcpy.FieldMap()

        # Add all fields from the input feature class to the fieldmappings object. AddTable is the most efficient way.
        #countyPolys = r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\Counties_sample"
        countyPolys = r"Database Connections\agrc@sgid@sgid.agrc.utah.gov.sde\SGID10.BOUNDARIES.Counties"
        fieldmappings.addTable(countyPolys)

        # define field maps for each field based on field names
        # NAME
        fldmap_CountyName.addInputField(countyPolys, "NAME")
        fldmap_CountyName.outputFieldSettyBetty('CNTY_NAME')
        fieldmappings.addFieldMap(fldmap_CountyName)

        # FIPS_STR
        fldmap_Cofips.addInputField(countyPolys, "FIPS_STR")
        fldmap_Cofips.outputFieldSettyBetty('CNTY_COFIPS')
        fieldmappings.addFieldMap(fldmap_Cofips)

        # append the data
        arcpy.Append_management(countyPolys, indentityPolys, "NO_TEST", fieldmappings)

        ## ADDRESS SYSTEM
        # append address system boundaries (GRID_NAME, QUADRANT)
        # use field mapping to transfer the data over
        fieldmappings = arcpy.FieldMappings()

        ## create a field map-variable for each field in the new-schema-FGD roads feature class
        fldmap_GridName = arcpy.FieldMap()
        fldmap_QuadName = arcpy.FieldMap()

        # Add all fields from the input feature class to the fieldmappings object. AddTable is the most efficient way.
        #addrPolys = r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\AddrSys_sample"
        addrPolys = r"Database Connections\agrc@sgid@sgid.agrc.utah.gov.sde\SGID10.LOCATION.AddressSystemQuadrants"
        fieldmappings.addTable(addrPolys)

        # define field maps for each field based on field names
        # GRID_NAME
        fldmap_GridName.addInputField(addrPolys, "GRID_NAME")
        fldmap_GridName.outputFieldSettyBetty('ADDR_SYS')
        fieldmappings.addFieldMap(fldmap_GridName)

        # QUADRANT
        fldmap_QuadName.addInputField(addrPolys, "QUADRANT")
        fldmap_QuadName.outputFieldSettyBetty('ADDR_QUAD')
        fieldmappings.addFieldMap(fldmap_QuadName)

        # append the data
        arcpy.Append_management(addrPolys, indentityPolys, "NO_TEST", fieldmappings)


        ## intersect all boundaries together
        #inFeaturesIntersect = [muniPolys, zipPolys, countyPolys, addrPolys]
        #intersectOutput = r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdPoly_Intersected"
        #arcpy.Intersect_analysis([indentityPolys], intersectOutput, "", "", "INPUT")

        ## dissolve the intersected layer so we don't have overlapping polygons
        #arcpy.Dissolve_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdPoly_Intersected", r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdPoly_InterDissolve", ["MUNI_NAME", "MUNI_SHORTDESC", "ZIP_NUM", "ZIP_NAME", "CNTY_NAME", "CNTY_COFIPS", "ADDR_SYS", "ADDR_QUAD"])


        ## create buffers for all the edges
        print "FINISHED creating polygon boundaries for spatial queries."
    except IndexError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print "*** print_exception:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                    limit=2, file=sys.stdout)
        print "*** print_exc:"
        traceback.print_exc()
        print "*** format_exc, first and last line:"
        formatted_lines = traceback.format_exc().splitlines()
        print formatted_lines[0]
        print formatted_lines[-1]
        print "*** format_exception:"
        print repr(traceback.format_exception(exc_type, exc_value,
                                                exc_traceback))
        print "*** extract_tb:"
        print repr(traceback.extract_tb(exc_traceback))
        print "*** format_tb:"
        print repr(traceback.format_tb(exc_traceback))
        print "*** tb_lineno:", exc_traceback.tb_lineno










def runIdentityTool():
    try:
        print "BEGIN running identity tool..."
        ## Set local parameters
        inFeatures = r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts"
        idFeatures = r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPolygons"
        outFeatures = r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPnts"

        # Process: Use the Identity function
        arcpy.Identity_analysis (inFeatures, idFeatures, outFeatures)

        print "FINISHED running identity tool."
    except IndexError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print "*** print_exception:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                    limit=2, file=sys.stdout)
        print "*** print_exc:"
        traceback.print_exc()
        print "*** format_exc, first and last line:"
        formatted_lines = traceback.format_exc().splitlines()
        print formatted_lines[0]
        print formatted_lines[-1]
        print "*** format_exception:"
        print repr(traceback.format_exception(exc_type, exc_value,
                                                exc_traceback))
        print "*** extract_tb:"
        print repr(traceback.extract_tb(exc_traceback))
        print "*** format_tb:"
        print repr(traceback.format_tb(exc_traceback))
        print "*** tb_lineno:", exc_traceback.tb_lineno







def createOffsetPnts(WhereClauseRoads):
    try:
        print "BEGIN creating left/right offset points..."
        print strftime("%Y-%m-%d %H:%M:%S", gmtime())

        ## create a feature class of the two offset points, so we can make a feature layer to pass that into the select by location tool
        # check if points layer exists, delete if exists
        if arcpy.Exists(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts2"):
            arcpy.Delete_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts2")
        arcpy.CreateFeatureclass_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb","OffsetRoadSegPnts2","POINT",None,None,None, arcpy.SpatialReference(26912))

        # add a few fields to the newly created feature class
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts2", "RdSegOID", "LONG")
        arcpy.AddField_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts2", "LeftRight", "TEXT", 20)

        # check if we're creating a point for all segments or a subset (aka: maybe just recent edits)
        if WhereClauseRoads == "":
            arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\RoadCenterlines", "lyr_Roads_SCur")
        else:
            arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\RoadCenterlines", "lyr_Roads_SCur", WhereClauseRoads)

        # loop through the appropriate segments in the roads layer
        with arcpy.da.SearchCursor("lyr_Roads_SCur", ["OID@","SHAPE@"]) as cursor_roads:
            for row_roads in cursor_roads:
                print "Road Segment OID: " + str(row_roads[0])
                        
                # get the first point on the polyline
                #roadSegFirstPoint = row_roads[1].firstPoint
                pnt1Geom = arcpy.PointGeometry(row_roads[1].firstPoint, arcpy.SpatialReference(26912)) 

                # get the last point on the polyline
                #roadSegLastPoint = row_roads[1].lastPoint
                pnt2Geom = arcpy.PointGeometry(row_roads[1].lastPoint, arcpy.SpatialReference(26912))
                
                # get the midpoint of the polyline
                roadSegMidPoint = row_roads[1].positionAlongLine(0.5, True)
                pntMidGeom = arcpy.PointGeometry(roadSegMidPoint.centroid, arcpy.SpatialReference(26912))

                # get the angle between the first and last point on the polyline
                roadSegAngleDistTo = pnt1Geom.angleAndDistanceTo(pnt2Geom)[0] # use [0] to only return the angle tuple, without that it would need two variables one for the angle and one for the distance
                #segmentAngleRight = roadSegAngleDistTo + 90
                #print segmentAngleRight

                # create two new point based on the midpoint of the segment, and the angle of the polyline, and an offset value (a point each for right and left sides)
                pntRightOffset = pntMidGeom.pointFromAngleAndDistance(roadSegAngleDistTo + 90, 10.06) #15.24 meters is 50 feet, 10.0584 meters is 33 feet
                #print pntRightOffset.centroid
                pntGeomRightOffset = arcpy.PointGeometry(pntRightOffset.centroid, arcpy.SpatialReference(26912))
                #print pntGeomRightOffset.centroid

                pntLeftOffset = pntMidGeom.pointFromAngleAndDistance(roadSegAngleDistTo - 90, 10.06) #15.24 meters is 50 feet, 10.0584 meters is 33 feet
                #print pntLeftOffset.centroid
                pntGeomLeftOffset = arcpy.PointGeometry(pntLeftOffset.centroid, arcpy.SpatialReference(26912))
                #print pntGeomLeftOffset.centroid

                ## insert the new points into temp feature class
                with arcpy.da.InsertCursor(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\OffsetRoadSegPnts2", ["SHAPE@X", "SHAPE@Y", "LeftRight", "RdSegOID"]) as insertCurPnts:
                    row_values = [pntRightOffset.centroid.X, pntRightOffset.centroid.Y, "RIGHT", row_roads[0]]
                    insertCurPnts.insertRow(row_values)

                    row_values = [pntLeftOffset.centroid.X, pntLeftOffset.centroid.Y, "LEFT", row_roads[0]]
                    insertCurPnts.insertRow(row_values)

        # clean up resources and memory
        arcpy.Delete_management("lyr_Roads_SCur")

        print "FINISHED creating left/right offset points."
        print strftime("%Y-%m-%d %H:%M:%S", gmtime())
    except IndexError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print "*** print_exception:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                    limit=2, file=sys.stdout)
        print "*** print_exc:"
        traceback.print_exc()
        print "*** format_exc, first and last line:"
        formatted_lines = traceback.format_exc().splitlines()
        print formatted_lines[0]
        print formatted_lines[-1]
        print "*** format_exception:"
        print repr(traceback.format_exception(exc_type, exc_value,
                                                exc_traceback))
        print "*** extract_tb:"
        print repr(traceback.extract_tb(exc_traceback))
        print "*** format_tb:"
        print repr(traceback.format_tb(exc_traceback))
        print "*** tb_lineno:", exc_traceback.tb_lineno






def assignValuesToRoadsFromOffsetPnts(identityFieldNameForJoin, assignValuesFieldNameLeft, assignValuesFieldNameRight):
    try:
        # change this to first add duplicate fields in the roads dataset corisponding to the spatial asigned fields (aka: INCMUNI_L_SA, INCMUNI_R_SA) - added "_SA" for spatially assigned
        # then populate those fields so we can retain the originals
        print "Began processing assignValuesToRoadsFromOffsetPnts() for " + str(identityFieldNameForJoin) +" at: " + strftime("%Y-%m-%d %H:%M:%S", gmtime())

        ## check if spatial assignment fields exist (both left and right side fields)
        print "Check if spatial assignment fields exist..."        
        if (not FieldExist(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\RoadCenterlines", str(assignValuesFieldNameLeft) + "_SA")):
            # add the missing field
            arcpy.AddField_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\RoadCenterlines", str(assignValuesFieldNameLeft) + "_SA", "TEXT", 100)
        if (not FieldExist(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\RoadCenterlines", str(assignValuesFieldNameRight) + "_SA")):
            # add the missing field
            arcpy.AddField_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\RoadCenterlines", str(assignValuesFieldNameRight) + "_SA", "TEXT", 100)

        ## calculate all values in the spatial fields to empty string (to ensure a fresh start) (maybe do this with an update cursor to speed it up)
        #arcpy.CalculateField_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\RoadCenterlines", str(assignValuesFieldNameLeft) + "_SA", "", "PYTHON_9.3")
        #arcpy.CalculateField_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\RoadCenterlines", str(assignValuesFieldNameRight) + "_SA", "", "PYTHON_9.3")


        print "BEGIN assigning values to the spatial fields in the Roads feature class -- based on values in the offset points..."

        ## LEFT SIDE ##
        print "Began assigning left-side field values at: " + strftime("%Y-%m-%d %H:%M:%S", gmtime())
        # create a feature layer from identity points layer where point intersected... (muni, zipcodes, addrsystem, counties)
        arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\RoadCenterlines", "lyr_RoadsNewSchema")
        arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\RoadCenterlines", "lyr_RoadsNewSchema_")
        arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPnts", "Identity_Muni_Left", str(identityFieldNameForJoin) + " IS NOT NULL and LeftRight = 'LEFT'")

        # join the pnts to the roads segments
        arcpy.AddJoin_management("lyr_RoadsNewSchema", "OBJECTID", "Identity_Muni_Left", "RdSegOID", "KEEP_COMMON")

        with arcpy.da.SearchCursor("lyr_RoadsNewSchema", ["OID@", "IdentityPnts." + str(identityFieldNameForJoin)]) as cursor:
            for row in cursor:
                updateOID = ""
                updatedValue = ""
                updateOID = row[0]
                updatedValue = row[1]

                with arcpy.da.UpdateCursor("lyr_RoadsNewSchema_", [str(assignValuesFieldNameLeft) + "_SA"], "OBJECTID = " + str(updateOID)) as cursor2:
                    for row2 in cursor2:
                        row2[0] = updatedValue
                        cursor2.updateRow(row2)
                del cursor2
        del cursor

        print "Left Fields for " + str(identityFieldNameForJoin) + "  - Done!"
        arcpy.Delete_management("lyr_RoadsNewSchema")
        arcpy.Delete_management("lyr_RoadsNewSchema_")
        arcpy.Delete_management("Identity_Muni_Left")



        ## RIGHT SIDE ##
        print "Began assigning right-side field values at: " + strftime("%Y-%m-%d %H:%M:%S", gmtime())
        # create a feature layer from identity points layer where point intersected... (muni, zipcodes, addrsystem, counties)
        arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\RoadCenterlines", "lyr_RoadsNewSchema2")
        arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\CenterLineSchema20160906_143901.gdb\RoadCenterlines", "lyr_RoadsNewSchema_2")
        arcpy.MakeFeatureLayer_management(r"D:\SGID Roads New Schema\NewSchemaTesting.gdb\IdentityPnts", "Identity_Muni_Right", str(identityFieldNameForJoin) + " IS NOT NULL and LeftRight = 'RIGHT'")

        # join the pnts to the roads segments
        arcpy.AddJoin_management("lyr_RoadsNewSchema2", "OBJECTID", "Identity_Muni_Right", "RdSegOID", "KEEP_COMMON")
        #arcpy.JoinField_management("lyr_RoadsNewSchema2", "OBJECTID", "Identity_Muni_Right", "RdSegOID")

        with arcpy.da.SearchCursor("lyr_RoadsNewSchema2", ["OID@", "IdentityPnts." + str(identityFieldNameForJoin)]) as cursor_:
            for row_ in cursor_:
                updateOID2 = ""
                updatedValue2 = ""
                updateOID2 = row_[0]
                updatedValue2 = row_[1]

                with arcpy.da.UpdateCursor("lyr_RoadsNewSchema_2", [str(assignValuesFieldNameRight) + "_SA"], "OBJECTID = " + str(updateOID2)) as cursor2_:
                    for row2_ in cursor2_:
                        row2_[0] = updatedValue2
                        cursor2_.updateRow(row2_)
                del cursor2_
        del cursor_
        print "Right Fields for " + str(identityFieldNameForJoin) + " - Done!"
        arcpy.Delete_management("lyr_RoadsNewSchema2")
        arcpy.Delete_management("lyr_RoadsNewSchema_2")
        arcpy.Delete_management("Identity_Muni_Right")

        print "FINISHED assigning values to the spatial fields in the Roads feature class -- based on values in the offset points."
        print "Finished processing assignValuesToRoadsFromOffsetPnts() at: " + strftime("%Y-%m-%d %H:%M:%S", gmtime())    
    except IndexError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print "*** print_exception:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                    limit=2, file=sys.stdout)
        print "*** print_exc:"
        traceback.print_exc()
        print "*** format_exc, first and last line:"
        formatted_lines = traceback.format_exc().splitlines()
        print formatted_lines[0]
        print formatted_lines[-1]
        print "*** format_exception:"
        print repr(traceback.format_exception(exc_type, exc_value,
                                                exc_traceback))
        print "*** extract_tb:"
        print repr(traceback.extract_tb(exc_traceback))
        print "*** format_tb:"
        print repr(traceback.format_tb(exc_traceback))
        print "*** tb_lineno:", exc_traceback.tb_lineno



# this function checks if a field exists in the feature class
def FieldExist(featureclass, fieldname):
    fieldList = arcpy.ListFields(featureclass, fieldname)

    fieldCount = len(fieldList)

    if (fieldCount == 1):
        return True
    else:
        return False



################# My notes - things to change and make better #########################
# 1. bring in field values from utrans that we're going to spatially assign as uppercase - because when i do the compare if the case is different they don't match
# 2. create a function to see if the nre schema roads already exists 
#   -if so, get the most recent mod date and use that to delete all recordsfrom that then date
#   -then, get all records from that date and forward (from utrans) and append into the new schema  
# 3. do update cursor on spatial fields only when the existing value doesn't match the new spatially-aquired value 
#   this should make the update cursor faster, as it only has to process where they don't match
#
################# My notes #########################


## CALL THE FUNCTIONS AS NEEDED ##
main(utransRoads, newRoadsSchemaFGBpath)

#createPolygonBoundaries()

##roadsWhereClause = "OBJECTID > 32767" # you could pass in only recent edits 
#roadsWhereClause = ""
#createOffsetPnts(roadsWhereClause)

#runIdentityTool()

### spatially assign incorporated municipality left/right fields
#identityFieldNameForJoin = "MUNI_SHORTDESC"
#assignValuesFieldNameLeft = "INCMUNI_L"
#assignValuesFieldNameRight = "INCMUNI_R"
#assignValuesToRoadsFromOffsetPnts(identityFieldNameForJoin, assignValuesFieldNameLeft, assignValuesFieldNameRight)

## spatially assign zipcode left/right number fields
#identityFieldNameForJoin = "ZIP_NUM"
#assignValuesFieldNameLeft = "ZIPCODE_L"
#assignValuesFieldNameRight = "ZIPCODE_R"
#assignValuesToRoadsFromOffsetPnts(identityFieldNameForJoin, assignValuesFieldNameLeft, assignValuesFieldNameRight)

## spatially assign postal community name left/right fields
#identityFieldNameForJoin = "ZIP_NAME"
#assignValuesFieldNameLeft = "POSTCOMM_L"
#assignValuesFieldNameRight = "POSTCOMM_R"
#assignValuesToRoadsFromOffsetPnts(identityFieldNameForJoin, assignValuesFieldNameLeft, assignValuesFieldNameRight)

## spatially assign county name (cofips) left/right fields
#identityFieldNameForJoin = "CNTY_COFIPS"
#assignValuesFieldNameLeft = "COUNTY_L"
#assignValuesFieldNameRight = "COUNTY_R"
#assignValuesToRoadsFromOffsetPnts(identityFieldNameForJoin, assignValuesFieldNameLeft, assignValuesFieldNameRight)

## spatially assign address system left/right fields
#identityFieldNameForJoin = "ADDR_SYS"
#assignValuesFieldNameLeft = "ADDRSYS_L"
#assignValuesFieldNameRight = "ADDRSYS_R"
#assignValuesToRoadsFromOffsetPnts(identityFieldNameForJoin, assignValuesFieldNameLeft, assignValuesFieldNameRight)

## spatially assign address quad field
#identityFieldNameForJoin = "ADDR_QUAD"
#assignValuesFieldNameLeft = "ADDRSYS_QUAD_L"
#assignValuesFieldNameRight = "ADDRSYS_QUAD_R"
#assignValuesToRoadsFromOffsetPnts(identityFieldNameForJoin, assignValuesFieldNameLeft, assignValuesFieldNameRight)