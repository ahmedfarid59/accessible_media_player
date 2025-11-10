import sqlite3 as sql
from paths import db_path
import os

def db_init():
	try:
		con = sql.connect(db_path)
	except Exception as e:
		print(e)
		con = None
	return con


def is_valid(function):
	def rapper(*args, **kwargs):
		if con is not None:
			return function(*args, **kwargs)
	return rapper

@is_valid
def prepare_tables():
	favorites_query = """create table if not exists favorite (
		id integer primary key, 
		title text not null, 
		display_title text not null, 
		url text not null, 
		is_live integer not null, 
		channel_name text not null, 
		channel_url not null,
		type text default 'video',
		item_count integer default 0
	)"""
	con.execute(favorites_query)
	# Add type and item_count columns to existing tables
	try:
		con.execute("ALTER TABLE favorite ADD COLUMN type text default 'video'")
	except:
		pass  # Column already exists
	try:
		con.execute("ALTER TABLE favorite ADD COLUMN item_count integer default 0")
	except:
		pass  # Column already exists
	con.commit()
	continue_quiry = "create table if not exists continue (id integer primary key, url text not null, position real not null)"
	con.execute(continue_quiry)
	con.commit()

@is_valid
def disconnect():
	con.close()

class Favorite:
	@is_valid
	def add_favorite(self, data):
		# Support for videos, playlists, and folders
		item_type = data.get('type', 'video')
		item_count = data.get('item_count', 0)
		
		query = f"""insert into favorite (title, display_title, url, is_live, channel_name, channel_url, type, item_count) 
values ("{data['title']}", "{data['display_title']}" ,"{data['url']}", {data.get('live', 0)}, "{data.get('channel_name', '')}", "{data.get('channel_url', '')}", "{item_type}", {item_count})"""
		con.execute(query)
		con.commit()

	@is_valid
	def remove_favorite(self, url):
		con.execute(f'delete from favorite where url="{url}"')
		con.commit()
	@is_valid
	def get_all(self):
		cursor = con.execute("select title, display_title, url, is_live, channel_name, channel_url, type, item_count from favorite").fetchall()
		data = []
		for title, display_title, url, live, channel_name, channel_url, item_type, item_count in cursor:
			row = {
				"title": title,
				"display_title": display_title,
				"url": url,
				"live": live,
				"channel_name": channel_name,
				"channel_url": channel_url,
				"type": item_type or "video",  # Default to video if None
				"item_count": item_count or 0
			}
			data.append(row)
		return data


class Continue:
	@classmethod
	@is_valid
	def new_continue(self, url, position):
		quiry = f"""insert into continue (url, position)
values ("{url}", {position})"""
		con.execute(quiry)
		con.commit()
	@classmethod
	@is_valid
	def get_all(self):
		cursor = con.execute("select url, position from continue").fetchall()
		data = {}
		for url, position in cursor:
			data[url] = position
		return data

	@classmethod
	@is_valid
	def update(self, url, position):
		quiry = f"""update continue 
set position={position} where url="{url}"
"""
		con.execute(quiry)
		con.commit()

	@classmethod
	@is_valid
	def remove_continue(self, url):
		con.execute(f'delete from continue where url="{url}"')
		con.commit()


con = db_init()
prepare_tables()