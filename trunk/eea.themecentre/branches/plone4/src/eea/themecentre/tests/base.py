""" Base
"""
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure
import eea.themecentre

#TODO: fix me, plone4
PRODUCTS = ('EEAContentTypes',)

PloneTestCase.installProduct('ATVocabularyManager')
PloneTestCase.installProduct('PloneHelpCenter')
PloneTestCase.installProduct('LinguaPlone')
PloneTestCase.installProduct('EEAPloneAdmin')

@onsetup
def setup_themecentre():
    """ Setup theme centre
    """
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', eea.themecentre)
    fiveconfigure.debug_mode = False

    PloneTestCase.installPackage('valentine.linguaflow')
    PloneTestCase.installPackage('eea.design')
    PloneTestCase.installPackage('eea.vocab')

setup_themecentre()
PloneTestCase.setupPloneSite(extension_profiles=('eea.themecentre:default',))

class EEAThemeCentreTestCase(PloneTestCase.FunctionalTestCase):
    """ Test case class used for functional themecentre tests. """
