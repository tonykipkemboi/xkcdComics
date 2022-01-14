import requests, os
import bs4

# download every single XKCD comic
# starting url
url = "https://xkcd.com"
# store comics in ./xkcd
os.makedirs("xkcd", exist_ok=True)

while not url.endswith("#"):
    # download page
    print("Downloading comic page %s..." % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, features="html.parser")

    # find the url of the comic image
    comicElem = soup.select("#comic img")
    if comicElem == []:
        print("Could not find comic image.")
    else:
        comicURL = "https:" + comicElem[0].get("src")
        # download the image
        print("Downloading image %s..." % (comicURL))
        res = requests.get(comicURL)
        res.raise_for_status()

    # save the image to ./xkcd
    imageFile = open(os.path.join("xkcd", os.path.basename(comicURL)), "wb")
    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()

    # get the Prev button's url
    prevLink = soup.select('a[rel="prev"]')[0]
    url = "https://xkcd.com" + prevLink.get("href")

print("Done!")