#!/usr/bin/python

import sys
import random
import time
import threading
import string
import urllib
import codecs

from unidecode import unidecode

url_format = "{base}/AskBot/ask?bot=Dent&type=json&username={user}&question={query}"

test_phrases = codecs.open("test_corpus.txt", 'r', 'utf-8').readlines()[1:]

host = "http://localhost:8090"
duration = 60

def random_agent():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10))
    
def format_url(line, url, agent):
    
    # I am sure there is a nicer way for this, but...
    q = urllib.quote_plus(unidecode(line), "")
    
    request = url_format.format(base=url, user=agent, query=q)
    
    return request

def get_rand_line():
    return random.choice(test_phrases)

def worker():
    agent = random_agent()
    start = time.time()
    while ( time.time() - start < duration ):
        q = get_rand_line().split(',')[0]
        req = format_url(q, host, agent)
        response = urllib.urlopen(req).read()
        time.sleep(5)        
    
def main(threads=2):
    ws = []
    for i in xrange(threads):
    	w = threading.Thread(target=worker)
    	ws.append(w)
    	w.start()
    
    # Join them all
    for w in ws:
        w.join()

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: {} HOST THREADS TIME".format(sys.argv[0]))
        sys.exit(1)
    host = sys.argv[1]
    duration = int(sys.argv[3])
    main(threads=int(sys.argv[2]))
