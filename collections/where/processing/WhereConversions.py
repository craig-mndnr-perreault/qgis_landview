import json, urllib, urllib2, time, math

PLS_TOWNSHIP_URL = 'http://arcgis.intranet.mndnr.dnr.state.mn.us/arcgis/rest/services/landview_tools/mndnr_twnshp/MapServer/0/query'
PLS_SECTION_URL = 'http://arcgis.intranet.mndnr.dnr.state.mn.us/arcgis/rest/services/landview_tools/mndnr_pls/MapServer/5/query'
PLS_40_URL = 'http://arcgis.intranet.mndnr.dnr.state.mn.us/arcgis/rest/services/landview_tools/mndnr_pls/MapServer/10/query'
COUNTY_URL = 'http://arcgis.intranet.mndnr.dnr.state.mn.us/arcgis/rest/services/quicklayers/mndnr_adminfeatures/MapServer/80/query'
MCD_URL = 'http://arcgis.intranet.mndnr.dnr.state.mn.us/arcgis/rest/services/quicklayers/mndnr_adminfeatures/MapServer/83/query'
USNG_URL = 'http://arcgis.intranet.mndnr.dnr.state.mn.us/arcgis/rest/services/quicklayers/mndnr_tile_schemes/MapServer/4/query'

MajorAxis = 6378137.0
MinorAxis = 6356752.3
Ecc = (MajorAxis * MajorAxis - MinorAxis * MinorAxis) / (MajorAxis * MajorAxis)
ecc2 = Ecc / (1.0 - Ecc)
K0 = 0.9996
E4 = Ecc * Ecc
E6 = Ecc * E4

MajorAxis_27 = 6378206.4
MinorAxis_27 = 6356583.8
Ecc_27 = (MajorAxis_27 * MajorAxis_27 - MinorAxis_27 * MinorAxis_27) / (MajorAxis_27 * MajorAxis_27)
ecc2_27 = Ecc_27 / (1.0 - Ecc_27)
E4_27 = Ecc_27 * Ecc_27
E6_27 = Ecc_27 * E4_27

def UTM2DD(args):
    UTM2LatLongDD(args)
def DD2UTM(args):
    LatLongDD2UTM(args)
def DD2DM(args):
    LatLongDD2LatLongDM(args)
def DD2DMS(args):
    LatLongDD2LatLongDMS(args)
def DM2DD(args):
    LatLongDM2LatLongDD(args)
def DMS2DD(args):
    LatLongDMS2LatLongDD(args)
    
def UTM2County(args):
    data = []  # Blank Dictionary to populate with return
    coords = str(str(args['UtmX']) + "," + str(args['UtmY']))  #Build coords from UtmX and UtmY
    countyParams = urllib.urlencode({
        'f': "pjson",
        'sr': "26915",
        'returnGeometry': "false",
        'outFields': "COUN, CTY_NAME",
    	'geometryType': "esriGeometryPoint",
        'spatialRel': "esriSpatialRelIntersects",
    	'geometry': coords
    })
    countyData = json.loads(urllib2.urlopen(COUNTY_URL, countyParams).read())
    try:
        countyReturn =  countyData['features']
        for feature in countyReturn:
            data.append(feature['attributes'])
            args['County'] = (data[0].get('COUN'))
            args['CountyName'] = (data[0].get('CTY_NAME'))
    except:
            args['County'] = -1
            args['CountyName'] = "No County Data features"
    UTM2MCD(args)         
                       
def UTM2MCD(args):
    #Query MCD data 
    data = []  # Blank Dictionary to populate with return
    coords = str(str(args['UtmX']) + "," + str(args['UtmY']))  #Build coords from UtmX and UtmY
    
    mcdParams = urllib.urlencode({
        'f': "pjson",
        'sr': "26915",
        'returnGeometry': "false",
        'outFields': "MCDNAME2",
    	'geometryType': "esriGeometryPoint",
        'spatialRel': "esriSpatialRelIntersects",
    	'geometry': coords
    })
    mcdData = json.loads(urllib2.urlopen(MCD_URL, mcdParams).read())
    try:
        mcdReturn = mcdData['features']
        for feature in mcdReturn:
            data.append(feature['attributes'])
            args['MCD'] = data[0].get('MCDNAME2')        
    except:
        args['MCD'] = "No MCD Data features"

def UTM2USNG(args):
    data = []  # Blank Dictionary to populate with return
    coords = str(str(args['UtmX']) + "," + str(args['UtmY']))  #Build coords from UtmX and UtmY
    usngParams = urllib.urlencode({
        'f': "pjson",
        'sr': "26915",
        'returnGeometry': "false",
        'outFields': "GRID1MIL, GRID100K",
    	'geometryType': "esriGeometryPoint",
        'spatialRel': "esriSpatialRelIntersects",
    	'geometry': coords
    })
    usngData = json.loads(urllib2.urlopen(USNG_URL, usngParams).read())
    try:
        usngReturn =  usngData['features']
        for feature in usngReturn:
            data.append(feature['attributes'])
            args['USNG1'] = (data[0].get('GRID1MIL')).upper()
            args['USNG2'] = (data[0].get('GRID100K')).upper()        
    except:
        args['USNG'] = "No USNG Data features"
        
    if args['USNG1'].startswith("14"):
        args14 =  {'Zone':15, 'UtmX':args['UtmX'], 'UtmY':args['UtmY'], 'LatDD':0.0, 'LongDD':0.0}
        UTM2LatLongDD(args14);
        args14['Zone'] = 14
        LatLongDD2UTM(args14);
        args['USNG3'] = int(round(args14['UtmX'] % 100000))
        args['USNG4'] = int(round(args14['UtmY'] % 100000))
    elif args['USNG1'].startswith("15"):
        args['USNG3'] = int(round(args['UtmX'] % 100000))
        args['USNG4'] = int(round(args['UtmY'] % 100000))
    elif args['USNG1'].startswith("16"):
        args16 =  {'Zone':15, 'UtmX':args['UtmX'], 'UtmY':args['UtmY'], 'LatDD':0.0, 'LongDD':0.0}
        UTM2LatLongDD(args16);
        args16['Zone'] = 16
        LatLongDD2UTM(args16);
        args['USNG3'] = int(round(args16['UtmX'] % 100000))
        args['USNG4'] = int(round(args16['UtmY'] % 100000))

    args['USNG'] = args['USNG1'] + args['USNG2'] + str(args['USNG3']) + str(args['USNG4'])
    
