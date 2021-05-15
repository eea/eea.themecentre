""" EEA Theme Centre import steps
"""

def setupVarious(context):
    """ Setup various
    """
    if context.readDataFile("eea.themecentre.txt") is None:
        return

    logger = context.getLogger("eea.themecentre")
    logger.info("EEA Theme Centre: done setting import steps")
    return
