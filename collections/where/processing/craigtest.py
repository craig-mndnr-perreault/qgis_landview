# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CraigTest
                                 A QGIS plugin
 Click on the map
                              -------------------
        begin                : 2017-12-08
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Craig
        email                : craig.perreault@state.mn.us
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.core import QgsApplication

from requests import Session
import json
from craigtest_dialog import CraigTestDialog
import os.path

# app.setPrefixPath('C:/Program Files/QGIS 2.18/apps/qgis', True)


from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon

import qgis.core
from qgis.gui import QgsMapToolEmitPoint
import qgis.gui

from qgis.gui import *

from PyQt4.QtGui import *

from PyQt4.QtCore import SIGNAL, Qt

import sys, os

# Initialize Qt resources from file resources.py
import resources

from qgis.gui import QgsMessageBar



class CraigTest(QWidget):
    """QGIS Plugin Implementation."""

    def __init__(self, iface, parent=None):
        super(CraigTest, self).__init__(parent)
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # self.initGui()
        self.canvas = self.iface.mapCanvas()
        self.clickTool = QgsMapToolEmitPoint(self.canvas)

        self.aTextBox = QLineEdit(self)

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CraigTest_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&CraigTest')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'CraigTest')
        self.toolbar.setObjectName(u'CraigTest')

    # noinspection PyMethodMayBeStatic

    def mousePressEvent(self, QMouseEvent):
        self.dlg.wCountyName.setText("mousePressEvent")
        # print QMouseEvent.pos()

    def mouseReleaseEvent(self, QMouseEvent):
        self.dlg.wCountyName.setText("mouseReleaseEvent")
        print('(', QMouseEvent.x(), ', ', QMouseEvent.y(), ')')

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CraigTest', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):

        self.dlg = CraigTestDialog()
        self.dlg.convertButton.clicked.connect(self.convertButtonClicked)
        self.dlg.mapButton.clicked.connect(self.mapButtonClicked)

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&CraigTest'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def pointedClickedOnMapEvent(self, event):
        # Get the click
        x = event.x()
        y = event.y()
        # point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        self.populateFromUTM(str(x), str(y))

    def clearWhereForm(self):
        self.dlg.wUtmX.setText("")
        self.dlg.wUtmY.setText("")

        self.dlg.wDmsLatDeg.setText("")
        self.dlg.wDmsLatMin.setText("")
        self.dlg.wDmsLatSec.setText("")
        self.dlg.wDmsLonDeg.setText("")
        self.dlg.wDmsLonMin.setText("")
        self.dlg.wDmsLonSec.setText("")

        self.dlg.wDdLat.setText("")
        self.dlg.wDdLon.setText("")

        self.dlg.wDmLatDeg.setText("")
        self.dlg.wDmLatDm.setText("")
        self.dlg.wDmLonDeg.setText("")
        self.dlg.wDmLonDm.setText("")

        self.dlg.wCountyName.setText("")
        self.dlg.wTwp.setText("")
        self.dlg.wRng.setText("")
        self.dlg.wSec.setText("")
        self.dlg.wForty.setText("")
        self.dlg.wForty1.setText("")
        self.dlg.wForty2.setText("")
        self.dlg.wGlot.setText("")

        self.dlg.wDirWest.setChecked(True)
        self.dlg.wDirEast.setChecked(False)

        self.dlg.wMcd.setText("")

        self.dlg.wUsngCoord.setText("")
        self.dlg.wUsng1.setText("")
        self.dlg.wUsng2.setText("")
        self.dlg.wUsng3.setText("")
        self.dlg.wUsng4.setText("")

    def populateWhereForm(self, data):
        # self.iface.messageBar().pushMessage("Hello", data, level=QgsMessageBar.INFO)
        self.dlg.wUtmX.setText("%0.0f" % data['results']['utm']['x'])
        self.dlg.wUtmY.setText("%0.0f" % data['results']['utm']['y'])

        self.dlg.wDmsLatDeg.setText(str(data['results']['latlong']['dms']['lat_deg']))
        self.dlg.wDmsLatMin.setText(str(data['results']['latlong']['dms']['lat_min']))
        self.dlg.wDmsLatSec.setText("%0.1f" % data['results']['latlong']['dms']['lat_sec'])
        self.dlg.wDmsLonDeg.setText(str(data['results']['latlong']['dms']['lon_deg']))
        self.dlg.wDmsLonMin.setText(str(data['results']['latlong']['dms']['lon_min']))
        self.dlg.wDmsLonSec.setText("%0.1f" % data['results']['latlong']['dms']['lon_sec'])

        self.dlg.wDdLat.setText("%0.5f" % data['results']['latlong']['dd']['lat'])
        self.dlg.wDdLon.setText("%0.5f" % data['results']['latlong']['dd']['lon'])

        self.dlg.wDmLatDeg.setText(str("%0.0f" % data['results']['latlong']['dm']['lat_deg']))
        self.dlg.wDmLatDm.setText("%0.3f" % data['results']['latlong']['dm']['lat_dm'])
        self.dlg.wDmLonDeg.setText(str("%0.0f" % data['results']['latlong']['dm']['lon_deg']))
        self.dlg.wDmLonDm.setText("%0.3f" % data['results']['latlong']['dm']['lon_dm'])

        self.dlg.wCountyName.setText(data['results']['cty_mcd']['county_name'])
        self.dlg.wTwp.setText(str(data['results']['pls']['twp']))
        self.dlg.wRng.setText(str(data['results']['pls']['rng']))
        self.dlg.wSec.setText(str(data['results']['pls']['sec']))
        self.dlg.wForty.setText(str(data['results']['pls']['forty']))
        self.dlg.wForty1.setText(data['results']['pls']['forty1'])
        self.dlg.wForty2.setText(data['results']['pls']['forty2'])
        self.dlg.wGlot.setText(str(data['results']['pls']['glot']))
        if data['results']['pls']['dir'] == 0:
            self.dlg.wDirWest.setChecked(True)
        else:
            self.dlg.wDirEast.setChecked(True)
        self.dlg.wMcd.setText(data['results']['cty_mcd']['mcd'])

        self.dlg.wUsngCoord.setText(str(data['results']['usng']['coord']))
        self.dlg.wUsng1.setText(str(data['results']['usng']['usng1']))
        self.dlg.wUsng2.setText(str(data['results']['usng']['usng2']))
        self.dlg.wUsng3.setText(str(data['results']['usng']['usng3']))
        self.dlg.wUsng4.setText(str(data['results']['usng']['usng4']))

    def convertButtonClicked(self):
        # theX = float(self.dlg.wUtmX.text())
        # theY = float(self.dlg.wUtmY.text())
        self.populateFromUTM(self.dlg.wUtmX.text(), self.dlg.wUtmY.text())

    def populateFromUTM(self, x, y):
        session = Session()
        session.head('http://arcgis.dnr.state.mn.us/gis/lv_where_service')
        whereData = session.post(
            url='http://arcgis.dnr.state.mn.us/gis/lv_where_service/where.py',
            data={
                'PointText': x + ' ' + y
            },
            headers={
                'Referer': 'http://arcgis.dnr.state.mn.us/gis/lv_where_service'
            }
        )
        data = json.loads(whereData.text)
        self.populateWhereForm(data)

    def mapButtonClicked(self):
        canvas = qgis.utils.iface.mapCanvas()
        canvas.refresh()
        theX = float(self.dlg.wUtmX.text())
        theY = float(self.dlg.wUtmY.text())
        offset = float(self.dlg.mapRadius.text()) * 1609.34
        zoomRectangle = QgsRectangle(theX - offset, theY - offset,theX + offset, theY + offset)
        canvas.setExtent(zoomRectangle)
        canvas.refresh()

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/CraigTest/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Landview'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.clickTool.canvasClicked.connect(self.pointedClickedOnMapEvent)
        # self.aTextBox..connect(self.clearWhereForm)
        # self.aTextBox.returnPressed(self.clearWhereForm)
        self.aTextBox.textChanged.connect(self.clearWhereForm)

    def run(self):

        # print 'Hello world!'
        # self.iface.messageBar().pushMessage("Hello", "World", level=QgsMessageBar.INFO)
        """Run method that performs all the real work"""
        # show the dialog
        self.canvas.setMapTool(self.clickTool)
        self.dlg.show()

        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # self.iface.messageBar().pushMessage("Hello", "World 2222222222222", level=QgsMessageBar.INFO)
            # sender = self.sender()
            # self.iface.messageBar().pushMessage(sender.text() + ' was pressed', level=QgsMessageBar.INFO)
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
