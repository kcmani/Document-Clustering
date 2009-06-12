import feedparser
import re

def getwordcounts(d):
    wc={}
    
    for e in d.entries:
        if 'summary' in e: summary = e.summary
        else: summary = e.description
        
        #Extract a list of words
        words = getwords(e.title+''+summary)
        for word in words:
            wc.setdefault(word,0)
            wc[word]+=1
    return d.feed.title,wc

def getwords(html):
    #Remove all the HTML tags
    txt=re.compile(r'<[^>]+>').sub('',html)
    
    #Split words by all non-alpha characters
    words=re.compile(r'[^A-Z^a-z]+').split(txt)
    
    #Convert to lowercase
    return [word.lower() for word in words if word!='']

apcount={}
wordcounts={}
feedlist=[]
for feedurl in file('feedlist.txt'):
    #parse the feed
    d=feedparser.parse(feedurl)
    if 'feed' not in d or 'title' not in d['feed']:
        continue
    feedlist.append(feedurl)
    title,wc=getwordcounts(d)
    wordcounts[title] = wc
    for word,count in wc.items():
        apcount.setdefault(word,0)
        if count>1:
            apcount[word]+=1

wordlist=[]
for w,bc in apcount.items():
    frac=float(bc)/len(feedlist)
    if frac>0.1 and frac<0.5: wordlist.append(w)

out=file('blogdata.txt','w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordcounts.items():
    #deal with unicode outside the ascii range
    blog=blog.encode('ascii','ignore')
    out.write(blog)
    for word in wordlist:
        if word in wc: out.write('\t%d' % wc[word])
        else: out.write('\t0')
    out.write('\n')
