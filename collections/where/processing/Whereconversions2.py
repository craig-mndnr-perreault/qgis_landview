import math

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

def LatLongDD2UTM(args):      ## UtmX and UTMY are computed in meters
    LatDD = args['LatDD']
    LongDD = args['LongDD']

    latsin = latTan = latCos = N = t2 = c = a = m = LatRad = LongRad = temp5 = temp6 = temp7 = temp8 = temp9 = temp11 = centMerRad = 0.0
    centMerRad = -((30 - args['Zone']) * 6 + 3) *  math.pi / 180
    LatRad = LatDD *  math.pi / 180
    LongRad = LongDD *  math.pi / 180
    latsin = math.sin(LatRad)
    latCos = math.cos(LatRad)
    latTan = latsin / latCos
    N = MajorAxis / math.sqrt(1.0 - Ecc * math.pow(latsin,2))
    t2 = math.pow(latTan, 2)
    c = ecc2 * math.pow(latCos,2)
    a = latCos * (LongRad - centMerRad)
    m = meridianDist(LatRad)

    temp5 = 1.0 - t2 + c
    temp6 = 5.0 - 18.0 * t2 + math.pow(t2,2) + 72.0 * c - 58.0 * ecc2
    temp11 =  math.pow(a,5)

    utmx = K0 * N * (a + (temp5 *  math.pow(a,3)) / 6.0 + temp6 * temp11 / 120.0) + 500000.0

    temp7 = (5.0 - t2 + 9.0 * c + 4.0 *  math.pow(a,2)) *  math.pow(a,4) / 24.0
    temp8 = 61.0 - 58.0 * t2 +  math.pow(t2,2) + 600.0 * c - 330.0 * ecc2
    temp9 = temp11 * a / 720.0

    utmy = K0 * (m + N * latTan * (math.pow(a,2) / 2.0 + temp7 + temp8 * temp9))

    args['UtmX'] = utmx
    args['UtmY'] = utmy

def LatLongDD2UTM_NAD27(args):      ## UtmX and UTMY are computed in meters
    LatDD = args['LatDD']
    LongDD = args['LongDD']
    
    latsin = latTan = latCos = N = t2 = c = a = m = LatRad = LongRad = temp5 = temp6 = temp7 = temp8 = temp9 = temp11 = centMerRad = 0.0
    centMerRad = -((30 - args['Zone']) * 6 + 3) *  math.pi / 180
    LatRad = LatDD *  math.pi / 180
    LongRad = LongDD *  math.pi / 180
    latsin = math.sin(LatRad)
    latCos = math.cos(LatRad)
    latTan = latsin / latCos
    N = MajorAxis_27 / math.sqrt(1.0 - Ecc_27 * math.pow(latsin,2))
    t2 = math.pow(latTan,2)
    c = ecc2_27 * math.pow(latCos,2)
    a = latCos * (LongRad - centMerRad)
    m = meridianDist27(LatRad)

    temp5 = 1.0 - t2 + c
    temp6 = 5.0 - 18.0 * t2 + math.pow(t2,2) + 72.0 * c - 58.0 * ecc2_27
    temp11 = math.pow(a,5)

    utmx = K0 * N * (a + (temp5 * math.pow(a,3)) / 6.0 + temp6 * temp11 / 120.0) + 500000.0

    temp7 = (5.0 - t2 + 9.0 * c + 4.0 * math.pow(c,2) * math.pow(a,4)) / 24.0
    temp8 = 61.0 - 58.0 * t2 + math.pow(t2,2) + 600.0 * c - 330.0 * ecc2_27
    temp9 = temp11 * a / 720.0

    utmy = K0 * (m + N * latTan * (math.pow(a,2) / 2.0 + temp7 + temp8 * temp9))
    args['UtmX'] = utmx
    args['UtmY'] = utmy

