""" Base
"""
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure
import eea.themecentre

PloneTestCase.installProduct('ATVocabularyManager')
PloneTestCase.installProduct('LinguaPlone')
PloneTestCase.installProduct('EEAPloneAdmin')
PloneTestCase.installProduct('EEAContentTypes')

@onsetup
def setup_themecentre():
    """ Setup theme centre
    """
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', eea.themecentre)
    fiveconfigure.debug_mode = False

setup_themecentre()
PloneTestCase.setupPloneSite(extension_profiles=(
    'eea.themecentre:default',
))

class EEAThemeCentreTestCase(PloneTestCase.FunctionalTestCase):
    """ Test case class used for functional themecentre tests.
    """
