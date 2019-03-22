from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

# Class LinkParser inherits HTMLParser 
class LinkParser(HTMLParser):

    # Add functions to handle_starttag
    def handle_starttag(self, tag, attrs):
        # look for link <a href=""></a>
        if tag == 'a':
            for (key, value) in attribs:
                if key == 'href':
                    # combine url with value
                    newUrl = parse.urljoin(self.baseUrl, value)
                    # add it to links:
                    self.links = self.links + [newUrl]

    # function to get links
    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        # Use the urlopen function from the standard Python 3 library
        response = urlopen(url)
        # Double check that the response is html
        if response.getheader('Content-Type')=='text/html':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "",[]

# Function to take in a URL, a word to find, and number of pages
def spider(url, word, maxPages):  
    pagesToVisit = [url]
    numberVisited = 0
    foundWord = False
    # Create a LinkParser and get all the links on the page.
    # search page for string
    # In our getLinks function we return the web page
    # and we return a set of links from that web page
    while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
        numberVisited = numberVisited +1
        # Start from the beginning of our collection of pages to visit:
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            print(numberVisited, "Visiting:", url)
            parser = LinkParser()
            data, links = parser.getLinks(url)
            if data.find(word)>-1:
                foundWord = True
                # Add the pages that we visited to the end of our collection
                pagesToVisit = pagesToVisit + links
                print(" **Success!**")
        except:
            print(" **Failed!**")
    if foundWord:
        print("The word", word, "was found at", url)
    else:
        print("Word never found")
