from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

seed_url = "https://press.un.org/en"
real_url = 'https://press.un.org/en/'

urls = [seed_url]
seen = [seed_url]
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
    if 'crisis' in text:
        crisis_links.append(curr_url)

    for tag in soup.find_all('a', href=True):
        childUrl = tag['href']
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        if real_url in childUrl and childUrl not in seen:
            urls.append(childUrl)
            seen.append(childUrl)

print("num. of URLs seen = %d, and scanned = %d" % (len(seen), len(opened)))
print(f'num. of URLs contain crisis = {len(crisis_links)}')

print("List of URLs contain crisis:")
for crisis_url in crisis_links:
    print(crisis_url)