def UTM2PLS(args):  
    data = []  # Blank Dictionary to populate with return
    coords = str(str(args['UtmX']) + "," + str(args['UtmY']))  #Build coords from UtmX and UtmY

    pls40Params = urllib.urlencode({
        'f': "pjson",
        'sr': "26915",
        'returnGeometry': "false",
        'outFields': "COUN, TOWN, RANG, RDIR, SECT, FORT, GLOT",
    	'geometryType': "esriGeometryPoint",
        'spatialRel': "esriSpatialRelIntersects",
    	'geometry': coords
    })
    #Query PLS40 data and load as JSON object
    Pls40Data = json.loads(urllib2.urlopen(PLS_40_URL, pls40Params).read())
    #PLS40 Atributes
    try:
        PLS40Return =  Pls40Data['features']
        for feature in PLS40Return:
            data.append(feature['attributes'])
            args['County'] = data[0].get('COUN')
            args['Twp'] = data[0].get('TOWN')
            args['Rng'] = data[0].get('RANG')
            args['Dir'] = data[0].get('RDIR')
            args['Sec'] = data[0].get('SECT')
            args['FortyNbr'] = data[0].get('FORT')
            args['Glot'] = data[0].get('GLOT')        
    except:
        Coords['Message'] = "Failed: No Pls40 Data features"

    if (args['Twp'] < 1) & (args['pls_slop'] > 0):
        getPLSSectionFromClosestPolygon(args)
    GlotMatch(args)
    County2CountyName(args)
    FortyNbr2Forties(args)
    UTM2MCD(args)
            
def getPLSSectionFromClosestPolygon(args):
    tF = args['pls_slop']
    envelope = str(str(args['UtmX'] - tF) + "," + str(args['UtmY'] - tF) + "," + str(args['UtmX'] + tF) + "," + str(args['UtmY'] + tF))

    plsParams = urllib.urlencode({
            'f': "pjson",
            'sr': "26915",
            'returnGeometry': "true",
            'outFields': "TOWN,RANG,RDIR,SECT,COUN",
            'geometryType': "esriGeometryEnvelope",
            'spatialRel': "esriSpatialRelIntersects",
            'geometry': envelope
        })
        
    plsData = json.loads(urllib2.urlopen(PLS_SECTION_URL, plsParams).read())
    closestSoFar = 99999
    try:
        plsReturn =  plsData['features']
        for feature in plsReturn:
            theGeometry = []
            data= []
            theGeometry.append(feature['geometry'])
            data.append(feature['attributes'])
            for line in theGeometry:
                for path in line['rings']:
                    for point in path:
                        d = math.sqrt((args['UtmX'] - point[0]) ** 2 + (args['UtmY'] - point[1]) ** 2)
                        if (d < closestSoFar):
                            args['Twp'] = data[0].get('TOWN')
                            args['Rng'] = data[0].get('RANG')
                            args['Dir'] = data[0].get('RDIR')
                            args['Sec'] = data[0].get('SECT')
                            args['County'] = data[0].get('COUN')
                            closestSoFar = d                            
##                            print 'closestSoFar=' + str(closestSoFar)
    except:
        args['Message'] = "Failed getting PLS Section within " + str(tF) + " meters"
    try:
        if (len(plsReturn) < 1):
            args['Message'] = "No PLS Section features within tolerance of " + str(tF) + " meters"
    except:
            args['Message'] = "Failed to execute query on: " + PLS_SECTION_URL

def PLS2UTM(args):
    if args['Sec'] == 0:
        PLS2UTM_Township(args)
    elif (args['FortyNbr'] == 0) & (args['Forty1'] == '') & (args['Glot'] == 0):
        PLS2UTM_Section(args)
    elif args['Glot'] > 0:
        PLS2UTM_Glot(args)        
    else:
        PLS2UTM_40(args)
            
def PLS2UTM_Township(args):
    theMinX = 999999
    theMinY = 9999999
    theMaxX = 0
    theMaxY = 0
    if args['County'] == 0:
        args['theQuery'] = "TOWN = " + str(args['Twp']) + " AND RANG = " + str(args['Rng']) + " AND RDIR = " + str(args['Dir'])
    else:
        args['theQuery'] = "COUN = " + str(args['County']) + " AND TOWN = " + str(args['Twp']) + " AND RANG = " + str(args['Rng']) + " AND RDIR = " + str(args['Dir'])

    plsParams = urllib.urlencode({
        'f': "pjson",
        'sr': "26915",
        'returnGeometry': "true",
        'geometryPrecision': "2",
        'outFields': "COUN, TWPRNGDIR",
        'where': args['theQuery']
    })
    plsData = json.loads(urllib2.urlopen(PLS_TOWNSHIP_URL, plsParams).read())
    try:
        plsReturn =  plsData['features']
        for feature in plsReturn:
            data= []
            data.append(feature['attributes'])
            args['plsCounties'].append(str(data[0].get('COUN')))
##            args['plsCounties'] = str(data[0].get('COUN'))
            
            plsGeom = feature['geometry'] 
            for rings in plsGeom['rings']:  #  get the extent of polygon to calculate center X Y
                for ring in rings:
                    if ring[0] < theMinX:
                        theMinX = ring[0]
                    if ring[1] < theMinY:
                        theMinY = ring[1]
                    if ring[0] > theMaxX:
                        theMaxX = ring[0]
                    if ring[1] > theMaxY:
                        theMaxY = ring[1]
        args['UtmX'] = (theMinX + theMaxX) / 2
        args['UtmY'] = (theMinY + theMaxY) / 2
        args['Message'] = "PLS from PLS_TOWNSHIP_URL"        
        args['plsGeom'] = plsGeom
    except:
        PLS2UTM_Section(args)

