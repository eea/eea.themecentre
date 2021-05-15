""" EEA Theme Centre import steps
"""
from Products.CMFCore.utils import getToolByName


def setupVarious(context):
    """ Setup various
    """
    if context.readDataFile("eea.themecentre.txt") is None:
        return

    logger = context.getLogger("eea.themecentre")
    logger.info("EEA Theme Centre: done setting import steps")
    return
