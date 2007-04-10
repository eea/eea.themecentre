sql_stretchminders = \
    "select tblElements.eid from tblPagesElements, tblElements " + \
    "where tblPagesElements.pid=200 and tblElements.tid=5 and " + \
    "tblPagesElements.eid=tblElements.eid"

sql_images = \
    u"select tblElements.eid, title, extension from tblImages, tblImagesBody, " + \
    u"tblPagesElements, tblElements " + \
    u"where tblPagesElements.eid=tblElements.eid and tblElements.tid=5 " + \
    u"and tblPagesElements.pid=%d and tblImages.yid=tblImagesBody.yid " + \
    u"and tblImages.eid=tblElements.eid and tblImagesBody.lid=1"
