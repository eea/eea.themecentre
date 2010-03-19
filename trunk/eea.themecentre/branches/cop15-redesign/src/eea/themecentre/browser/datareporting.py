from eea.themecentre.themecentre import getTheme, getThemeCentre
from Products.CMFCore.utils import getToolByName
from DateTime.DateTime import DateTime

class DataCentreReporting(object):
    """ Return reporting obligations realted to this theme. 
    This is done by getting first all data sets tagged with this theme and then
    getting all the ROD urls used for those datasets."""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    def relatedReportingObligations(self):
        """ return a list of Reporting Obligations related to this theme """
        currentTheme = getTheme(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')
        rodbaseurl = 'http://rod.eionet.europa.eu/obligations/'
        rods = []
        rodsdone = []
        now = DateTime()

        result = catalog({
            'object_provides': 'eea.dataservice.interfaces.IDataset',
            'getThemes': currentTheme,
            'review_state': 'published',
            'effectiveRange' : now,
        })
        
        for res in result[:10]:
            reso=res.getObject()
            for rodid in reso.reportingObligations:
                if rodid not in rodsdone:
                    rodsdone.append(rodid)
                    rodurl = rodbaseurl + rodid
                    rods.append({
                       'id' : rodid,
                       'Description' : '',
                       'Title' : rodurl,
                       'url' : rodurl,
                       'absolute_url' : rodurl,
                     })

        return rods