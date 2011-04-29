""" Base TestCase for Audit
"""
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure

PRODUCTS = (#'ATVocabularyManager',
            #'LinguaPlone',
            #'PloneHelpCenter',
            'EEAContentTypes',
            'valentine.linguaflow',
            'PloneLanguageTool',
            'EEAPloneAdmin',
            #'FiveSite',
            'ThemeCentre')

PloneTestCase.installProduct('ATVocabularyManager')
PloneTestCase.installProduct('PloneHelpCenter')
PloneTestCase.installProduct('LinguaPlone')

@onsetup
def setup_themecentre():
    fiveconfigure.debug_mode = True
    import eea.themecentre
    #TODO: fix me plone4
    #import Products.ThemeCentre
    zcml.load_config('configure.zcml', eea.themecentre)
    #TODO: fix me plone4
    #zcml.load_config('overrides.zcml', Products.ThemeCentre)
    fiveconfigure.debug_mode = False

setup_themecentre()
PloneTestCase.setupPloneSite(extension_profiles=('eea.themecentre:default',))

class ThemeCentreTestCase(PloneTestCase.FunctionalTestCase):
    """ Test case class used for functional themecentre tests. """
