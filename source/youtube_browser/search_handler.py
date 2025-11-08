from youtubesearchpython import VideosSearch, CustomSearch, PlaylistsSearch, PlaylistsSearch, Playlist
from utiles import time_formatting
from logger_config import get_logger

logger = get_logger(__name__)



class PlaylistResult:
	def __init__(self, url):
		self.url = url
		self.playlist = Playlist(url)
		self.videos = []
		self.count = 0
		self.parse()

	def parse(self):
		for vid in self.playlist.videos[self.count:]:
			video = {
				"title": vid["title"],
				"url": f"https://youtube.com/watch?v={vid['id']}",
				"duration": time_formatting(vid["duration"]),
				"channel": {
					"name": vid["channel"]["name"], 
					"url": f"https://www.youtube.com/channel/{vid['channel']['id']}"},

			}
			self.videos.append(video)
			self.count = len(self.videos)

	def next(self):
		if not self.playlist.hasMoreVideos:
			return
		self.playlist.getNextVideos()
		current = self.count
		self.parse()
		self.new_videos = self.count-current

		return True
	def get_new_titles(self):
		titles = self.get_display_titles()
		return titles[len(titles)-self.new_videos:len(titles)]

	def get_title(self, n):
		return self.videos[n]["title"]
	def get_display_titles(self):
		titles = []
		for vid in self.videos:
			title = [vid['title'], _("المدة: {}").format(vid['duration']), f"{_('بواسطة')} {vid['channel']['name']}"]
			titles.append(", ".join(title))
		return titles
	def get_url(self, n):
		return self.videos[n]["url"]





class Search:
	def __init__(self, query, filter=0):
		logger.info(f"Initializing Search with query: '{query}', filter: {filter}")
		self.query = query
		self.filter = filter
		self.results = {}
		self.count = 1
		filters = {
			1: "EgJAAQ",
			2: "CAISAhAB",
			3: "CAMSAhAB", 
			4: "EgIQA"
		}
		try:
			if self.filter == 0:
				logger.debug("Creating VideosSearch")
				self.search = VideosSearch(self.query)
			elif self.filter == 4:
				logger.debug("Creating PlaylistsSearch")
				self.search = PlaylistsSearch(self.query)
			else:
				logger.debug(f"Creating CustomSearch with filter: {filters[self.filter]}")
				self.search = CustomSearch(self.query, filters[self.filter])
			logger.debug("Loading initial search results...")
			self.load_more()
			logger.info(f"Search initialized successfully with {self.count-1} results")
		except Exception as e:
			logger.error(f"Failed to initialize search: {type(e).__name__}: {str(e)}")
			raise

	def load_more(self):
		logger.info("Loading more search results...")
		try:
			results = self.search.result()["result"]
			initial_count = self.count
			logger.debug(f"Processing {len(results)} additional results")
			
			for i, result in enumerate(results):
				logger.debug(f"Processing result {i+1}/{len(results)}: {result.get('title', 'N/A')}")
				self.results[self.count] = {
					"type": result["type"],
					"title": result["title"],
					"url": result["link"], 
					"duration": result.get("duration"),
					"elements": result.get("videoCount"),
					"channel": {
						"name": result["channel"]["name"], 
						"url": f"https://www.youtube.com/channel/{result['channel']['id']}"}
				}
				if result["type"] == "video":
					self.results[self.count]["views"] = self.parse_views(result["viewCount"]["text"])
				else:
					self.results[self.count]["views"] = None
				self.count += 1
			
			logger.info(f"Loaded {self.count - initial_count} more results. Total: {self.count-1}")
		except KeyError as e:
			logger.error(f"KeyError while loading more results - missing key: {str(e)}")
			raise
		except Exception as e:
			logger.error(f"Failed to load more results: {type(e).__name__}: {str(e)}")
			raise
	def get_titles(self):
		titles = []
		for result, data  in self.results.items():
			title = [data['title']]
			if data["type"] == "video":
				title += [self.get_duration(data['duration']),
					f"{_('بواسطة')} {data['channel']['name']}",
					self.views_part(data['views'])]
			elif data["type"] == "playlist":
				title += [_("قائمة تشغيل"),
			f"{_('بواسطة')} {data['channel']['name']}", 
					_("تحتوي على {} من الفيديوهات").format(data["elements"])]
			titles.append(", ".join([element for element in title if element != ""]))
		return titles

	def get_last_titles(self):
		titles = self.get_titles()
		return titles[len(titles)-self.new_videos:len(titles)]
	def get_title(self, number):
		return self.results[number+1]["title"]
	def get_url(self, number):
		return self.results[number+1]["url"]
	def get_type(self, number):
		return self.results[number+1]["type"]
	def get_channel(self, number):
		return self.results[number+1]["channel"]

	def load_more_next_page(self):
		"""Load the next page of search results"""
		logger.info("Attempting to load next page of search results...")
		try:
			self.search.next()
			logger.debug("search.next() called successfully")
		except Exception as e:
			logger.warning(f"No more results to load: {type(e).__name__}: {str(e)}")
			return False
		current = self.count
		logger.debug(f"Current result count before parsing: {current}")
		# Now parse the new results from the next page
		try:
			results = self.search.result()["result"]
			logger.debug(f"Processing {len(results)} additional results from next page")
			
			for i, result in enumerate(results):
				logger.debug(f"Processing result {i+1}/{len(results)}: {result.get('title', 'N/A')}")
				self.results[self.count] = {
					"type": result["type"],
					"title": result["title"],
					"url": result["link"], 
					"duration": result.get("duration"),
					"elements": result.get("videoCount"),
					"channel": {
						"name": result["channel"]["name"], 
						"url": f"https://www.youtube.com/channel/{result['channel']['id']}"}
				}
				if result["type"] == "video":
					self.results[self.count]["views"] = self.parse_views(result["viewCount"]["text"])
				else:
					self.results[self.count]["views"] = None
				self.count += 1
			
			self.new_videos = self.count-current
			logger.info(f"Loaded {self.new_videos} new videos. Total: {self.count-1}")
			return True
		except KeyError as e:
			logger.error(f"KeyError while loading next page - missing key: {str(e)}")
			raise
		except Exception as e:
			logger.error(f"Failed to load next page: {type(e).__name__}: {str(e)}")
			raise
	def parse_views(self, string):
		try:
			string = string.replace(",", "")
		except AttributeError:
			return
		return string.replace("views", "")
	def get_views(self, number):

		return self.results[number+1]['views']
	def views_part(self, data):
		if data is not None:
			return _("عدد المشاهدات {}").format(data)
		else:
			return _("بث مباشر")

	def get_duration(self, data): # get the duration of the video
		if data is not None:
			return _("المدة: {}").format(time_formatting(data))
		else:
			return ""