def PLS2UTM_Section(args):
    theMinX = 999999
    theMinY = 9999999
    theMaxX = 0
    theMaxY = 0
    if (args['theQuery'] == ""):
        args['theQuery'] = "TOWN = " + str(args['Twp']) + " AND RANG = " + str(args['Rng']) + " AND RDIR = " + str(args['Dir']) + " AND SECT = " + str(args['Sec'])
    plsParams = urllib.urlencode({
        'f': "pjson",
        'sr': "26915",
        'returnGeometry': "true",
        'geometryPrecision': "2",
        'outFields': "TWPRNGSEC",
        'where': args['theQuery']    
    })
    plsData = json.loads(urllib2.urlopen(PLS_SECTION_URL, plsParams).read())
    try:
        plsReturn =  plsData['features']       
        for feature in plsReturn:
            plsGeom = feature['geometry'] 
            for rings in plsGeom['rings']:  #  get the extent of polygon to calculate center X Y
                for ring in rings:
                    if ring[0] < theMinX:
                        theMinX = ring[0]
                    if ring[1] < theMinY:
                        theMinY = ring[1]
                    if ring[0] > theMaxX:
                        theMaxX = ring[0]
                    if ring[1] > theMaxY:
                        theMaxY = ring[1]
##        args['MCD'] = "theMinX=" + str(theMinX) + "theMaxX=" + str(theMaxX) + "theMinY=" + str(theMinY) + "theMaxY=" + str(theMaxY)                    
        args['UtmX'] = (theMinX + theMaxX) / 2
        args['UtmY'] = (theMinY + theMaxY) / 2
        args['Message'] = "PLS from PLS_SECTION_URL"
        args['plsGeom'] = plsGeom
    except:
        args['Message'] = "Not in Minnesota"
        args['UtmX'] = 0
        args['UtmY'] = 0
##        PLS2UTM_40(args)

def PLS2UTM_Glot(args):
    theMinX = 999999
    theMinY = 9999999
    theMaxX = 0
    theMaxY = 0
    args['theQuery'] = "TOWN = " + str(args['Twp']) + " AND RANG = " + str(args['Rng']) + " AND RDIR = " + str(args['Dir']) + " AND SECT = " + str(args['Sec']) + " AND GLOT = " + str(args['Glot'])
    plsParams = urllib.urlencode({
        'f': "pjson",
        'sr': "26915",
        'returnGeometry': "true",
        'geometryPrecision': "2",
        'outFields': "GEOFORT",
        'where': args['theQuery']
    })
    plsData = json.loads(urllib2.urlopen(PLS_40_URL, plsParams).read())
    try:
        plsReturn =  plsData['features']       
        for feature in plsReturn:
            plsGeom = feature['geometry'] 
            for rings in plsGeom['rings']:  #  get the extent of polygon to calculate center X Y
                for ring in rings:
                    if ring[0] < theMinX:
                        theMinX = ring[0]
                    if ring[1] < theMinY:
                        theMinY = ring[1]
                    if ring[0] > theMaxX:
                        theMaxX = ring[0]
                    if ring[1] > theMaxY:
                        theMaxY = ring[1]
        args['UtmX'] = (theMinX + theMaxX) / 2
        args['UtmY'] = (theMinY + theMaxY) / 2
        args['Message'] = "PLS from PLS_40_URL"
        args['plsGeom'] = plsGeom
    except:
        args['UtmX'] = -1
        args['UtmY'] = -1
        args['Message'] = "No PLS at: " + args['theQuery']
        
def PLS2UTM_40(args):
    theMinX = 999999
    theMinY = 9999999
    theMaxX = 0
    theMaxY = 0
    if (args['theQuery'] == ""):
        if (args['FortyNbr'] == 0) & (args['Forty1'] != ''):
##            if (args['Forty1'] = 'NE': f1 = 1
##            elif args['Forty1'] = 'NW': f1 = 2
##            args['FortyNbr'] = 22
            f1 = 0
            f2 = 0
            if (args['Forty1'].upper() == 'NE'): f2 = 1
            elif (args['Forty1'].upper() == 'NW'): f2 = 2
            elif (args['Forty1'].upper() == 'SW'): f2 = 3
            elif (args['Forty1'].upper() == 'SE'): f2 = 4

            if (args['Forty2'].upper() == 'NE'): f1 = 10
            elif (args['Forty2'].upper() == 'NW'): f1 = 20
            elif (args['Forty2'].upper() == 'SW'): f1 = 30
            elif (args['Forty2'].upper() == 'SE'): f1 = 40
            args['FortyNbr'] = f2 + f1
        args['theQuery'] = "TOWN = " + str(args['Twp']) + " AND RANG = " + str(args['Rng']) + " AND RDIR = " + str(args['Dir']) + " AND SECT = " + str(args['Sec']) + " AND FORT = " + str(args['FortyNbr'])

##        if args['Glot'] > 0:
##            args['theQuery'] = args['theQuery'] + " AND GLOT = " + str(args['Glot'])
    plsParams = urllib.urlencode({
        'f': "pjson",
        'sr': "26915",
        'returnGeometry': "true",
        'geometryPrecision': "2",
        'outFields': "GEOFORT",
        'where': args['theQuery']
    })
    plsData = json.loads(urllib2.urlopen(PLS_40_URL, plsParams).read())
    try:
        plsReturn =  plsData['features']       
        for feature in plsReturn:
            plsGeom = feature['geometry'] 
            for rings in plsGeom['rings']:  #  get the extent of polygon to calculate center X Y
                for ring in rings:
                    if ring[0] < theMinX:
                        theMinX = ring[0]
                    if ring[1] < theMinY:
                        theMinY = ring[1]
                    if ring[0] > theMaxX:
                        theMaxX = ring[0]
                    if ring[1] > theMaxY:
                        theMaxY = ring[1]
        args['UtmX'] = (theMinX + theMaxX) / 2
        args['UtmY'] = (theMinY + theMaxY) / 2
        args['Message'] = "PLS from PLS_40_URL"
        args['plsGeom'] = plsGeom
    except:
        args['UtmX'] = -1
        args['UtmY'] = -1
        args['Message'] = "No PLS at: " + args['theQuery']