def UTM2LatLongDD(args):    ##    UtmX and UtmY must be in meters
    utmx = args['UtmX']
    utmy = args['UtmY']
    first = True
    ecc1 = e12 = e13 = e14 = m = um = temp8 = temp9 = latrad1 = latsin1 = latcos1 = latTan1 = n1 = centMerRad = 0.0
    t2 = c1 = r1 = temp20 = D1 = D2 = D3 = D4 = D5 = D6 = t12 = c12 = temp1 = temp2 = temp4 = temp5 = temp6 = 0.0

    centMerRad = -((30 - args['Zone']) * 6 + 3) *  math.pi / 180
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
    n1 = MajorAxis / math.sqrt(1.0 - Ecc * math.pow(latsin1,2))
    t2 = math.pow(latTan1,2)
    c1 = ecc2 * math.pow(latcos1,2)

    temp20 = (1.0 - Ecc * math.pow(latsin1,2))
    r1 = MajorAxis * (1.0 - Ecc) / math.sqrt(math.pow(temp20,3))

    D1 = utmx / (n1 * K0)
    D2 = math.pow(D1,2)
    D3 = D1 * D2
    D4 = math.pow(D2,2)
    D5 = D1 * D4
    D6 = math.pow(D3,2)

    t12 = math.pow(t2,2)
    c12 = math.pow(c1,2)

    temp1 = n1 * latTan1 / r1
    temp2 = 5.0 + 3.0 * t2 + 10.0 * c1 - 4.0 * c12 - 9.0 * ecc2
    temp4 = 61.0 + 90.0 * t2 + 298.0 * c1 + 45.0 * t12 - 252.0 * ecc2 - 3.0 * c12
    temp5 = (1.0 + 2.0 * t2 + c1) * D3 / 6.0
    temp6 = 5.0 - 2.0 * c1 + 28.0 * t2 - 3.0 * c12 + 8.0 * ecc2 + 24.0 * t12
  
    args['LatDD'] = (latrad1 - (temp1) * (D2 / 2.0 - temp2 * (D4 / 24.0) + temp4 * D6 / 720.0)) * 180 /  math.pi
    args['LongDD'] = (centMerRad + (D1 - temp5 + temp6 * D5 / 120.0) / latcos1) * 180 /  math.pi
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

        tmpTxt = str(args['County']) + lTwp + str(args['Twp']) + str(args['Dir']) + lRng + str(args['Rng']) + lSec + str(args['Sec']) + l40 + str(args['FortyNbr']) + lGlot + str(args['Glot'])
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
    countyNames = [" ","Aitkin","Anoka","Becker","Beltrami","Benton","Big Stone","Blue Earth","Brown","Carlton","Carver","Cass","Chippewa","Chisago","Clay","Clearwater","Cook","Cottonwood","Crow Wing","Dakota","Dodge","Douglas","Faribault"]
    countyNames.extend(["Fillmore","Freeborn","Goodhue","Grant","Hennepin","Houston","Hubbard","Isanti","Itasca","Jackson","Kanabec","Kandiyohi","Kittson","Koochiching","Lac Qui Parle","Lake","Lake of the Woods","Le Sueur","Lincoln","Lyon"])
    countyNames.extend(["McLeod","Mahnomen","Marshall","Martin","Meeker","Mille Lacs","Morrison","Mower","Murray","Nicollet","Nobles","Norman","Olmsted","Otter Tail","Pennington","Pine","Pipestone","Polk","Pope","Ramsey","Red Lake","Redwood"])
    countyNames.extend(["Renville","Rice","Rock","Roseau","St. Louis","Scott","Sherburne","Sibley","Stearns","Steele","Stevens","Swift","Todd","Traverse","Wabasha","Wadena","Waseca","Washington","Watonwan","Wilkin","Winona","Wright","Yellow Medicine"])
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
        #--------------------------------------------------------
        TextY = str(args['USNG4'])
        while (len(TextY) < 5):
            TextY = "0" + TextY
        if (len(TextY) > 5):
            TextY = TextY[:5]
        USNG4 = int(TextY)
        #--------------------------------------------------------
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
            args14 =  {'Zone':14, 'UtmX':tmpX, 'UtmY':tmpY, 'LatDD':0.0, 'LongDD':0.0}
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

            args16 =  {'Zone':16, 'UtmX':tmpX, 'UtmY':tmpY, 'LatDD':0.0, 'LongDD':0.0}
            UTM2LatLongDD(args16)
            args['LatDD'] = args16['LatDD']
            args['LongDD'] = args16['LongDD']
            LatLongDD2UTM(args)

        else:   # theZone was not 14,15, or 16
            args['UtmX'] = 0
            args['UtmY'] = 0
            
    if (args['UtmX'] < 1):
        args['Message'] = "USNG Coordinates Not in Minnesota"

        
