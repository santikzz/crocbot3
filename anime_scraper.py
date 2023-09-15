import cloudscraper
from bs4 import BeautifulSoup
import re

pattern = r"Capítulo (\d+.\d+)(:(.+))*"

# url = "https://lectortmo.com/library/manga/43882/spy-x-family"
# url = "https://lectortmo.com/library/manga/8635/mushoku-tensei-isekai-ittara-honki-dasu"

def get_manga_info(url):

	scraper = cloudscraper.create_scraper()

	html = scraper.get(url).text

	soup = BeautifulSoup(html, "lxml")

	chapter = soup.find(id="chapters").find("li", class_="list-group-item p-0 bg-light upload-link").find("a").text
	title = soup.find("h2", class_="element-subtitle").text
	image = soup.find("img", class_="book-thumbnail")['src']

	if image.startswith("/cdn-cgi/mirage/"):
		# print("error image /cdn-cgi/mirage/")
		image = re.search(f"(https.*)", image)[1]
		# print(image)
		
	description = soup.find("p", class_="element-description").text

	regex = re.search(pattern, chapter)

	try:
		last_chapter_title = regex[2][2:]
	except:
		last_chapter_title = ""

	chapter = { "last_chapter_number": float(regex[1]), "last_chapter_title": last_chapter_title, "manga_title": title, "manga_description": description, "manga_image": image }
	return chapter


# result = get_manga_info(url)
# print(result)