TITLE               = 'NewsLook'
PREFIX              = '/video/newslook'
ART                 = 'art-default.jpg'
ICON                = 'icon-default.png'

BROKEN_TITLE   = "This channel is no longer available"
BROKEN_MESSAGE = "The Newslook web site no longer contains any videos"

###################################################################################################
def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art    = R(ART)
    DirectoryObject.thumb  = R(ICON)
    HTTP.CacheTime         = CACHE_1HOUR
    
###################################################################################################
@handler(PREFIX, TITLE, thumb = ICON, art = ART)
def MainMenu():
    oc = ObjectContainer()
    
    oc.add(
        DirectoryObject(
            key =
                Callback(
                    Broken
                ),
            title   = BROKEN_TITLE,
            summary = BROKEN_MESSAGE
        )
    )

    return oc
    
####################################################################################################
@route(PREFIX + '/Broken')
def Broken():
	oc = ObjectContainer(title2 = "Broken")
	
	oc.header  = BROKEN_TITLE
	oc.message = BROKEN_MESSAGE
	
	return oc