def meridianDist(LatRad):
    ##  ****   Computes the meridian distance for the Clarke 1866 Spheroid   ****
    con1 = MajorAxis * (1 - Ecc / 4 - 3 * E4 / 64 - 5 * E6 / 256)
    con2 = -MajorAxis * (3 * Ecc / 8 + 3 * E4 / 32 + 45 * E6 / 1024)
    con3 = MajorAxis * (15 * E4 / 256 + 45 * E6 / 1024)
    con4 = -MajorAxis * 35 * E6 / 3072
    return con1 * LatRad + con2 * math.sin(LatRad * 2) + con3 * math.sin(LatRad * 4) + con4 * math.sin(LatRad * 6)


def meridianDist27(LatRad):
    ##  ****   Computes the meridian distance for the GRS-80 Spheroid. See equation 3-22, USGS Professional Paper 1395      ****
    con1 = MajorAxis_27 * (1 - Ecc_27 / 4 - 3 * E4_27 / 64 - 5 * E6_27 / 256)
    con2 = -MajorAxis_27 * (3 * Ecc_27 / 8 + 3 * E4_27 / 32 + 45 * E6_27 / 1024)
    con3 = MajorAxis_27 * (15 * E4_27 / 256 + 45 * E6_27 / 1024)
    con4 = -MajorAxis_27 * 35 * E6_27 / 3072
    return con1 * LatRad + con2 * math.sin(LatRad * 2) + con3 * math.sin(LatRad * 4) + con4 * math.sin(LatRad * 6)


def GetTheRotation(p1X, p1Y, p2X, p2Y):
    quadrant = 0
    Direction = 0
    wx = 0.0
    wy = 0.0
    try:
        wx = p2X - p1X
        wy = p2Y - p1Y
        if ((wx < 0) & (wy <= 0)):
            quadrant = 3
        elif ((wx > 0) & (wy < 0)):
            quadrant = 4
        elif ((wx > 0) & (wy >= 0)):
            quadrant = 1
        elif ((wx < 0) & (wy > 0)):
            quadrant = 2

        if quadrant == 0:
            if (wy < 0):
                Direction = 360
            else:
                Direction = 180
        elif quadrant == 1:
            Direction = 270 + int(math.atan(wy / wx) * 57.2958)
        elif quadrant == 2:
            Direction = 90 - int(abs(math.atan(wy / wx) * 57.2958))
        elif quadrant == 3:
            Direction = 90 + int(math.atan(wy / wx) * 57.2958)
        elif quadrant == 4:
            Direction = 270 + int(math.atan(wy / wx) * 57.2958)

        if ((wx == 0) & (wy > 0)):
            Direction = 0
        if ((wx == 0) & (wy < 0)):
            Direction = 180
        if ((wx < 0) & (wy == 0)):
            Direction = 90
        if ((wx > 0) & (wy == 0)):
            Direction = 270

        if (abs(Direction) < 0.5):
            Direction = 360

        return Direction
    except:
        return 0


def LatLongDD2UTM(args):  ## UtmX and UTMY are computed in meters
    LatDD = args['LatDD']
    LongDD = args['LongDD']

    latsin = latTan = latCos = N = t2 = c = a = m = LatRad = LongRad = temp5 = temp6 = temp7 = temp8 = temp9 = temp11 = centMerRad = 0.0
    centMerRad = -((30 - args['Zone']) * 6 + 3) * math.pi / 180
    LatRad = LatDD * math.pi / 180
    LongRad = LongDD * math.pi / 180
    latsin = math.sin(LatRad)
    latCos = math.cos(LatRad)
    latTan = latsin / latCos
    N = MajorAxis / math.sqrt(1.0 - Ecc * math.pow(latsin, 2))
    t2 = math.pow(latTan, 2)
    c = ecc2 * math.pow(latCos, 2)
    a = latCos * (LongRad - centMerRad)
    m = meridianDist(LatRad)

    temp5 = 1.0 - t2 + c
    temp6 = 5.0 - 18.0 * t2 + math.pow(t2, 2) + 72.0 * c - 58.0 * ecc2
    temp11 = math.pow(a, 5)

    utmx = K0 * N * (a + (temp5 * math.pow(a, 3)) / 6.0 + temp6 * temp11 / 120.0) + 500000.0

    temp7 = (5.0 - t2 + 9.0 * c + 4.0 * math.pow(a, 2)) * math.pow(a, 4) / 24.0
    temp8 = 61.0 - 58.0 * t2 + math.pow(t2, 2) + 600.0 * c - 330.0 * ecc2
    temp9 = temp11 * a / 720.0

    utmy = K0 * (m + N * latTan * (math.pow(a, 2) / 2.0 + temp7 + temp8 * temp9))

    args['UtmX'] = utmx
    args['UtmY'] = utmy


def LatLongDD2UTM_NAD27(args):  ## UtmX and UTMY are computed in meters
    LatDD = args['LatDD']
    LongDD = args['LongDD']

    latsin = latTan = latCos = N = t2 = c = a = m = LatRad = LongRad = temp5 = temp6 = temp7 = temp8 = temp9 = temp11 = centMerRad = 0.0
    centMerRad = -((30 - args['Zone']) * 6 + 3) * math.pi / 180
    LatRad = LatDD * math.pi / 180
    LongRad = LongDD * math.pi / 180
    latsin = math.sin(LatRad)
    latCos = math.cos(LatRad)
    latTan = latsin / latCos
    N = MajorAxis_27 / math.sqrt(1.0 - Ecc_27 * math.pow(latsin, 2))
    t2 = math.pow(latTan, 2)
    c = ecc2_27 * math.pow(latCos, 2)
    a = latCos * (LongRad - centMerRad)
    m = meridianDist27(LatRad)

    temp5 = 1.0 - t2 + c
    temp6 = 5.0 - 18.0 * t2 + math.pow(t2, 2) + 72.0 * c - 58.0 * ecc2_27
    temp11 = math.pow(a, 5)

    utmx = K0 * N * (a + (temp5 * math.pow(a, 3)) / 6.0 + temp6 * temp11 / 120.0) + 500000.0

    temp7 = (5.0 - t2 + 9.0 * c + 4.0 * math.pow(c, 2) * math.pow(a, 4)) / 24.0
    temp8 = 61.0 - 58.0 * t2 + math.pow(t2, 2) + 600.0 * c - 330.0 * ecc2_27
    temp9 = temp11 * a / 720.0

    utmy = K0 * (m + N * latTan * (math.pow(a, 2) / 2.0 + temp7 + temp8 * temp9))
    args['UtmX'] = utmx
    args['UtmY'] = utmy


