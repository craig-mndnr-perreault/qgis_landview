# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CraigTest
                                 A QGIS plugin
 Click on the map
                             -------------------
        begin                : 2017-12-08
        copyright            : (C) 2017 by Craig
        email                : craig.perreault@state.mn.us
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load CraigTest class from file CraigTest.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .craigtest import CraigTest
    return CraigTest(iface)
