sql_images = \
    u"select tblElements.eid, title, extension from tblImages, tblImagesBody, " + \
    u"tblPagesElements, tblElements " + \
    u"where tblPagesElements.eid=tblElements.eid and tblElements.tid=5 " + \
    u"and tblPagesElements.pid=%d and tblImages.yid=tblImagesBody.yid " + \
    u"and tblImages.eid=tblElements.eid and tblImagesBody.lid=1"

sql_animations = \
    u"select tblElements.eid, title " + \
    u"from tblAnimations, tblAnimationsTitle, tblPagesElements, tblElements " + \
    u"where tblPagesElements.eid=tblElements.eid and tblElements.tid=4 " + \
    u"and tblPagesElements.pid=%d " + \
    u"and tblAnimations.kid=tblAnimationsTitle.kid " + \
    u"and tblAnimations.eid=tblElements.eid"

sql_mindstretchers = \
    u"select tblElements.eid, title " + \
    u"from tblAnimations, tblAnimationsTitle, tblPagesElements, tblElements " + \
    u"where tblPagesElements.eid=tblElements.eid and tblElements.tid=8 " + \
    u"and tblPagesElements.pid=%d " + \
    u"and tblAnimations.kid=tblAnimationsTitle.kid " + \
    u"and tblAnimations.eid=tblElements.eid"

sql_videos = \
    u"select tblElements.eid, tblVideosTitles.title, body, item " + \
    u"from tblVideos, tblVideosTitles, tblVideosBody, " + \
    u"     tblPagesElements, tblElements " + \
    u"where tblPagesElements.eid=tblElements.eid and tblElements.tid=1 " + \
    u"and tblPagesElements.pid=%d " + \
    u"and tblVideos.aid=tblVideosTitles.aid " + \
    u"and tblVideosTitles.aid=tblVideosBody.aid " + \
    u"and tblVideos.eid=tblElements.eid " + \
    u"and tblVideosTitles.lid=1 " + \
    u"and tblVideosBody.lid=1"
