import configparser
import os
from language_handler import get_default_language
from paths import settings_path
from logger_config import get_logger

logger = get_logger(__name__)

# settings_path = os.path.join(os.getenv("appdata"), "Accessible Media Player")

defaults = {
	"path": f"{os.getenv('USERPROFILE')}\\downloads\\Accessible Media Player",
	"defaultaudio": 0,
	"lang": get_default_language(),
	"autodetect": True,
	"checkupdates": True,
	"autoload": True,
	"seek": 5,
	"conversion": 1,
	"repeatetracks":False,
	"autonext": False,
	"defaultformat": 0,
	"volume": 100,
	"continue": True,
	# File associations
	"assoc_mp4": False,
	"assoc_avi": False,
	"assoc_mkv": False,
	"assoc_webm": False,
	"assoc_flv": False,
	"assoc_mp3": False,
	"assoc_m4a": False,
	"assoc_wav": False,
	"assoc_flac": False,
	"assoc_ogg": False,
}

def config_initialization():
	try:
		os.mkdir(settings_path)
	except FileExistsError:
		pass
	if not os.path.exists(os.path.join(settings_path, "settings.ini")):
		config = configparser.ConfigParser()
		config.add_section("settings")
		for key, value in defaults.items():
			config["settings"][key] = str(value)
		with open(os.path.join(settings_path, "settings.ini"), "w") as file:
			config.write(file)

def string_to_bool(string):
	if string == "True":
		return True
	elif string == "False":
		return False
	else:
		return string


def config_get(string):
	config = configparser.ConfigParser()
	config.read(os.path.join(settings_path, "settings.ini"))
	try:
		value = config["settings"][string]
		return string_to_bool(value)
	except KeyError:
		config_set(string, defaults[string])
		return defaults[string]


def config_set(key, value):
	config = configparser.ConfigParser()
	config.read(os.path.join(settings_path, "settings.ini"))
	config["settings"][key] = str(value)
	with open(os.path.join(settings_path, "settings.ini"), "w") as file:
		config.write(file)


def get_associated_formats():
	"""Get list of file formats that are currently associated with the application"""
	formats = ["mp4", "avi", "mkv", "webm", "flv", "mp3", "m4a", "wav", "flac", "ogg"]
	associated = []
	for fmt in formats:
		if config_get(f"assoc_{fmt}"):
			associated.append(fmt)
	return associated


def set_file_association(extension, enable=True):
	"""Set or remove file association for a specific extension"""
	logger.info(f"{'Enabling' if enable else 'Disabling'} file association for .{extension}")
	import sys
	import winreg
	
	if enable:
		try:
			# Get the path to the Python executable and script
			exe_path = sys.executable
			script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "accessible_media_player.py"))
			logger.debug(f"Python executable: {exe_path}")
			logger.debug(f"Script path: {script_path}")
			
			# Create ProgID key
			prog_id = f"AccessibleMediaPlayer.{extension}"
			logger.debug(f"Creating ProgID: {prog_id}")
			
			# Create file type association
			key_path = f".{extension}"
			key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{key_path}")
			winreg.SetValue(key, "", winreg.REG_SZ, prog_id)
			winreg.CloseKey(key)
			logger.debug(f"Created file type association for {key_path}")
			
			# Create ProgID key with command
			prog_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{prog_id}")
			winreg.SetValue(prog_key, "", winreg.REG_SZ, f"Accessible Media Player - {extension.upper()}")
			
			# Create shell\open\command key
			command_key = winreg.CreateKey(prog_key, "shell\\open\\command")
			command_value = f'"{exe_path}" "{script_path}" "%1"'
			winreg.SetValue(command_key, "", winreg.REG_SZ, command_value)
			winreg.CloseKey(command_key)
			winreg.CloseKey(prog_key)
			logger.debug(f"Created registry command: {command_value}")
			
			config_set(f"assoc_{extension}", True)
			logger.info(f"Successfully enabled file association for .{extension}")
			return True
		except Exception as e:
			logger.error(f"Error setting file association for {extension}: {type(e).__name__}: {str(e)}")
			return False
	else:
		try:
			# Remove file association
			prog_id = f"AccessibleMediaPlayer.{extension}"
			key_path = f".{extension}"
			logger.debug(f"Attempting to remove file association for {key_path}")
			
			# Try to remove the association
			try:
				key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{key_path}", 0, winreg.KEY_READ)
				current_prog_id = winreg.QueryValue(key, "")
				winreg.CloseKey(key)
				
				# Only remove if it's our association
				if current_prog_id == prog_id:
					winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{key_path}")
					logger.debug(f"Removed file type association for {key_path}")
			except Exception as e:
				logger.debug(f"Could not remove file type association: {type(e).__name__}: {str(e)}")
				pass
			
			# Remove ProgID
			try:
				winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{prog_id}\\shell\\open\\command")
				winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{prog_id}\\shell\\open")
				winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{prog_id}\\shell")
				winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{prog_id}")
				logger.debug(f"Removed ProgID registry keys for {prog_id}")
			except Exception as e:
				logger.debug(f"Could not remove ProgID keys: {type(e).__name__}: {str(e)}")
				pass
			
			config_set(f"assoc_{extension}", False)
			logger.info(f"Successfully disabled file association for .{extension}")
			return True
		except Exception as e:
			logger.error(f"Error removing file association for {extension}: {type(e).__name__}: {str(e)}")
			return False

