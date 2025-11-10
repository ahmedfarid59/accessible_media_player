import wx
import re

try:
	import markdown
	MARKDOWN_AVAILABLE = True
except ImportError:
	MARKDOWN_AVAILABLE = False


def markdown_to_plain_text(md_content):
	"""Convert markdown to fully clean plain text with preserved structure."""
	text = md_content
	
	# Remove HTML comments first
	text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
	
	# Remove YAML front matter if present
	text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)
	
	# Remove code blocks but keep content with indentation
	text = re.sub(r'```[\w]*\n(.*?)\n```', lambda m: '\n'.join('    ' + line for line in m.group(1).split('\n')), text, flags=re.DOTALL)
	
	# Convert headers - different levels get different formatting
	text = re.sub(r'^# (.+)$', r'\n\n\1\n' + '=' * 70 + '\n', text, flags=re.MULTILINE)
	text = re.sub(r'^## (.+)$', r'\n\n\1\n' + '-' * 60 + '\n', text, flags=re.MULTILINE)
	text = re.sub(r'^### (.+)$', r'\n\n\1\n' + '·' * 40, text, flags=re.MULTILINE)
	text = re.sub(r'^#### (.+)$', r'\n\n\1:', text, flags=re.MULTILINE)
	text = re.sub(r'^#{5,6} (.+)$', r'\n\1', text, flags=re.MULTILINE)
	
	# Convert bold and italic (remove formatting but keep text)
	text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)  # bold+italic
	text = re.sub(r'___(.+?)___', r'\1', text)  # bold+italic
	text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # bold
	text = re.sub(r'__(.+?)__', r'\1', text)  # bold
	text = re.sub(r'\*(.+?)\*', r'\1', text)  # italic
	text = re.sub(r'_(.+?)_', r'\1', text)  # italic
	
	# Convert inline code
	text = re.sub(r'`([^`]+)`', r'"\1"', text)
	
	# Convert links - show text and URL
	text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'\1 (\2)', text)
	
	# Convert images - show alt text
	text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'[Image: \1]', text)
	
	# Convert bullet lists with proper indentation
	text = re.sub(r'^(\s*)[-*+]\s+', r'\1• ', text, flags=re.MULTILINE)
	
	# Convert numbered lists - preserve numbers
	text = re.sub(r'^(\s*)(\d+)\.\s+', r'\1\2. ', text, flags=re.MULTILINE)
	
	# Convert blockquotes
	text = re.sub(r'^>\s+(.+)$', r'    \1', text, flags=re.MULTILINE)
	
	# Convert horizontal rules
	text = re.sub(r'^[-*_]{3,}\s*$', '\n' + '-' * 70 + '\n', text, flags=re.MULTILINE)
	
	# Remove reference-style link definitions
	text = re.sub(r'^\[.+?\]:\s+.+$', '', text, flags=re.MULTILINE)
	
	# Clean up table formatting (convert to simple text)
	# Remove table header separators
	text = re.sub(r'^\|?[-:\s|]+\|?\s*$', '', text, flags=re.MULTILINE)
	# Simplify table rows
	text = re.sub(r'^\|(.+)\|\s*$', r'\1', text, flags=re.MULTILINE)
	text = re.sub(r'\|', ' | ', text)
	
	# Remove escape characters
	text = re.sub(r'\\([\\`*_{}[\]()#+\-.!])', r'\1', text)
	
	# Clean up multiple blank lines (max 2)
	text = re.sub(r'\n{4,}', '\n\n\n', text)
	
	# Clean up spaces before punctuation
	text = re.sub(r'\s+([.,;:!?])', r'\1', text)
	
	# Remove trailing spaces
	text = re.sub(r' +$', '', text, flags=re.MULTILINE)
	
	return text.strip()


class Viewer(wx.Dialog):
	def __init__(self, parent, title, content):
		wx.Dialog.__init__(self, parent, title=title)
		self.Centre()
		self.Maximize(True)
		sizer = wx.BoxSizer(wx.VERTICAL)
		panel = wx.Panel(self)
		
		# Check if content looks like markdown (contains markdown syntax)
		is_markdown = MARKDOWN_AVAILABLE and ('##' in content or '**' in content or '```' in content or '[' in content and '](' in content)
		
		if is_markdown:
			# Convert markdown to plain text for better navigation
			plain_content = markdown_to_plain_text(content)
			viewer = wx.TextCtrl(panel, -1, value=plain_content, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_WORDWRAP)
		else:
			# Use text control for plain text
			viewer = wx.TextCtrl(panel, -1, value=content, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_WORDWRAP)
		
		# Set a larger, more readable font
		font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
		viewer.SetFont(font)
		
		closeButton = wx.Button(panel, -1, _("إغلاق"))
		closeButton.Bind(wx.EVT_BUTTON, lambda event: self.Destroy())
		sizer.Add(closeButton, 0)
		sizer.Add(viewer, 1, wx.EXPAND)
		panel.SetSizer(sizer)
		self.Bind(wx.EVT_CHAR_HOOK, self.onEscape)
	
	def onEscape(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.Destroy()
		event.Skip()


