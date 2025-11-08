
import webbrowser
from threading import Thread


import pyperclip
import wx
from logger_config import get_logger
from gui.download_progress import DownloadProgress
from gui.search_dialog import SearchDialog

logger = get_logger(__name__)
from gui.settings_dialog import SettingsDialog
from gui.playlist_dialog import PlaylistDialog
from gui.activity_dialog import LoadingDialog

from download_handler.downloader import downloadAction
from media_player.media_gui import MediaGui
from media_player.player import Player
from nvda_client.client import speak
from settings_handler import config_get
from youtube_browser.search_handler import Search
from utiles import direct_download, get_audio_stream, get_video_stream
from database import Favorite, Continue


class YoutubeBrowser(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent=parent, title=parent.Title)
		self.Centre()
		self.SetSize(wx.DisplaySize())
		self.Maximize(True)
		self.panel = wx.Panel(self)
		lbl = wx.StaticText(self.panel, -1, _("نتائج البحث: "))
		self.searchResults = wx.ListBox(self.panel, -1)
		self.loadMoreButton = wx.Button(self.panel, -1, _("تحميل المزيد من النتائج"))
		self.loadMoreButton.Enabled = False
		self.loadMoreButton.Show(not config_get("autoload"))
		self.playButton = wx.Button(self.panel, -1, _("تشغيل (enter)"), name="controls")
		self.downloadButton = wx.Button(self.panel, -1, _("تنزيل"), name="controls")
		self.favCheck = wx.CheckBox(self.panel, -1, _("تفضيل الفيديو"))
		searchButton = wx.Button(self.panel, -1, _("بحث... (ctrl+f)"))
		backButton = wx.Button(self.panel, -1, _("العودة إلى النافذة الرئيسية"))
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer1 = wx.BoxSizer(wx.HORIZONTAL)
		sizer1.Add(backButton, 1, wx.ALL)
		sizer1.Add(searchButton, 1, wx.ALL)
		sizer2 = wx.BoxSizer(wx.HORIZONTAL)
		for control in self.panel.GetChildren():
			if control.Name == "controls":
				sizer2.Add(control, 1)
		sizer.Add(sizer1, 1, wx.EXPAND)
		sizer.Add(lbl, 1, wx.ALL)
		sizer.Add(self.searchResults, 1, wx.EXPAND)
		sizer.Add(self.loadMoreButton, 1)
		sizer.Add(sizer2, 1)
		self.panel.SetSizer(sizer)
		self.contextSetup()
		results_shortcuts = wx.AcceleratorTable([
			(0, wx.WXK_RETURN, self.audioPlayItemId),
			(wx.ACCEL_CTRL, wx.WXK_RETURN, self.videoPlayItemId)
		])
		self.searchResults.SetAcceleratorTable(results_shortcuts)
		menuBar = wx.MenuBar()
		optionsMenu = wx.Menu()
		settingsItem = optionsMenu.Append(-1, _("الإعدادات...\talt+s"))
		hotKeys = wx.AcceleratorTable([
			(wx.ACCEL_ALT, ord("S"), settingsItem.GetId()),
			(wx.ACCEL_CTRL, ord("F"), searchButton.GetId()),
			(wx.ACCEL_CTRL, ord("D"), self.directDownloadId),
			(wx.ACCEL_CTRL, ord("L"), self.copyItemId)
		])
		# hotkey table
		self.SetAcceleratorTable(hotKeys)
		menuBar.Append(optionsMenu, _("خيارات"))
		self.SetMenuBar(menuBar)
		self.Bind(wx.EVT_MENU, lambda event: SettingsDialog(self), settingsItem)
		self.loadMoreButton.Bind(wx.EVT_BUTTON, self.onLoadMore)
		self.playButton.Bind(wx.EVT_BUTTON, lambda event: self.playVideo())
		self.downloadButton.Bind(wx.EVT_BUTTON, self.onDownload)
		self.favCheck.Bind(wx.EVT_CHECKBOX, self.onFavorite)
		searchButton.Bind(wx.EVT_BUTTON, self.onSearch)
		backButton.Bind(wx.EVT_BUTTON, lambda event: self.backAction())
		self.Bind(wx.EVT_CHAR_HOOK, self.onHook)

		self.Bind(wx.EVT_LISTBOX_DCLICK, lambda event: self.playVideo(), self.searchResults)
		self.searchResults.Bind(wx.EVT_LISTBOX, self.onListBox)
		self.Bind(wx.EVT_SHOW, self.onShow)
		self.Bind(wx.EVT_CLOSE, lambda event: wx.Exit())
		if self.searchAction():
			self.Show()
			self.Parent.Hide()
		else:
			self.Destroy()
		self.favorites = Favorite()
		self.togleFavorite()

	def searchAction(self, value=""):
		logger.info(f"Search action initiated with value: {value}")
		dialog = SearchDialog(self, value=value)
		query = dialog.query
		filter = dialog.filter
		logger.info(f"Search query: '{query}', filter: {filter}")
		
		if query is None:
			logger.debug("Search cancelled by user")
			self.togleControls()
			return
		
		# Run the search in LoadingDialog
		logger.info("Starting YouTube search...")
		loading_dlg = LoadingDialog(self, _("جاري البحث"), Search, query, filter)
		
		# Check if an error occurred
		if loading_dlg.error is not None:
			import traceback
			e = loading_dlg.error
			error_details = str(e)
			logger.error(f"Search failed with error: {type(e).__name__}: {error_details}")
			logger.debug(f"Full traceback:\n{traceback.format_exception(type(e), e, e.__traceback__)}")
			print(f"Search error: {e}")
			print(f"Full traceback:\n{traceback.format_exception(type(e), e, e.__traceback__)}")
			
			# More specific error messages
			error_msg = _("تعذر إجراء عملية البحث بسبب وجود خلل ما في الاتصال بالشبكة.")
			
			if "unexpected keyword argument 'proxies'" in error_details or "got an unexpected keyword argument" in error_details:
				error_msg = _("خطأ في توافق المكتبات. يرجى تحديث youtube-search-python:\nuv pip install --upgrade youtube-search-python requests")
			elif "KeyError" in str(type(e).__name__):
				error_msg = _("خطأ في تحليل نتائج البحث. قد تكون واجهة YouTube API قد تغيرت.")
			elif "ConnectionError" in str(type(e).__name__) or "Timeout" in str(type(e).__name__):
				error_msg = _("فشل الاتصال بخوادم YouTube. تحقق من اتصال الإنترنت.")
			elif "HTTPError" in str(type(e).__name__):
				if "429" in error_details:
					error_msg = _("تم تجاوز حد الطلبات. يرجى الانتظار قليلاً وإعادة المحاولة.")
				elif "403" in error_details:
					error_msg = _("تم رفض الوصول من قبل YouTube. قد تحتاج إلى تحديث المكتبات.")
			
			# Show detailed error in dialog
			full_msg = f"{error_msg}\n\n{_('تفاصيل الخطأ')}: {error_details[:200]}\n\n{_('هل تريد المحاولة مرة أخرى؟')}"
			result = wx.MessageBox(full_msg, _("خطأ"), style=wx.YES_NO | wx.ICON_ERROR)
			if result == wx.YES:
				self.searchAction(query)
			return False
		
		# Check if result is valid
		if loading_dlg.res is None:
			logger.warning("Search returned None result")
			error_msg = _("تعذر إجراء عملية البحث. لم يتم الحصول على نتائج.")
			result = wx.MessageBox(f"{error_msg}\n\n{_('هل تريد المحاولة مرة أخرى؟')}", _("خطأ"), style=wx.YES_NO | wx.ICON_ERROR)
			if result == wx.YES:
				self.searchAction(query)
			return False
		
		self.search = loading_dlg.res
		titles = self.search.get_titles()
		logger.info(f"Search successful. Found {len(titles)} results")
		self.searchResults.Set(titles)
		self.togleControls()
		try:
			self.searchResults.SetSelection(0)
		except:
			pass
		self.searchResults.SetFocus()
		self.togleDownload()
		self.toglePlay()
		logger.debug("Search action completed successfully")
		return True

	def onSearch(self, event):
		if hasattr(self, "search"):
			self.searchAction(self.search.query)
		else:
			self.searchAction()

	def playVideo(self):
		number = self.searchResults.Selection
		if self.search.get_type(number) == "playlist":

			PlaylistDialog(self, self.search.get_url(number))
			return
		title = self.search.get_title(number)
		url = self.search.get_url(number)
		print(url)
		stream = LoadingDialog(self, _("جاري التشغيل"), get_video_stream, url).res
		gui = MediaGui(self, title, stream, url, True if self.search.get_views(number) is not None else False, results=self.search)
		self.Hide()

	def playAudio(self):
		number = self.searchResults.Selection
		if self.search.get_type(number) == "playlist":
			return
		title = self.search.get_title(number)
		url = self.search.get_url(number)
		stream = LoadingDialog(self, _("جاري التشغيل"), get_audio_stream, url).res
		gui = MediaGui(self, title, stream, url, results=self.search, audio_mode=True)
		self.Hide()


	def onHook(self, event):

		if event.KeyCode == wx.WXK_SPACE and self.search.get_type(self.searchResults.Selection) == "video" and self.FindFocus() == self.searchResults:
			self.favCheck.Value = not self.favCheck.Value
			self.onFavorite(None)
		elif event.KeyCode == wx.WXK_BACK and not type(self.FindFocus()) == MediaGui:
			self.backAction()
		else:
			event.Skip()
	def contextSetup(self):
		self.contextMenu = wx.Menu()

		videoPlayItem = self.contextMenu.Append(-1, _("تشغيل"))
		self.videoPlayItemId = videoPlayItem.GetId()
		audioPlayItem = self.contextMenu.Append(-1, _("التشغيل كمقطع صوتي"))
		self.audioPlayItemId = audioPlayItem.GetId()
		self.downloadMenu = wx.Menu()
		videoItem = self.downloadMenu.Append(-1, _("فيديو"))
		audioMenu = wx.Menu()
		m4aItem = audioMenu.Append(-1, "m4a")
		mp3Item = audioMenu.Append(-1, "mp3")
		self.downloadMenu.AppendSubMenu(audioMenu, _("صوت"))
		self.downloadId = self.contextMenu.AppendSubMenu(self.downloadMenu, _("تنزيل")).GetId()
		directDownloadItem = self.contextMenu.Append(-1, _("التنزيل المباشر...\tctrl+d"))
		self.directDownloadId = directDownloadItem.GetId()
		openChannelItem = self.contextMenu.Append(-1, _("الانتقال إلى القناة"))
		downloadChannelItem = self.contextMenu.Append(-1, _("تنزيل القناة"))
		copyItem = self.contextMenu.Append(-1, _("نسخ رابط المقطع"))
		self.copyItemId = copyItem.GetId()
		webbrowserItem = self.contextMenu.Append(-1, _("الفتح من خلال متصفح الإنترنت"))
		def popup():
			if self.searchResults.Strings != []:
				self.searchResults.PopupMenu(self.contextMenu)
		self.searchResults.Bind(wx.EVT_MENU, lambda event: self.playVideo(), id=self.videoPlayItemId)
		self.searchResults.Bind(wx.EVT_MENU, lambda event: self.playAudio(), id=self.audioPlayItemId)
		self.searchResults.Bind(wx.EVT_MENU, self.onOpenChannel, openChannelItem)
		self.searchResults.Bind(wx.EVT_MENU, self.onDownloadChannel, downloadChannelItem)
		self.Bind(wx.EVT_MENU, self.onCopy, copyItem)
		self.Bind(wx.EVT_MENU, self.onOpenInBrowser, webbrowserItem)
		self.searchResults.Bind(wx.EVT_CONTEXT_MENU, lambda event: popup())
		self.Bind(wx.EVT_MENU, self.onVideoDownload, videoItem)
		self.Bind(wx.EVT_MENU, self.onM4aDownload, m4aItem)
		self.Bind(wx.EVT_MENU, self.onMp3Download, mp3Item)
		self.Bind(wx.EVT_MENU, lambda event: self.directDownload(), directDownloadItem)

	def onOpenChannel(self, event):
		n = self.searchResults.Selection
		webbrowser.open(self.search.get_channel(n)["url"])
	def onDownloadChannel(self, event):
		n = self.searchResults.Selection
		channel = self.search.get_channel(n)
		title = channel["name"]
		url = channel["url"]
		download_type = "channel"
		dlg = DownloadProgress(wx.GetApp().GetTopWindow(), title)
		direct_download(int(config_get('defaultformat')), url, dlg, download_type)

	def onOpenInBrowser(self, event):
		number = self.searchResults.Selection
		url = self.search.get_url(number)
		webbrowser.open(url)
	def onDownload(self, event):
		downloadMenu = wx.Menu()
		videoItem = downloadMenu.Append(-1, _("فيديو"))
		audioMenu = wx.Menu()
		m4aItem = audioMenu.Append(-1, "m4a")
		mp3Item = audioMenu.Append(-1, "mp3")
		downloadMenu.Append(-1, _("صوت"), audioMenu)
		self.Bind(wx.EVT_MENU, self.onVideoDownload, videoItem)
		self.Bind(wx.EVT_MENU, self.onM4aDownload, m4aItem)
		self.Bind(wx.EVT_MENU, self.onMp3Download, mp3Item)
		self.PopupMenu(downloadMenu)

	def onM4aDownload(self, event):
		url = self.search.get_url(self.searchResults.Selection)
		title = self.search.get_title(self.searchResults.Selection)
		download_type = self.search.get_type(self.searchResults.Selection)
		dlg = DownloadProgress(wx.GetApp().GetTopWindow(), title)
		direct_download(1, url, dlg, download_type)

	def onMp3Download(self, event):
		url = self.search.get_url(self.searchResults.Selection)
		title = self.search.get_title(self.searchResults.Selection)
		download_type = self.search.get_type(self.searchResults.Selection)
		dlg = DownloadProgress(wx.GetApp().GetTopWindow(), title)
		direct_download(2, url, dlg, download_type)

	def onVideoDownload(self, event):
		url = self.search.get_url(self.searchResults.Selection)
		title = self.search.get_title(self.searchResults.Selection)
		download_type = self.search.get_type(self.searchResults.Selection)
		dlg = DownloadProgress(wx.GetApp().GetTopWindow(), title)
		direct_download(0, url, dlg, download_type)



	def onCopy(self, event):
		pyperclip.copy(self.search.get_url(self.searchResults.Selection))
		wx.MessageBox(_("تم نسخ رابط المقطع بنجاح"), _("اكتمال"), parent=self)
	def loadMore(self):
		if self.searchResults.Strings == []:
			return
		speak(_("جاري تحميل المزيد من النتائج"))
		if self.search.load_more() is None:
			speak(_("لم يتمكن البرنامج من تحميل المزيد من النتائج"))
			return
		# position = self.searchResults.Selection
		wx.CallAfter(self.searchResults.Append, self.search.get_last_titles())
		speak(_("تم تحميل المزيد من نتائج البحث"))
		wx.CallAfter(self.searchResults.SetFocus)
	def onListBox(self, event):
		self.togleDownload()
		self.toglePlay()
		self.togleFavorite()
		if self.searchResults.Selection == len(self.searchResults.Strings)-1:
			if not config_get("autoload"):
				self.loadMoreButton.Enabled = True
				return
			Thread(target=self.loadMore).start()
		else:
			self.loadMoreButton.Enabled = False
	def onLoadMore(self, event):
		Thread(target=self.loadMore).start()
	def backAction(self):
		self.Destroy()
		self.Parent.Show()
	def togleControls(self):
		if self.searchResults.Strings == []:
			for control in self.panel.GetChildren():
				if control.Name == "controls":
					control.Hide()
			self.loadMoreButton.Hide()
		else:
			for control in self.panel.GetChildren():
				if control.Name == "controls":
					control.Show()
			self.loadMoreButton.Show(not config_get("autoload"))
	def togleDownload(self):
		n = self.searchResults.Selection
		if self.search.get_views(n) is None and self.search.get_type(n) == "video":
			self.contextMenu.Enable(self.downloadId, False)
			self.contextMenu.Enable(self.directDownloadId, False)
			self.downloadButton.Enabled = False
			return
		self.contextMenu.Enable(self.downloadId, True)
		self.contextMenu.Enable(self.directDownloadId, True)
		self.downloadButton.Enabled = True

	def toglePlay(self):
		n = self.searchResults.Selection
		contextMenuIds = (self.videoPlayItemId, self.audioPlayItemId)
		if self.search.get_type(n) == "playlist":
			self.playButton.Label = _("فتح")
			for i in contextMenuIds:
				self.contextMenu.Enable(i, False)
			return
			self.playButton.Enabled = True
			for i in contextMenuIds:
				self.contextMenu.Enable(i, True)
	def onFavorite(self, event):
		n = self.searchResults.Selection
		url = self.search.get_url(n)
		if self.favCheck.Value:
			title = self.search.get_title(n)
			display_title = f"{title}. {self.search.get_channel(n)['name']}"
			channel_url = self.search.get_channel(n)['url']
			channel_name = self.search.get_channel(n)['name']
			live = 1 if not self.search.get_views(n) else 0
			data = {"title": title, "display_title": display_title, "url": url, "live": live, "channel_url": channel_url, "channel_name": channel_name}
			self.favorites.add_favorite(data)
			speak(_("تمت إضافة الفيديو إلى قائمة المفضلة"))
		else:
			self.favorites.remove_favorite(url)
			speak(_("تم حذف الفيديو من قائمة المفضلة"))

	def togleFavorite(self):
		n = self.searchResults.Selection
		self.favCheck.Enabled = self.search.get_type(n) == "video"
		if not self.favCheck.Enabled:
			return
		rows = self.favorites.get_all()
		url = self.search.get_url(n)
		def check_url(url):
			for row in rows:
				if url == row["url"]:
					wx.CallAfter(self.favCheck.SetValue, True)
					break
			else:
					wx.CallAfter(self.favCheck.SetValue, False)
		Thread(target=check_url, args=[url]).start()

	def directDownload(self):
		n = self.searchResults.Selection
		if self.search.get_views(n) is None and self.search.get_type(n) == "video":
			return
		url = self.search.get_url(self.searchResults.Selection)
		title = self.search.get_title(self.searchResults.Selection)
		download_type = self.search.get_type(self.searchResults.Selection)
		dlg = DownloadProgress(wx.GetApp().GetTopWindow(), title)
		direct_download(int(config_get('defaultformat')), url, dlg, download_type)
	def onShow(self, event):
		self.searchResults.SetFocus()