def UTM2LatLongDD(args):  ##    UtmX and UtmY must be in meters
    utmx = float(args['UtmX'])
    utmy = float(args['UtmY'])
    first = True
    ecc1 = e12 = e13 = e14 = m = um = temp8 = temp9 = latrad1 = latsin1 = latcos1 = latTan1 = n1 = centMerRad = 0.0
    t2 = c1 = r1 = temp20 = D1 = D2 = D3 = D4 = D5 = D6 = t12 = c12 = temp1 = temp2 = temp4 = temp5 = temp6 = 0.0

    centMerRad = -((30 - args['Zone']) * 6 + 3) * math.pi / 180
    if first:
        temp1 = math.sqrt(1.0 - Ecc)
        ecc1 = (1.0 - temp1) / (1.0 + temp1)
        e12 = ecc1 * ecc1
        e13 = ecc1 * e12
        e14 = e12 * e12
        first = False

    utmx = utmx - 500000.0

    m = utmy / K0
    um = m / (MajorAxis * (1.0 - (Ecc / 4.0) - 3.0 * (E4 / 64.0) - 5.0 * (E6 / 256.0)))

    temp8 = (1.5 * ecc1) - (27.0 / 32.0) * e13
    temp9 = ((21.0 / 16.0) * e12) - ((55.0 / 32.0) * e14)

    latrad1 = um + temp8 * math.sin(2 * um) + temp9 * math.sin(4 * um) + (151.0 * e13 / 96.0) * math.sin(6 * um)

    latsin1 = math.sin(latrad1)
    latcos1 = math.cos(latrad1)
    latTan1 = latsin1 / latcos1
    n1 = MajorAxis / math.sqrt(1.0 - Ecc * math.pow(latsin1, 2))
    t2 = math.pow(latTan1, 2)
    c1 = ecc2 * math.pow(latcos1, 2)

    temp20 = (1.0 - Ecc * math.pow(latsin1, 2))
    r1 = MajorAxis * (1.0 - Ecc) / math.sqrt(math.pow(temp20, 3))

    D1 = utmx / (n1 * K0)
    D2 = math.pow(D1, 2)
    D3 = D1 * D2
    D4 = math.pow(D2, 2)
    D5 = D1 * D4
    D6 = math.pow(D3, 2)

    t12 = math.pow(t2, 2)
    c12 = math.pow(c1, 2)

    temp1 = n1 * latTan1 / r1
    temp2 = 5.0 + 3.0 * t2 + 10.0 * c1 - 4.0 * c12 - 9.0 * ecc2
    temp4 = 61.0 + 90.0 * t2 + 298.0 * c1 + 45.0 * t12 - 252.0 * ecc2 - 3.0 * c12
    temp5 = (1.0 + 2.0 * t2 + c1) * D3 / 6.0
    temp6 = 5.0 - 2.0 * c1 + 28.0 * t2 - 3.0 * c12 + 8.0 * ecc2 + 24.0 * t12

    args['LatDD'] = (latrad1 - (temp1) * (D2 / 2.0 - temp2 * (D4 / 24.0) + temp4 * D6 / 720.0)) * 180 / math.pi
    args['LongDD'] = (centMerRad + (D1 - temp5 + temp6 * D5 / 120.0) / latcos1) * 180 / math.pi
    utmx = utmx + 500000.0


