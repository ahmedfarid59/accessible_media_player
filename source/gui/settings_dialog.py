import os
import sys

import wx
from settings_handler import config_get, config_set, set_file_association
from language_handler import supported_languages


languages = {index:language for language, index in enumerate(supported_languages.values())}

class SettingsDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, title=_("الإعدادات"))
		self.SetSize(500, 500)
		self.Centre()
		self.preferences = {}
		panel = wx.Panel(self)
		lbl = wx.StaticText(panel, -1, _("لغة البرنامج: "), name="language")
		self.languageBox = wx.Choice(panel, -1, name="language")
		self.languageBox.Set(list(supported_languages.keys()))
		try:
			self.languageBox.Selection = languages[config_get("lang")]
		except KeyError:
			self.languageBox.Selection = 0
		lbl1 = wx.StaticText(panel, -1, _("مسار مجلد التنزيل: "), name="path")
		self.pathField = wx.TextCtrl(panel, -1, value=config_get("path"), name="path", style=wx.TE_READONLY|wx.TE_MULTILINE|wx.HSCROLL)
		changeButton = wx.Button(panel, -1, _("&تغيير المسار"), name="path")
		preferencesBox = wx.StaticBox(panel, -1, _("التفضيلات العامة"))
		self.autoDetectItem = wx.CheckBox(preferencesBox, -1, _("اكتشاف الروابط تلقائيًا عند فتح البرنامج"), name="autodetect")
		self.autoCheckForUpdates = wx.CheckBox(preferencesBox, -1, _("الكشف عن التحديثات الجديدة تلقائيًا عند فتح البرنامج"), name="checkupdates")
		self.autoLoadItem = wx.CheckBox(preferencesBox, -1, _("تحميل المزيد من نتائج البحث عند الوصول إلى نهاية قائمة الفيديوهات المعروضة"), name="autoload")
		self.autoCheckForUpdates.SetValue(config_get("checkupdates"))
		self.autoDetectItem.SetValue(config_get("autodetect"))
		self.autoLoadItem.SetValue(config_get("autoload"))
		downloadPreferencesBox = wx.StaticBox(panel, -1, _("إعدادات التنزيل"))
		lbl2 = wx.StaticText(downloadPreferencesBox, -1, _("صيغة التحميل المباشر: "))
		self.formats = wx.Choice(downloadPreferencesBox, -1, choices=[_("فيديو (mp4)"), _("صوت (m4a)"), _("صوت (mp3)")])
		self.formats.Selection = int(config_get('defaultformat'))
		lbl3 = wx.StaticText(downloadPreferencesBox, -1, _("جودة تحويل ملفات mp3: "))
		self.mp3Quality = wx.Choice(downloadPreferencesBox, -1, choices=["96 kbps", "128 kbps", "192 kbps"], name="conversion")
		self.mp3Quality.Selection = int(config_get("conversion"))
		playerOptions = wx.StaticBox(panel, -1, _("إعدادات المشغل"))
		self.continueWatching = wx.CheckBox(playerOptions, -1, _("متابعة المشاهدة بعد إغلاق الفيديو وتشغيله من جديد"), name="continue")
		self.continueWatching.Value = config_get("continue")
		self.repeateTracks = wx.CheckBox(playerOptions, -1, _("إعادة تشغيل المقطع تلقائيًا عند انتهائه"), name="repeatetracks")
		self.autoPlayNext = wx.CheckBox(playerOptions, -1, _("الانتقال إلى المقطع التالي تلقائيًا عند انتهاء المقطع الحالي"), name="autonext")
		self.autoPlayNext.Value = config_get('autonext')
		self.repeateTracks.Value = config_get("repeatetracks")
		
		# File associations panel
		fileAssocBox = wx.StaticBox(panel, -1, _("ربط صيغ الملفات بالمشغل"))
		videoFormatsLabel = wx.StaticText(fileAssocBox, -1, _("صيغ الفيديو: "))
		self.assoc_mp4 = wx.CheckBox(fileAssocBox, -1, "MP4", name="assoc_mp4")
		self.assoc_avi = wx.CheckBox(fileAssocBox, -1, "AVI", name="assoc_avi")
		self.assoc_mkv = wx.CheckBox(fileAssocBox, -1, "MKV", name="assoc_mkv")
		self.assoc_webm = wx.CheckBox(fileAssocBox, -1, "WEBM", name="assoc_webm")
		self.assoc_flv = wx.CheckBox(fileAssocBox, -1, "FLV", name="assoc_flv")
		audioFormatsLabel = wx.StaticText(fileAssocBox, -1, _("صيغ الصوت: "))
		self.assoc_mp3 = wx.CheckBox(fileAssocBox, -1, "MP3", name="assoc_mp3")
		self.assoc_m4a = wx.CheckBox(fileAssocBox, -1, "M4A", name="assoc_m4a")
		self.assoc_wav = wx.CheckBox(fileAssocBox, -1, "WAV", name="assoc_wav")
		self.assoc_flac = wx.CheckBox(fileAssocBox, -1, "FLAC", name="assoc_flac")
		self.assoc_ogg = wx.CheckBox(fileAssocBox, -1, "OGG", name="assoc_ogg")
		
		# Set current values
		self.assoc_mp4.Value = config_get("assoc_mp4")
		self.assoc_avi.Value = config_get("assoc_avi")
		self.assoc_mkv.Value = config_get("assoc_mkv")
		self.assoc_webm.Value = config_get("assoc_webm")
		self.assoc_flv.Value = config_get("assoc_flv")
		self.assoc_mp3.Value = config_get("assoc_mp3")
		self.assoc_m4a.Value = config_get("assoc_m4a")
		self.assoc_wav.Value = config_get("assoc_wav")
		self.assoc_flac.Value = config_get("assoc_flac")
		self.assoc_ogg.Value = config_get("assoc_ogg")
		
		okButton = wx.Button(panel, wx.ID_OK, _("مواف&ق"), name="ok_cancel")
		okButton.SetDefault()
		cancelButton = wx.Button(panel, wx.ID_CANCEL, _("إل&غاء"), name="ok_cancel")
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer1 = wx.BoxSizer(wx.HORIZONTAL)
		sizer2 = wx.BoxSizer(wx.HORIZONTAL)
		sizer3 = wx.BoxSizer(wx.HORIZONTAL)
		sizer4 = wx.BoxSizer(wx.VERTICAL)
		sizer5 = wx.BoxSizer(wx.HORIZONTAL)
		sizer6 = wx.BoxSizer(wx.HORIZONTAL)
		sizer7 = wx.BoxSizer(wx.HORIZONTAL)
		sizer8 = wx.BoxSizer(wx.VERTICAL)  # File association sizer
		okCancelSizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer1.Add(lbl, 1)
		sizer1.Add(self.languageBox, 1, wx.EXPAND)
		for control in panel.GetChildren():
			if control.Name == "ok_cancel":
				okCancelSizer.Add(control, 1)
			elif control.Name == "path":
				sizer2.Add(control, 1)
		for item in preferencesBox.GetChildren():
			sizer3.Add(item, 1)
		preferencesBox.SetSizer(sizer3)
		sizer5.Add(lbl3, 1)
		sizer5.Add(self.mp3Quality, 1)
		sizer6.Add(lbl2, 1)
		sizer6.Add(self.formats, 1)
		sizer4.Add(sizer5)
		sizer4.Add(sizer6)
		downloadPreferencesBox.SetSizer(sizer4)
		for ctrl in playerOptions.GetChildren():
			sizer7.Add(ctrl, 1)
		playerOptions.SetSizer(sizer7)
		
		# File association sizer layout
		videoFormatsSizer = wx.BoxSizer(wx.HORIZONTAL)
		videoFormatsSizer.Add(videoFormatsLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		videoFormatsSizer.Add(self.assoc_mp4, 0, wx.RIGHT, 5)
		videoFormatsSizer.Add(self.assoc_avi, 0, wx.RIGHT, 5)
		videoFormatsSizer.Add(self.assoc_mkv, 0, wx.RIGHT, 5)
		videoFormatsSizer.Add(self.assoc_webm, 0, wx.RIGHT, 5)
		videoFormatsSizer.Add(self.assoc_flv, 0)
		
		audioFormatsSizer = wx.BoxSizer(wx.HORIZONTAL)
		audioFormatsSizer.Add(audioFormatsLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		audioFormatsSizer.Add(self.assoc_mp3, 0, wx.RIGHT, 5)
		audioFormatsSizer.Add(self.assoc_m4a, 0, wx.RIGHT, 5)
		audioFormatsSizer.Add(self.assoc_wav, 0, wx.RIGHT, 5)
		audioFormatsSizer.Add(self.assoc_flac, 0, wx.RIGHT, 5)
		audioFormatsSizer.Add(self.assoc_ogg, 0)
		
		sizer8.Add(videoFormatsSizer, 0, wx.EXPAND | wx.ALL, 5)
		sizer8.Add(audioFormatsSizer, 0, wx.EXPAND | wx.ALL, 5)
		fileAssocBox.SetSizer(sizer8)
		
		sizer.Add(sizer1, 1, wx.EXPAND)
		sizer.Add(sizer2, 1, wx.EXPAND)
		sizer.Add(preferencesBox, 1, wx.EXPAND)
		sizer.Add(downloadPreferencesBox, 1, wx.EXPAND)
		sizer.Add(playerOptions, 1, wx.EXPAND)
		sizer.Add(fileAssocBox, 1, wx.EXPAND)
		sizer.Add(okCancelSizer, 1, wx.EXPAND)
		panel.SetSizer(sizer)
		changeButton.Bind(wx.EVT_BUTTON, self.onChange)
		self.autoDetectItem.Bind(wx.EVT_CHECKBOX, self.onCheck)
		self.autoLoadItem.Bind(wx.EVT_CHECKBOX, self.onCheck)
		self.autoCheckForUpdates.Bind(wx.EVT_CHECKBOX, self.onCheck)
		self.repeateTracks.Bind(wx.EVT_CHECKBOX, self.onCheck)
		self.autoPlayNext.Bind(wx.EVT_CHECKBOX, self.onCheck)
		self.continueWatching.Bind(wx.EVT_CHECKBOX, self.onCheck)
		
		# Bind file association checkboxes
		self.assoc_mp4.Bind(wx.EVT_CHECKBOX, self.onFileAssocCheck)
		self.assoc_avi.Bind(wx.EVT_CHECKBOX, self.onFileAssocCheck)
		self.assoc_mkv.Bind(wx.EVT_CHECKBOX, self.onFileAssocCheck)
		self.assoc_webm.Bind(wx.EVT_CHECKBOX, self.onFileAssocCheck)
		self.assoc_flv.Bind(wx.EVT_CHECKBOX, self.onFileAssocCheck)
		self.assoc_mp3.Bind(wx.EVT_CHECKBOX, self.onFileAssocCheck)
		self.assoc_m4a.Bind(wx.EVT_CHECKBOX, self.onFileAssocCheck)
		self.assoc_wav.Bind(wx.EVT_CHECKBOX, self.onFileAssocCheck)
		self.assoc_flac.Bind(wx.EVT_CHECKBOX, self.onFileAssocCheck)
		self.assoc_ogg.Bind(wx.EVT_CHECKBOX, self.onFileAssocCheck)
		
		okButton.Bind(wx.EVT_BUTTON, self.onOk)
		self.ShowModal()
	def onCheck(self, event):
		obj = event.EventObject
		if all((self.repeateTracks.Value, self.autoPlayNext.Value)) and obj in (self.repeateTracks, self.autoPlayNext):
			self.repeateTracks.Value = self.autoPlayNext.Value = False
		if obj.Name in self.preferences and config_get(obj.Name) == obj.Value:
			del self.preferences[obj.Name]
		elif not obj.Value == config_get(obj.Name):
			self.preferences[obj.Name] = obj.Value
	def onChange(self, event):
		new = wx.DirSelector(_("اختر مجلد التنزيل"), os.path.join(os.getenv("userprofile"), "downloads"), parent=self)
		if not new == "":
			self.preferences['path'] = new
			self.pathField.Value = new
			self.pathField.SetFocus()
	
	def onFileAssocCheck(self, event):
		obj = event.EventObject
		extension = obj.Name.replace("assoc_", "")
		if obj.Name in self.preferences and config_get(obj.Name) == obj.Value:
			del self.preferences[obj.Name]
		elif not obj.Value == config_get(obj.Name):
			self.preferences[obj.Name] = obj.Value
	
	def onOk(self, event):
		# Apply file associations first
		file_extensions = ["mp4", "avi", "mkv", "webm", "flv", "mp3", "m4a", "wav", "flac", "ogg"]
		for ext in file_extensions:
			checkbox_name = f"assoc_{ext}"
			if checkbox_name in self.preferences:
				set_file_association(ext, self.preferences[checkbox_name])
		
		# Apply other preferences
		for key, item in self.preferences.items():
			if not key.startswith("assoc_"):
				config_set(key, item)
		
		if not self.mp3Quality.Selection == int(config_get("conversion")):
			config_set("conversion", self.mp3Quality.Selection)
		config_set("defaultformat", self.formats.Selection) if not self.formats.Selection == int(config_get('defaultformat')) else None
		lang = {value:key for key, value in languages.items()}
		if not lang[self.languageBox.Selection] == config_get("lang"):
			config_set("lang", lang[self.languageBox.Selection])
			msg = wx.MessageBox(_("لقد قمت بتغيير لغة البرنامج إلى {}, مما يعني أنه ينبغي عليك إعادة تشغيل البرنامج لتطبيق التعديلات. هل تريد القيام بذلك حالًا?").format(self.languageBox.StringSelection), _("تنبيه"), style=wx.YES_NO, parent=self)
			os.execl(sys.executable, sys.executable, *sys.argv) if msg == 2 else None
		self.Destroy()
