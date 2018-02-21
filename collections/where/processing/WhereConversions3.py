import math

def ParseCoordinates(Coords):

    theText = Coords['PointText']
    
    try:
    ##Try to get Utm or LatLong Decimal Degrees out of theText
        clipText = " "
        aLen = len(theText)
        aChar = ' '
        for I in range(0, aLen):   ## Replace non numbers with spaces (except .)
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

