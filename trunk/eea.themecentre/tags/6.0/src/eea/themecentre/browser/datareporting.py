""" Data reporting
"""
from eea.themecentre.themecentre import getTheme #, getThemeCentre
from Products.CMFCore.utils import getToolByName
from DateTime.DateTime import DateTime
import xmlrpclib

#from eea.dataservice.config import ROD_SERVER
ROD_SERVER = 'http://rod.eionet.europa.eu/rpcrouter'

class DataCentreReporting(object):
    """ Return reporting obligations related to this theme.
        This is done by getting first all data sets tagged with this theme and then
        getting all the ROD urls used for those datasets.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request


    def relatedReportingObligations(self):
        """ Return a list of Reporting Obligations related to this theme
        """
        currentTheme = getTheme(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')
        rodbaseurl = 'http://rod.eionet.europa.eu/obligations/'
        rods = []
        rodsdone = []
        now = DateTime()
        rodsinfo = {}
        server = xmlrpclib.Server(ROD_SERVER)
        result = server.WebRODService.getROComplete()
        if result:
            for obligation in result:
                rodsinfo[int(obligation['PK_RA_ID'])] = obligation

        query = {
            'object_provides': 'eea.dataservice.interfaces.IDataset',
            'review_state': 'published',
            'effectiveRange' : now,
        }
        if currentTheme:
            query['getThemes'] = currentTheme
        result = catalog.searchResults(query)

        for res in result:
            reso = res.getObject()
            for rodid in reso.reportingObligations:
                if rodid not in rodsdone:
                    rodsdone.append(rodid)
                    rodurl = rodbaseurl + rodid
                    rods.append({
                       'id' : rodid,
                       'Description' : rodsinfo[int(rodid)]['DESCRIPTION'],
                       'Title' : rodsinfo[int(rodid)]['TITLE'],
                       'url' : rodurl,
                       'absolute_url' : rodurl,
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
        server = xmlrpclib.Server(ROD_SERVER)
        result = server.WebRODService.getROComplete()
        if result:
            for obligation in result:
                rods[int(obligation['PK_RA_ID'])] = obligation
        return rods


