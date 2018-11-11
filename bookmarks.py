import josn
from bs4 import BeautifulSoup

class Bookmark(object):
	def __init__(self, link, title, read_time, publish_date):
		self.link = link
		self.title = title
		self.read_time = read_time
		self.publish_date = publish_date		
	@classmethod
	def load_from_dom(cls, dom_item):
		anchor_tag = dom_item.find('a', attrs={'class':'link'})
		return cls(
			anchor_tag.get('href'), anchor_tag.text, 
			dom_item.find('span', attrs={'class':'readingTime'}).get('title'),
			dom_item.find('time').get('datetime'))
	def to_dict(self):
		return self.__dict__
	def __str__(self):
		return json.dumps(self.to_dict())

def parse_bookmarks(bookmark_html_file):

	data = open(bookmark_html_file).read()
	soup = BeautifulSoup(data, 'html.parser')
	bookmarks = soup.find_all('div', attrs={'class':'streamItem'})

	parsed_bookmarks = []
	for bookmark in bookmarks:
		b = Bookmark.load_from_dom(bookmark)
		parsed_bookmarks.append(b)
		
	return parsed_bookmarks