##public void UTM2LatLongDD_NAD27(int zone, utmx, utmy, ref LatDD, ref LongDD)
##//    UtmX and UtmY must be in meters
##{
##    bool first = True
##    ecc1 = 0.0
##    e12 = 0.0
##    e13 = 0.0
##    e14 = 0.0
##    m = 0.0
##    um = 0.0
##    temp8 = 0.0
##    temp9 = 0.0
##    latrad1 = 0.0
##    latsin1 = 0.0
##    latcos1 = 0.0
##    latTan1 = 0.0
##    n1 = 0.0
##    centMerRad = 0.0
##    t2 = 0.0
##    c1 = 0.0
##    r1 = 0.0
##    temp20 = 0.0
##    D1 = 0.0
##    D2 = 0.0
##    D3 = 0.0
##    D4 = 0.0
##    D5 = 0.0
##    D6 = 0.0
##    t12 = 0.0
##    c12 = 0.0
##    temp1 = 0.0
##    temp2 = 0.0
##    temp4 = 0.0
##    temp5 = 0.0
##    temp6 = 0.0
##
##    centMerRad = -((30 - zone) * 6 + 3) *  math.pi / 180
##    if (first == True)
##    {
##        temp1 = math.sqrt(1.0 - Ecc_27)
##        ecc1 = (1.0 - temp1) / (1.0 + temp1)
##        e12 = ecc1 * ecc1
##        e13 = ecc1 * e12
##        e14 = e12 * e12
##        first = False
##    }
##    utmx = utmx - 500000.0
##
##    m = utmy / K0
##    um = m / (MajorAxis_27 * (1.0 - (Ecc_27 / 4.0) - 3.0 * (E4_27 / 64.0) - 5.0 * (E6_27 / 256.0)))
##
##    temp8 = (1.5 * ecc1) - (27.0 / 32.0) * e13
##    temp9 = ((21.0 / 16.0) * e12) - ((55.0 / 32.0) * e14)
##
##    latrad1 = um + temp8 * math.sin(2 * um) + temp9 * math.sin(4 * um) + (151.0 * e13 / 96.0) * math.sin(6 * um)
##
##    latsin1 = math.sin(latrad1)
##    latcos1 = math.cos(latrad1)
##    latTan1 = latsin1 / latcos1
##    n1 = MajorAxis_27 / math.sqrt(1.0 - Ecc_27 * CSq(latsin1))
##    t2 = CSq(latTan1)
##    c1 = ecc2 * CSq(latcos1)
##
##    temp20 = (1.0 - Ecc * CSq(latsin1))
##    r1 = MajorAxis * (1.0 - Ecc) / math.sqrt(CSq(temp20) * temp20)
##
##    D1 = utmx / (n1 * K0)
##    D2 = CSq(D1)
##    D3 = D1 * D2
##    D4 = CSq(D2)
##    D5 = D1 * D4
##    D6 = CSq(D3)
##
##    t12 = CSq(t2)
##    c12 = CSq(c1)
##
##    temp1 = n1 * latTan1 / r1
##    temp2 = 5.0 + 3.0 * t2 + 10.0 * c1 - 4.0 * c12 - 9.0 * ecc2_27
##    temp4 = 61.0 + 90.0 * t2 + 298.0 * c1 + 45.0 * t12 - 252.0 * ecc2_27 - 3.0 * c12
##    temp5 = (1.0 + 2.0 * t2 + c1) * D3 / 6.0
##    temp6 = 5.0 - 2.0 * c1 + 28.0 * t2 - 3.0 * c12 + 8.0 * ecc2_27 + 24.0 * t12
##
##    LatDD = (latrad1 - (temp1) * (D2 / 2.0 - temp2 * (D4 / 24.0) + temp4 * D6 / 720.0)) * 180 /  math.pi
##    LongDD = (centMerRad + (D1 - temp5 + temp6 * D5 / 120.0) / latcos1) * 180 /  math.pi
##    utmx = utmx + 500000.0
def LatLongDD2LatLongDM(args):
    args['LatDmDeg'] = int(math.floor(args['LatDD']));
    args['LatDmMin'] = (args['LatDD'] - args['LatDmDeg']) * 60;
    args['LongDmDeg'] = int(math.floor(abs(args['LongDD'])));
    args['LongDmMin'] = abs(args['LongDD'] + args['LongDmDeg']) * 60;


def LatLongDM2LatLongDD(args):
    args['LatDD'] = args['LatDmDeg'] + args['LatDmMin'] / 60;
    args['LongDD'] = (args['LongDmDeg'] + (args['LongDmMin'] / 60)) * -1;


def LatLongDD2LatLongDMS(args):
    LatDD = args['LatDD']
    LongDD = args['LongDD']
    t1 = 0.0
    try:
        LatDeg = LatMin = LatSec = LongDeg = LongMin = LongSec = 0
        t1 = abs(LatDD)
        LatDeg = int(math.floor(t1))
        t1 = t1 - LatDeg
        t1 = t1 * 60
        LatMin = int(math.floor(t1))
        t1 = t1 - LatMin
        LatSec = t1 * 60
        if (LatSec >= 60):
            LatSec = LatSec - 60
            LatMin = LatMin + 1
        if (LatMin >= 60):
            LatMin = LatMin - 60
            LatDeg = LatDeg + 1
        t1 = abs(LongDD)
        LongDeg = int(math.floor(t1))
        t1 = t1 - LongDeg
        t1 = t1 * 60
        LongMin = int(math.floor(t1))
        t1 = t1 - LongMin
        LongSec = t1 * 60
        if (LongSec >= 60):
            LongSec = LongSec - 60
            LongMin = LongMin + 1
        if (LongMin >= 60):
            LongMin = LongMin - 60
            LongDeg = LongDeg + 1

        args['LatDeg'] = LatDeg
        args['LatMin'] = LatMin
        args['LatSec'] = LatSec
        args['LongDeg'] = LongDeg
        args['LongMin'] = LongMin
        args['LongSec'] = LongSec
    except:
        Coords['Message'] = "Failed: in LatLongDD2LatLongDMS"


def LatLongDMS2LatLongDD(args):
    args['LatDD'] = (args['LatDeg'] + (float(args['LatMin']) / 60) + (args['LatSec'] / 3600))
    args['LongDD'] = (args['LongDeg'] + (float(args['LongMin']) / 60) + (args['LongSec'] / 3600))
    if (args['LongDD'] > 0):
        args['LongDD'] = args['LongDD'] * -1.0


def GlotMatch(args):
    lTwp = ""
    lRng = ""
    lSec = ""
    l40 = ""
    lGlot = ""
    tmpTxt = ""
    try:
        if (args['Twp'] < 100):
            lTwp = "0"
        if (args['Rng'] < 10):
            lRng = "0"
        if (args['Sec'] < 10):
            lSec = "0"
        if (args['FortyNbr'] < 10):
            l40 = "0"
        if (args['Glot'] < 10):
            lGlot = "0"

        tmpTxt = str(args['County']) + lTwp + str(args['Twp']) + str(args['Dir']) + lRng + str(
            args['Rng']) + lSec + str(args['Sec']) + l40 + str(args['FortyNbr']) + lGlot + str(args['Glot'])
        tmpTxt.replace(" ", "")

        args['GlotMatch'] = tmpTxt
    except:
        args['GlotMatch'] = "?"


def FortyNbr2Forties(args):
    forty1 = ""
    forty2 = ""
    theFortyNbr = args['FortyNbr']
    if (theFortyNbr < 9):  ## Quarter and Half Section
        if theFortyNbr == 1:
            forty1 = "NE"
        elif theFortyNbr == 2:
            forty1 = "NW"
        elif theFortyNbr == 3:
            forty1 = "SW"
        elif theFortyNbr == 4:
            forty1 = "SE"
        elif theFortyNbr == 5:
            forty1 = "N"
        elif theFortyNbr == 6:
            forty1 = "W"
        elif theFortyNbr == 7:
            forty1 = "S"
        elif theFortyNbr == 8:
            forty1 = "E"
    else:
        ll = math.floor(theFortyNbr / 10)
        rr = math.fmod(theFortyNbr, 10)
        if ((ll > 0) & (ll < 5) & (rr > 0) & (rr < 5)):
            if rr == 1:
                forty1 = "NE"
            elif rr == 2:
                forty1 = "NW"
            elif rr == 3:
                forty1 = "SW"
            elif rr == 4:
                forty1 = "SE"

            if ll == 1:
                forty2 = "NE"
            elif ll == 2:
                forty2 = "NW"
            elif ll == 3:
                forty2 = "SW"
            elif ll == 4:
                forty2 = "SE"
        else:
            forty1 = "";
            forty2 = "";

    args['Forty1'] = forty1
    args['Forty2'] = forty2


