from tornado import ioloop, web, httpclient
from BeautifulSoup import BeautifulSoup, SoupStrainer
from urlparse import urlparse
import json
import time
import random


print("restarted")


tocrawl = ["legoben.tumblr.com"] #List of blogs to start crawling
apikey = "" #Tumblr Public API Key


class NextBlog(web.RequestHandler):
    def get(self):

        num = random.randint(0, len(tocrawl) - 1) #Get random entry in the tocrawl list.
        turl = tocrawl[num] #The url we'll be using.
        c = self.crawlBlog(turl) #Crawl the blog.
        c.append(turl) #Append the blog to the crawled list.
        open("crawled.json", "w").write(json.dumps(c)) #Put the list in the file.

        ## UNCOMMENT TO ENABLE recent
        
        #client = httpclient.HTTPClient()
        #client.fetch("http://localhost/path/to/recent/?newurlis=" + turl) #Let the recent server know we've crawled this domain.

        del tocrawl[num] #Delete from tocrawl
        self.write("https://www.tumblr.com/ask_form/" + turl) #Send url to the client.
        print(tocrawl) #print tocrawl.

    def crawlBlog(self, url):
        client = httpclient.HTTPClient()
        resp = client.fetch("http://" + url).body #Get the blog URL

        common = ["www.tumblr.com"] #Most blogs will have these URL(s).

        crawled = json.loads(open("crawled.json").read()) #Open crawled log.

        for link in BeautifulSoup(resp, parseOnlyThese=SoupStrainer('a')): #Loop through every link on the page.
            try:
                parse = urlparse(link['href']) #Try to get the anchor's link.
            except Exception:
                continue

            #Checks if there is a hostname, the host name is not in crawled or tocrawl, and it is not a common hostname
            if parse.netloc != '' and parse.netloc not in crawled and parse.netloc not in tocrawl and  parse.netloc not in common:

                url = "http://api.tumblr.com/v2/blog/"+parse.netloc+"/info?api_key=" + apikey #prepare call to Tumblr API
                try:
                    info = json.loads(client.fetch(url).body) #Get tumblr API
                except Exception:
                    info = {"meta":{"status":404,"msg":"Not Found"},"response":[]} #The blog doesn't exist, mock response.

                if info['meta']['status'] != 200:
                    crawled.append(parse.netloc) #Invalid blog, add it to crawled so we don't parse it again and move on.
                    continue

                if info['response']['blog']['ask'] == False:
                    crawled.append(parse.netloc) #Blog's asks are not open, add to crawled and move on.
                    continue

                else:
                    tocrawl.append(parse.netloc) #Blog checks out, add it to tocrawl.

        return crawled #Return list of crawled blogs.




application = web.Application([
    (r"/nextblog", NextBlog),
], debug=True)

if __name__ == "__main__":
    application.listen(9009)
    ioloop.IOLoop.instance().start()


