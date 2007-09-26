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
    u"select tblElements.eid, link, title, body, tblLinks.pid " + \
    u"from tblLinks, tblLinksBody, tblPagesElements, tblElements " + \
    u"where tblPagesElements.eid=tblElements.eid and tblElements.tid=7 " + \
    u"and tblPagesElements.pid=%d " + \
    u"and tblLinks.hid=tblLinksBody.hid " + \
    u"and tblLinks.hid=tblLinksBody.hid " + \
    u"and tblLinks.eid=tblElements.eid " + \
    u"and tblLinksBody.lid=1 " + \
    u"and link != 'NULL'"

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

sql_level_one = \
    u"select title, tblTierOne.pid, cid " + \
    u"from (tblPages inner join tblPagesSectionsBody " + \
    u"on tblPages.pid = tblPagesSectionsBody.pid) " + \
    u"inner join tblTierOne on tblPages.pid = tblTierOne.pid " + \
    u"where tblPagesSectionsBody.section=1 " + \
    u"and tblPages.status=4 " + \
    u"and (trans not like '%%|1|%%' or trans=1) " + \
    u"and tblPagesSectionsBody.lid=1 " + \
    u"ORDER BY tblPagesSectionsBody.title asc"

sql_level_two = \
    u"select tblTierTwo.pid, tblTierTwo.ciid, tblPagesSectionsBody.title " + \
    u"from (tblPages inner join tblPagesSectionsBody " + \
    u"on tblPages.pid=tblPagesSectionsBody.pid) " + \
    u"inner join tblTierTwo on tblPages.pid=tblTierTwo.pid " + \
    u"where (tblPagesSectionsBody.section=1 " + \
    u"and tblPagesSectionsBody.lid=1 " + \
    u"and tblTierTwo.cid=%d and tblPages.status=4 " + \
    u"and (trans not like '%%|1|%%' or trans=1)) " + \
    u"order by tblPagesSectionsBody.title asc"

sql_level_three = \
    u"select tblPagesSectionsBody.pid, tblPagesSectionsBody.title " + \
    u"from (tblPages inner join tblPagesSectionsBody " + \
    u"on tblPages.pid=tblPagesSectionsBody.pid) " + \
    u"inner join tblTierThree on tblPages.pid = tblTierThree.pid " + \
    u"where tblPagesSectionsBody.section=1 " + \
    u"and tblPagesSectionsBody.lid=1 " + \
    u"and tblTierThree.ciid=%d and tblPages.status=4 " + \
    u"and (trans not like '%%|1|%%' or trans=1) " + \
    u"order by tblPagesSectionsBody.title asc"

sql_sections = \
    u"select tblPagesSections.pid, tblPagesSections.section, " + \
    u"tblPagesSections.type, tblPagesSections.eid, " + \
    u"tblPagesSections.align " + \
    u"from tblPages " + \
    u"inner join tblPagesSections on tblPages.pid = tblPagesSections.pid " + \
    u"where tblPagesSections.pid=%d " + \
    u"order by tblPagesSections.section"

sql_title = \
    u"select title " + \
    u"from tblPagesSectionsBody " + \
    u"where pid=%d " + \
    u"and section=1"

sql_section_content = \
    u"select title, body, quote, tag " + \
    u"from tblPagesSectionsBody " + \
    u"where pid=%d " + \
    u"and lid=1 " + \
    u"and section=%d"

sql_article_links = \
    u"select eid, link, pid, title, body " + \
    u"from tblLinks inner join tblLinksBody " + \
    u"on tblLinks.hid=tblLinksBody.hid " + \
    u"where tblLinks.eid=%d " + \
    u"and tblLinksBody.lid=1"

sql_snapshot_pid = \
    u"select tblPages.pid, status, cid " + \
    u"from tblPages inner join tblTierTwo " + \
    u"on tblPages.pid=tblTierTwo.pid " + \
    u"where tblTierTwo.cid=%d and tblPages.status=2"

sql_fullarticle_pid = \
    u"select tblPages.pid, status, cid " + \
    u"from tblPages inner join tblTierTwo " + \
    u"on tblPages.pid=tblTierTwo.pid " + \
    u"where tblTierTwo.cid=%d and tblPages.status=3"

sql_cid_with_onetier_pid = \
    u"select cid " + \
    u"from tblTierOne " + \
    u"where pid=%d"

sql_image_by_eid = \
    u"select title, extension, source, note " + \
    u"from tblImages inner join tblImagesBody " + \
    u"on tblImages.yid = tblImagesBody.yid " + \
    u"where tblImages.eid=%d and tblImagesBody.lid=1"

sql_eids_by_pid = \
    u"select eid from tblPagesElements where pid=%d"

sql_all_images = \
    u"select eid, title, extension " + \
    u"from tblImages, tblImagesBody " + \
    u"where tblImages.yid=tblImagesBody.yid " + \
    u"and lid=1"