def County2CountyName(args):
    countyNames = [" ", "Aitkin", "Anoka", "Becker", "Beltrami", "Benton", "Big Stone", "Blue Earth", "Brown",
                   "Carlton", "Carver", "Cass", "Chippewa", "Chisago", "Clay", "Clearwater", "Cook", "Cottonwood",
                   "Crow Wing", "Dakota", "Dodge", "Douglas", "Faribault"]
    countyNames.extend(
        ["Fillmore", "Freeborn", "Goodhue", "Grant", "Hennepin", "Houston", "Hubbard", "Isanti", "Itasca", "Jackson",
         "Kanabec", "Kandiyohi", "Kittson", "Koochiching", "Lac Qui Parle", "Lake", "Lake of the Woods", "Le Sueur",
         "Lincoln", "Lyon"])
    countyNames.extend(
        ["McLeod", "Mahnomen", "Marshall", "Martin", "Meeker", "Mille Lacs", "Morrison", "Mower", "Murray", "Nicollet",
         "Nobles", "Norman", "Olmsted", "Otter Tail", "Pennington", "Pine", "Pipestone", "Polk", "Pope", "Ramsey",
         "Red Lake", "Redwood"])
    countyNames.extend(
        ["Renville", "Rice", "Rock", "Roseau", "St. Louis", "Scott", "Sherburne", "Sibley", "Stearns", "Steele",
         "Stevens", "Swift", "Todd", "Traverse", "Wabasha", "Wadena", "Waseca", "Washington", "Watonwan", "Wilkin",
         "Winona", "Wright", "Yellow Medicine"])
    try:
        if ((args['County'] >= 0) & (args['County'] < 88)):
            args['CountyName'] = countyNames[args['County']]
        else:
            args['CountyName'] = ""
    except:
        args['CountyName'] = ""


def USNG2UTM(args):
    args['UtmX'] = 0
    args['UtmY'] = 0
    tmpX = 0
    tmpY = 0
    if ((args['USNG1'].strip() != "") & (args['USNG2'].strip() != "") & (args['USNG3'] != 0) & (args['USNG4'] != 0)):
        TextX = str(args['USNG3'])
        while (len(TextX) < 5):
            TextX = "0" + TextX
        if (len(TextX) > 5):
            TextX = TextX[:5]
        USNG3 = int(TextX)
        # --------------------------------------------------------
        TextY = str(args['USNG4'])
        while (len(TextY) < 5):
            TextY = "0" + TextY
        if (len(TextY) > 5):
            TextY = TextY[:5]
        USNG4 = int(TextY)
        # --------------------------------------------------------
        TextGZD = args['USNG1'].strip().upper()
        Text100k = args['USNG2'].strip().upper()
        theZone = 0
        theFirstLetter = ""
        theSecondLetter = ""
        if (len(Text100k) > 1):
            theFirstLetter = Text100k[0]
            theSecondLetter = Text100k[1]
        try:
            theZone = int(TextGZD[:2])
        except:
            theZone = 0

        if theZone == 14:
            if theFirstLetter == "P":
                tmpX = 600000 + float(TextX)
            elif theFirstLetter == "Q":
                tmpX = 700000 + float(TextX)

            if theSecondLetter == "P":
                tmpY = 4800000 + float(TextY)
            elif theSecondLetter == "Q":
                tmpY = 4900000 + float(TextY)
            elif theSecondLetter == "R":
                tmpY = 5000000 + float(TextY)
            elif theSecondLetter == "S":
                tmpY = 5100000 + float(TextY)
            elif theSecondLetter == "T":
                tmpY = 5200000 + float(TextY)
            elif theSecondLetter == "U":
                tmpY = 5300000 + float(TextY)
            elif theSecondLetter == "V":
                tmpY = 5400000 + float(TextY)
            args14 = {'Zone': 14, 'UtmX': tmpX, 'UtmY': tmpY, 'LatDD': 0.0, 'LongDD': 0.0}
            UTM2LatLongDD(args14)
            args['LatDD'] = args14['LatDD']
            args['LongDD'] = args14['LongDD']
            LatLongDD2UTM(args)

        elif theZone == 15:
            if theFirstLetter == "T":
                utmX = 200000 + float(TextX)
            elif theFirstLetter == "U":
                utmX = 300000 + float(TextX)
            elif theFirstLetter == "V":
                utmX = 400000 + float(TextX)
            elif theFirstLetter == "W":
                utmX = 500000 + float(TextX)
            elif theFirstLetter == "X":
                utmX = 600000 + float(TextX)
            elif theFirstLetter == "Y":
                utmX = 700000 + float(TextX)

            if theSecondLetter == "J":
                utmY = 4800000 + float(TextY)
            elif theSecondLetter == "K":
                utmY = 4900000 + float(TextY)
            elif theSecondLetter == "L":
                utmY = 5000000 + float(TextY)
            elif theSecondLetter == "M":
                utmY = 5100000 + float(TextY)
            elif theSecondLetter == "N":
                utmY = 5200000 + float(TextY)
            elif theSecondLetter == "P":
                utmY = 5300000 + float(TextY)
            elif theSecondLetter == "Q":
                utmY = 5400000 + float(TextY)

            args['UtmX'] = utmX
            args['UtmY'] = utmY

        elif theZone == 16:
            if theFirstLetter == "B":
                tmpX = 200000 + float(TextX)
            elif theFirstLetter == "C":
                tmpX = 300000 + float(TextX)

            if theSecondLetter == "T":
                tmpY = 5200000 + float(TextY)
            elif theSecondLetter == "U":
                tmpY = 5300000 + float(TextY)

            args16 = {'Zone': 16, 'UtmX': tmpX, 'UtmY': tmpY, 'LatDD': 0.0, 'LongDD': 0.0}
            UTM2LatLongDD(args16)
            args['LatDD'] = args16['LatDD']
            args['LongDD'] = args16['LongDD']
            LatLongDD2UTM(args)

        else:  # theZone was not 14,15, or 16
            args['UtmX'] = 0
            args['UtmY'] = 0

    if (args['UtmX'] < 1):
        args['Message'] = "USNG Coordinates Not in Minnesota"

