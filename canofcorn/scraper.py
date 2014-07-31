import bs4
import urllib2
import re

def get_base_url():
  """ Return the MLB XML database url"""
  return 'http://gd2.mlb.com/components/game/mlb/'

def url_to_soup(url):
  """ For a given url, return BeautifulSoup of the data."""
  resp = urllib2.urlopen(url)
  data = resp.read()
  soup = bs4.BeautifulSoup(data)
  return soup

def get_year_urls(year_start = 2003, year_end = 2014):
  url = get_base_url()
  soup = url_to_soup(url)
  year_urls = []
  for tag in soup.find_all('li'):
    # Match things like year_2014 but not old_year2004
    match = re.match('.*year_[0-9]{4}', tag.text)
    if not match:
      continue
    year = match.group().split("_")[1]
    year = int(year)
    if 'year' in tag.text and year_start <= year <= year_end:
      year_urls.append(url + tag.a['href'])
  return year_urls

def get_urls_with_re(url, regex=''):
  """ Read the target 'url' and grab all <li> tags. Apply the regular
  expression filter 'regex' to the resulting tag text.
  """
  soup = url_to_soup(url)
  urls = []
  for tag in soup.find_all('li'):
    match = re.match(regex, tag.text)
    if match:
      urls.append(url + tag.a['href'])
  return urls


