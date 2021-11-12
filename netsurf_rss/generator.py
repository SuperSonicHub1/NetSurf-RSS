from datetime import datetime
from urllib.parse import urljoin
from dateutil import parser
from rfeed import Guid, Item, Feed
from requests import Session
from selectolax.parser import HTMLParser, Node
from .extensions import WebfeedsIcon, Webfeeds

session = Session()
URL = "https://www.netsurf-browser.org/about/news.html"

def generate_item(node: Node):
	description_node = node.next.next

	title_node =  node.css_first("a")
	date_node = node.css_first("span")

	title = title_node.text()
	link = urljoin(
		"https://www.netsurf-browser.org/",
		title_node.attributes["href"]
	)
	published = parser.parse(date_node.text())
	# Selectolax, why can't I just get the inner HTML of a node?!
	description = "".join(
		map(lambda x: x.html, description_node.iter(include_text=True))
	)

	info = {
		"title": title,
		"link": link,
		"guid": Guid(link),
		"pubDate": published,
		"author": "NetSurf Developers",
		"description": description
	}
	
	return Item(**info)

def create_feed():
	res = session.get(URL)
	text = res.text
	tree = HTMLParser(text)
	
	icon = WebfeedsIcon("https://www.netsurf-browser.org/webimages/favicon.png")

	DESCRIPTION = "Small as a mouse, fast as a cheetah and available for free. NetSurf is a multi-platform web browser for RISC OS, UNIX-like platforms (including Linux), Mac OS X, and more."

	info = {
		"title": "NetSurf",
		"description": DESCRIPTION,
		"link": URL,
		"items": map(generate_item, tree.css("dl.news dt")),
		"extensions": [Webfeeds(),  icon,],
		"lastBuildDate": datetime.now(),
	}

	return Feed(**info)
