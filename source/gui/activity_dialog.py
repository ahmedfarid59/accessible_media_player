import wx
from threading import Thread
from logger_config import get_logger

logger = get_logger(__name__)

class LoadingDialog(wx.Dialog):
    def __init__(self, parent, msg, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.res = None  # Initialize res to None
        self.error = None  # Store any error that occurs
        logger.debug(f"LoadingDialog created for function: {function.__name__}")
        super().__init__(parent)
        self.CenterOnParent()
        p = wx.Panel(self)
        self.message = wx.StaticText(p, -1, msg)
        self.message.SetCanFocus(True)
        self.message.SetFocus()
        indicator = wx.ActivityIndicator(p)
        indicator.Start()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.message, 1, wx.EXPAND)
        sizer.AddStretchSpacer()
        sizer.Add(indicator, 1, wx.EXPAND)
        sizer.AddStretchSpacer()
        p.SetSizer(sizer)
        self.Bind(wx.EVT_CLOSE, lambda e: wx.Exit())
        self.Bind(wx.EVT_CHAR_HOOK, self.onHook)
        Thread(target=self.run).start()
        self.ShowModal()
    def run(self):
        try:
            logger.info(f"Executing function: {self.function.__name__} with args: {self.args[:2] if len(self.args) > 2 else self.args}")
            self.res = self.function(*self.args, **self.kwargs)
            logger.info(f"Function {self.function.__name__} completed successfully")
            wx.CallAfter(self.Destroy)
        except Exception as e:
            logger.error(f"Function {self.function.__name__} failed: {type(e).__name__}: {str(e)}")
            self.error = e  # Store the error
            wx.CallAfter(self.Destroy)
            # Don't raise here, let the caller handle it
    def onHook(self, event):
        if event.KeyCode in (wx.WXK_DOWN, wx.WXK_UP, wx.WXK_LEFT, wx.WXK_RIGHT):
            self.message.SetFocus()
            return
        event.Skip()
