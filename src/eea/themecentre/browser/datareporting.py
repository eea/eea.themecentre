""" Data reporting
"""
import logging

import eventlet
from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName

# from eea.dataservice.config import ROD_SERVER, SOCKET_TIMEOUT
from eea.themecentre.themecentre import getTheme

ROD_SERVER = 'http://rod.eionet.europa.eu/rpcrouter'
SOCKET_TIMEOUT = 2.0  # in seconds
logger = logging.getLogger('eea.themecentre.datareporting')


class DataCentreReporting(object):
    """ Return reporting obligations related to this theme.
        This is done by getting first all data sets tagged with this theme and
        then getting all the ROD urls used for those datasets.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def relatedReportingObligations(self):
        """ Return a list of Reporting Obligations related to this theme
        """
        current_theme = getTheme(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')
        rodbaseurl = 'http://rod.eionet.europa.eu/obligations/'
        rods = []
        rodsdone = []
        now = DateTime()
        rodsinfo = {}
        result = None
        xmlrpclib = eventlet.import_patched('xmlrpclib')

        with eventlet.timeout.Timeout(SOCKET_TIMEOUT):
            try:
                server = xmlrpclib.Server(ROD_SERVER)
                result = server.WebRODService.getROComplete()
            except Exception, err:
                logger.exception(err)
                result = []

        if result:
            for obligation in result:
                rodsinfo[int(obligation['PK_RA_ID'])] = obligation

        query = {
            'object_provides': 'eea.dataservice.interfaces.IDataset',
            'review_state': 'published',
            'effectiveRange': now,
        }
        if current_theme:
            query['getThemes'] = current_theme
        result = catalog.searchResults(query)

        for res in result:
            reso = res.getObject()
            for rodid in reso.reportingObligations:
                if rodid not in rodsdone:
                    rodsdone.append(rodid)
                    rodurl = rodbaseurl + rodid
                    rods.append({
                        'id': rodid,
                        'Description': rodsinfo[int(rodid)]['DESCRIPTION'],
                        'Title': rodsinfo[int(rodid)]['TITLE'],
                        'url': rodurl,
                        'absolute_url': rodurl,
                    })

        return rods


class ReportingObligationInfo(object):
    """ Return complete info about all reporting obligations from ROD
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        """ Return a struct with full info for obligation with id=rodid
        """
        rods = {}
        result = None
        xmlrpclib = eventlet.import_patched('xmlrpclib')

        with eventlet.timeout.Timeout(SOCKET_TIMEOUT):
            try:
                server = xmlrpclib.Server(ROD_SERVER)
                result = server.WebRODService.getROComplete()
            except Exception, err:
                logger.exception(err)
                result = []

        if result:
            for obligation in result:
                rods[int(obligation['PK_RA_ID'])] = obligation
        return rods
