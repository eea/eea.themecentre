""" Base TestCase for Audit
"""
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure


#TODO: fix me, plone4
PRODUCTS = ('EEAContentTypes',
            'EEAPloneAdmin')

PloneTestCase.installProduct('ATVocabularyManager')
PloneTestCase.installProduct('eea.design')
PloneTestCase.installProduct('PloneHelpCenter')
PloneTestCase.installProduct('LinguaPlone')
PloneTestCase.installProduct('valentine.linguaflow')

@onsetup
def setup_themecentre():
    """ Setup theme centre
    """
    fiveconfigure.debug_mode = True
    import eea.themecentre
    zcml.load_config('configure.zcml', eea.themecentre)
    fiveconfigure.debug_mode = False

setup_themecentre()
PloneTestCase.setupPloneSite(extension_profiles=('eea.themecentre:default',))

class ThemeCentreTestCase(PloneTestCase.FunctionalTestCase):
    """ Test case class used for functional themecentre tests. """