def ParseCoordinates(Coords):
    theText = Coords['PointText']

    try:
        ##Try to get Utm or LatLong Decimal Degrees out of theText
        clipText = " "
        aLen = len(theText)
        aChar = ' '
        for I in range(0, aLen):  ## Replace non numbers with spaces (except .)
            if (((theText[I] < '0') or (theText[I] > '9')) and (theText[I] != '.')):
                clipText = clipText + " "
            else:
                clipText = clipText + theText[I]

        words = clipText.split(' ')
        ##        print words

        theMinX = 130000
        theMinY = 4799000
        theMaxX = 772000
        theMaxY = 5488000

        tmpX = 0.0
        tmpY = 0.0
        DMSDLat = 0
        DMSMLat = 0
        DMSSLat = 0.0
        DMSDLong = 0
        DMSMLong = 0
        DMSSLong = 0.0
        DMDLat = 0
        DMMLat = 0.0
        DMDLong = 0
        DMMLong = 0.0
        tmpLat = 0.0
        tmpLong = 0.0
        X = 0
        tmpDbl = 0.0
        N = 0
        wordArray = []
        for word in words:
            if (len(word) > 0):
                wordArray.append(word)
                N = N + 1

        I = 0
        while (I < N):
            tmpDbl = float(wordArray[I])
            if ((tmpDbl > theMinX) and (tmpDbl < theMaxX)):
                tmpX = tmpDbl
            if ((tmpDbl > theMinY) and (tmpDbl < theMaxY)):
                tmpY = tmpDbl
            if ((tmpDbl > 42) and (tmpDbl < 50)):
                ##                print "Lat we have dm or dms or dd"
                tmpLat = tmpDbl
                if (tmpDbl < 0):
                    tmpDbl = tmpDbl * -1
                X = int(tmpDbl)
                if (((tmpDbl - float(X)) == 0) & (N > 2)):
                    tmpLat = 0
                    ##                    print "we have dms or dm"
                    tmpDbl = float(wordArray[I + 1])
                    X = int(tmpDbl)
                    ##                    print ('Xx=' , X, ' tmpDbl - float(X)=', tmpDbl - float(X))
                    if ((tmpDbl - float(X)) == 0):
                        ##                        print "we are at DMS for sure"
                        tmpDbl = float(wordArray[I + 2])
                        if ((tmpDbl > 0) and (tmpDbl < 60)):
                            ##                            print "Lat good dms"
                            DMSDLat = int(wordArray[I])
                            DMSMLat = int(wordArray[I + 1])
                            DMSSLat = float(wordArray[I + 2])
                            I = I + 2
                    else:
                        if ((tmpDbl > 0) and (tmpDbl < 60)):
                            ##                            print "Lat good dm"
                            DMDLat = int(wordArray[I])
                            DMMLat = float(wordArray[I + 1])
                            I = I + 1

            if ((tmpDbl > 88) and (tmpDbl < 98)):
                ##                print "Long we have dm or dms or dd"
                tmpLong = tmpDbl
                if (tmpDbl < 0):
                    tmpDbl = tmpDbl * -1
                X = int(tmpDbl)
                if (((tmpDbl - float(X)) == 0) & (N > 2)):
                    tmpLong = 0
                    tmpDbl = float(wordArray[I + 1])
                    X = int(tmpDbl)
                    if ((tmpDbl - float(X)) == 0):
                        ##                        print "Long we have DMS"
                        tmpDbl = float(wordArray[I + 2])
                        if ((tmpDbl > 0) and (tmpDbl < 60)):
                            ##                            print "Long good dms"
                            DMSDLong = int(wordArray[I])
                            DMSMLong = int(wordArray[I + 1])
                            DMSSLong = float(wordArray[I + 2])
                            I = I + 2
                    else:
                        if ((tmpDbl > 0) and (tmpDbl < 60)):
                            ##                            print "Long good dm"
                            DMDLong = int(wordArray[I])
                            DMMLong = float(wordArray[I + 1])
                            I = I + 1

            I = I + 1

        if ((tmpX > 0) and (tmpY > 0)):
            Coords['UtmX'] = tmpX
            Coords['UtmY'] = tmpY
            Coords['PointTextType'] = "UTM"

        elif ((tmpLat > 0) and (tmpLong > 0)):
            if (tmpLong > 0):
                tmpLong = tmpLong * -1
            Coords['LatDD'] = tmpLat
            Coords['LongDD'] = tmpLong
            Coords['PointTextType'] = "DD"

        elif ((DMDLat > 0) and (DMDLong > 0) and (DMMLong > 0) and (DMMLat > 0)):
            Coords['LatDmDeg'] = DMDLat
            Coords['LatDmMin'] = DMMLat
            Coords['LongDmDeg'] = DMDLong
            Coords['LongDmMin'] = DMMLong
            Coords['PointTextType'] = "DM"

        elif ((DMSDLat > 0) and (DMSDLong > 0)):
            Coords['LatDeg'] = DMSDLat
            Coords['LatMin'] = DMSMLat
            Coords['LatSec'] = DMSSLat
            Coords['LongDeg'] = DMSDLong
            Coords['LongMin'] = DMSMLong
            Coords['LongSec'] = DMSSLong
            Coords['PointTextType'] = "DMS"

    except:
        Coords['Message'] = "Failed: getting coordinates from: " + theText

    if (Coords['PointTextType'] == ""):
        Coords['Message'] = "Error: Could not get coordinates from: " + theText