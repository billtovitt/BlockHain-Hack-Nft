from itertools import islice
from time import sleep
from snscrape.base import ScraperException
import snscrape.modules.twitter as sntwitter
import termtables, requests, os, sys

summary_data = []
rcount = 1; passes = 10
dn = "Output"

def handle(items):
    for i, tweet in enumerate(islice(items, passes)):
        result = requests.get(tweet.media[0].fullUrl)
        with open(str(tweet.id) + ".png", "wb") as f:
            f.write(result.content)
        summary_data.append([tweet.id, tweet.content[:72], tweet.date.strftime("%d/%m/%Y %H:%M %Z")])

def main():
    global rcount
    while (1):
        try:
            items = sntwitter.TwitterSearchScraper('from:cryptopunksbot').get_items()
            handle(items)
            break
        except ScraperException:
            print("Restart " + str(rcount) + "..."); rcount += 1
            sleep(1.5)

if __name__ == "__main__":
    if (not os.path.isdir(dn)): os.mkdir(dn)
    os.chdir(dn)
    if (len(sys.argv) > 1):
        passes = int(sys.argv[1])
    print("On " + str(passes) + " passes.\nWorking...")
    main()
    with open("log.txt", "w", encoding = "utf-8") as f:
        f.write(termtables.to_string(
            summary_data,
            header = ["ID/Filename", "Content", "Date"],
            style = termtables.styles.double_thin
        ))
    print("Done")
