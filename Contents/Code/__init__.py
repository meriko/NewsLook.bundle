TITLE               = 'NewsLook'
PREFIX              = '/video/newslook'
ART                 = 'art-default.jpg'
ICON                = 'icon-default.png'
API_CATEGORIES_URL  = 'http://iptv.newslook.com/api/v2/categories.json'
API_VIDEO_URL       = 'http://iptv.newslook.com/api/v2/categories/%s.json'
IMG_URL             = 'http://img2.newslook.com/images/dyn/videos/%s/%s/pad/516/291/%s.jpg'

###################################################################################################
def Start():
	# Set the default ObjectContainer attributes
	ObjectContainer.title1 = TITLE
	ObjectContainer.art    = R(ART)

	# Set the default cache time and user agent
	HTTP.CacheTime = 3600
	
###################################################################################################
@handler(PREFIX, TITLE, thumb = ICON, art = ART)
def MainMenu():
	oc = ObjectContainer()

	categories = JSON.ObjectFromURL(API_CATEGORIES_URL)

	for category in categories['categories']:
		oc.add(
			DirectoryObject(
				key = 
					Callback(
						Videos, 
						title = category['name'], 
						id = category['permalink']
					),
				title = category['name']
			)
		) 
	
	return oc

####################################################################################################
@route(PREFIX + '/Videos')
def Videos(title, id):
	oc = ObjectContainer(title2 = title)
	
	url    = API_VIDEO_URL % id
	videos = JSON.ObjectFromURL(url)
						
	for video in videos['videos']:
		oc.add(
			CreateVideoClipObject(
				url = video["cdn_asset_url"],
				title = video["title"],
				thumb = IMG_URL % (str(video["id"]), str(video["thumbnail_version"]), str(video["id"])),
				summary = video["description"],
				duration = int(video["duration"])
			)
		)	
		
	return oc
####################################################################################################
@route(PREFIX + '/CreateVideoClipObject', duration = int, include_container = bool)	
def CreateVideoClipObject(url, title, thumb, summary, duration, include_container = False):
	vco = VideoClipObject(
			key = 
				Callback(
					CreateVideoClipObject,
					url = url,
					title = title,
					thumb = thumb,
					summary = summary,
					duration = duration,
					include_container = True
				),
			rating_key = title,
			title = title,
			thumb = thumb,
			summary = summary,
			duration = duration,
			items = [
				MediaObject(
					container = Container.MP4,
					video_codec = VideoCodec.H264,
					audio_codec = AudioCodec.AAC,
					video_resolution = 360,
					audio_channels = 2,
					parts = [
						PartObject(
							key = url
						)
					],
					optimized_for_streaming = True
				)
			]
	)
	
	if include_container:
		return ObjectContainer(objects = [vco])
	else:
		return vco

