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

sql_links = \
    u"select tblElements.eid, link, title, body " + \
    u"from tblLinks, tblLinksBody, tblPagesElements, tblElements " + \
    u"where tblPagesElements.eid=tblElements.eid and tblElements.tid=7 " + \
    u"and tblPagesElements.pid=%d " + \
    u"and tblLinks.hid=tblLinksBody.hid " + \
    u"and tblLinks.hid=tblLinksBody.hid " + \
    u"and tblLinks.eid=tblElements.eid " + \
    u"and tblLinksBody.lid=1"

METADATA = {
    '1004_1.flv': { 'height': 180, 'width': 240, 'duration': 46.866 },
    '1004_2.flv': { 'height': 180, 'width': 240, 'duration': 44.466 },
    '1075_1.flv': { 'height': 180, 'width': 240, 'duration': 58.995 },
    '1149_1.flv': { 'height': 180, 'width': 240, 'duration': 87.44 },
    '1150_1.flv': { 'height': 180, 'width': 240, 'duration': 48.36 },
    '1151_1.flv': { 'height': 180, 'width': 240, 'duration': 63.16 },
    '1152_1.flv': { 'height': 180, 'width': 240, 'duration': 33.355 },
    '1153_1.flv': { 'height': 180, 'width': 240, 'duration': 48 },
    '1154_1.flv': { 'height': 180, 'width': 240, 'duration': 64.44 },
    '1203_1.flv': { 'height': 180, 'width': 240, 'duration': 87.2 },
    '1225_1.flv': { 'height': 180, 'width': 240, 'duration': 48.199 },
    '1225_2.flv': { 'height': 180, 'width': 240, 'duration': 114.666 },
    '1225_3.flv': { 'height': 180, 'width': 240, 'duration': 38.999 },
    '1225_4.flv': { 'height': 180, 'width': 240, 'duration': 31.099 },
    '1278_1.flv': { 'height': 178, 'width': 238, 'duration': 36 },
    '1279_1.flv': { 'height': 178, 'width': 238, 'duration': 20 },
    '462_1.flv': { 'height': 180, 'width': 240, 'duration': 48.281 },
    '462_3.flv': { 'height': 180, 'width': 240, 'duration': 39.084 },
    '462_4.flv': { 'height': 180, 'width': 240, 'duration': 31.183 },
    '462_5.flv': { 'height': 180, 'width': 240, 'duration': 114.747 },
    '464_2.flv': { 'height': 180, 'width': 240, 'duration': 51.236 },
    '464_5.flv': { 'height': 180, 'width': 240, 'duration': 50.505 },
    '464_6.flv': { 'height': 180, 'width': 240, 'duration': 95.856 },
    '464_7.flv': { 'height': 180, 'width': 240, 'duration': 64.184 },
    '464_8.flv': { 'height': 180, 'width': 240, 'duration': 86.494 },
    '465_1.flv': { 'height': 180, 'width': 240, 'duration': 100.139 },
    '465_2.flv': { 'height': 180, 'width': 240, 'duration': 94.86 },
    '465_3.flv': { 'height': 180, 'width': 240, 'duration': 108.937 },
    '465_4.flv': { 'height': 180, 'width': 240, 'duration': 141.772 },
    '466_1.flv': { 'height': 180, 'width': 240, 'duration': 39.084 },
    '466_3.flv': { 'height': 180, 'width': 240, 'duration': 39.084 },
    '667_1.flv': { 'height': 180, 'width': 240, 'duration': 33.355 },
    '667_2.flv': { 'height': 180, 'width': 240, 'duration': 36.435 },
    '667_3.flv': { 'height': 180, 'width': 240, 'duration': 60.795 },
    '667_4.flv': { 'height': 180, 'width': 240, 'duration': 53.435 },
    '667_5.flv': { 'height': 180, 'width': 240, 'duration': 108 },
    '668_1.flv': { 'height': 180, 'width': 240, 'duration': 25.84 },
    '669_1.flv': { 'height': 180, 'width': 240, 'duration': 55.56 },
    '672_1.flv': { 'height': 180, 'width': 240, 'duration': 44.755 },
    '677_1.flv': { 'height': 180, 'width': 240, 'duration': 16.24 },
    '678_1.flv': { 'height': 180, 'width': 240, 'duration': 69.875 },
    '678_2.flv': { 'height': 180, 'width': 240, 'duration': 53.115 },
    '678_3.flv': { 'height': 180, 'width': 240, 'duration': 50.595 },
    '678_5.flv': { 'height': 180, 'width': 240, 'duration': 64.235 },
    '678_6.flv': { 'height': 180, 'width': 240, 'duration': 108 },
    '678_7.flv': { 'height': 180, 'width': 240, 'duration': 108 },
    '699_1.flv': { 'height': 240, 'width': 264, 'duration': 56.166 },
    '700_1.flv': { 'height': 180, 'width': 240, 'duration': 57.28 },
    '701_1.flv': { 'height': 180, 'width': 240, 'duration': 42.84 },
    '702_1.flv': { 'height': 180, 'width': 240, 'duration': 13.68 },
    '703_1.flv': { 'height': 180, 'width': 240, 'duration': 16.24 },
    '707_1.flv': { 'height': 164, 'width': 240, 'duration': 599.6 },
    '707_1_old.flv': { 'height': 180, 'width': 240, 'duration': 599.715 },
    '707_2.flv': { 'height': 180, 'width': 240, 'duration': 108 },
    '708_1.flv': { 'height': 180, 'width': 240, 'duration': 58.995 },
    '742_1.flv': { 'height': 180, 'width': 240, 'duration': 48.281 },
    '751_1.flv': { 'height': 360, 'width': 462, 'duration': 36.24 },
    '752_1.flv': { 'height': 180, 'width': 230, 'duration': 36.24 },
    '755_1.flv': { 'height': 180, 'width': 240, 'duration': 36 },
    '757_1.flv': { 'height': 180, 'width': 240, 'duration': 33.52 },
}
