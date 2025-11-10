from settings_handler import config_get
import os
import application

def documentation_get():
	"""Get the user guide content. Returns markdown content."""
	# Try to get the USER_GUIDE.md from the root directory
	root_guide = os.path.join(os.path.dirname(os.getcwd()), "USER_GUIDE.md")
	
	# If running from built executable, try relative to executable
	if not os.path.exists(root_guide):
		root_guide = os.path.join(os.getcwd(), "USER_GUIDE.md")
	
	# Fallback to old language-specific docs if USER_GUIDE.md not found
	if not os.path.exists(root_guide):
		lang = config_get("lang")
		available_languages = os.listdir("docs") if os.path.exists("docs") else []
		if not lang in available_languages:
			lang = "en"
		path = os.path.join(os.getcwd(), f"docs\\{lang}\\guide.txt")
		if not os.path.exists(path):
			return None
		with open(path, "r", encoding="utf-8") as file:
			namespace = {"name": application.name, "version": application.version, "author": application.author}
			return file.read().format(**namespace)
	
	# Read and return the markdown content
	with open(root_guide, "r", encoding="utf-8") as file:
		content = file.read()
		# Replace version placeholders if any
		namespace = {"name": application.name, "version": application.version, "author": application.author}
		return content.format(**namespace)
