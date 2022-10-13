# grabs HTML files from websites
import requests

# converts the obtained HTML string into object that can be manipulated
from bs4 import BeautifulSoup

# prints items in terminal in an organized manner
import pprint

# grabs the HTML source file of the page (also found in the 'Response' window under 'Network' tab)
res = requests.get('https://news.ycombinator.com/')
# grabs second page
res2 = requests.get('https://news.ycombinator.com/news?p=2')

# all the HTML markup returned 
# print(res.text)

# 'soup' object takes the markup and parses it (data type to parse mentioned in the second argument) 
# removes unnecessary HTML tags
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

# all the tags containing the class 'titleline' are stored as a list
# 'titleline' class contains all the news headline links
links = soup.select('.titleline')
links2 = soup2.select('.titleline')
mega_link = links + links2

# all the tags containing the class 'score' are within the class 'subtext'
# the entire class is stored within the 'subtext' variable as list
subtext = soup.select('.subtext')
subtext2 = soup2.select('.subtext')
mega_subtext = subtext + subtext2

# function to get titles of the news from the website
def create_custom_hackernews(links, subtext):
	hackernews = []
	# 'idx' stores the number given to each tag by '.enumerate(), 'item' stores the <a> tag
	# 'idx' is also used to access the subtext of each links
	for idx, item in enumerate(links):
		# each item here is 'links[idx]' respectively
		# the text of the article within the <a> tag is extracted and stored in the 'title' variable
		title = item.getText()

		# the links of the titles are extracted from 'href' in <a> tag and stored in the 'href' variable
		href = item.get('href')

		# the vote count under each article are extracted
		# in case articles don't have any votes, the list index gets out of range
		# the 'score' class within 'subtext' is selected which contains the number of votes in text
		# articles might not have votes but have 'subtext' class under them preventing out of range error
		votes_string = subtext[idx].select('.score')

		# for when there are no votes the votes_string list has no element so length of the list is zero and is skipped
		if len(votes_string):
			# an array containing one element at a time is created as 'votes_string'
			# the first element contains the contents of the class 'score'
			# the text is extracted which displays the number of votes
			# the returned string is converted to 'int' and the extra bit is removed
			votes_number = int(votes_string[0].getText().replace(' points', ''))

			# votes_number greater than 99 are appended only
			if votes_number > 99:
				hackernews.append({'title': title, 'links': href, 'votes': votes_number})

	return sort_articles_by_votes(hackernews)

# function to sort the votes in descending order
def sort_articles_by_votes(list):
	return sorted(list, key=lambda k:k['votes'], reverse=True)


pprint.pprint(create_custom_hackernews(mega_link, mega_subtext))
