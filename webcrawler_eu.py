from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

base_url = "https://www.europarl.europa.eu/news/en/press-room/page/"
page_number = 0
urls = [base_url + str(page_number)]
seen = [base_url + str(page_number)]
opened = []
crisis_links = []

maxNumUrl = 150
print("Starting with url=" + str(urls))

while len(urls) > 0 and len(crisis_links) < 10 and len(opened) < maxNumUrl:
    try:
        curr_url = urls.pop(0)
        req = urllib.request.Request(curr_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= " + curr_url)
        print(ex)
        continue

    soup = BeautifulSoup(webpage, 'html.parser')

    text = soup.get_text().lower().replace('-', ' ').replace(',', ' ').replace('.', ' ').replace('\n', ' ').split()
    plenary_session_tag = soup.find('span', class_='ep_name', text='Plenary session')
    if 'crisis' in text and plenary_session_tag:
        crisis_links.append(curr_url)

    for tag in soup.find_all('a', href=True):
        childUrl = tag['href']
        childUrl = urllib.parse.urljoin(base_url, childUrl)
        if base_url in childUrl and childUrl not in seen:
            urls.append(childUrl)
            seen.append(childUrl)

    if len(crisis_links) < 10:
        page_number += 1
        next_page_url = base_url + str(page_number)
        if next_page_url not in seen:
            urls.append(next_page_url)
            seen.append(next_page_url)

print("num. of URLs seen = %d, and scanned = %d" % (len(seen), len(opened)))
print(f'num. of URLs contain crisis and related to plenary sessions = {len(crisis_links)}')

print("List of URLs contain crisis and related to plenary sessions:")
for crisis_url in crisis_links:
    print(crisis_url)
