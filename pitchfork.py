from bs4 import BeautifulSoup
import csv
import requests 
import time

# configuration
page_start = ""
page_end = ""
doc_save = ""


start = time.time()
url = "https://pitchfork.com/reviews/albums/?page="
doc = open(doc_save, 'w')
f = csv.writer(doc)
f.writerow(["Title", "Artist", "Score", "Author", "Genre", "Date", "Text"]) 
for i in range(page_start, page_end):
    fulllinks = []
    new_url = url + str(i)
    response = requests.get(new_url)
    soup = BeautifulSoup(response.content, "html.parser")
    for link in soup.find_all('a'):
        full = link.get('href')
        if str.startswith(full, "/reviews/albums") and str.endswith(full, "/") and full !="/reviews/albums/":
            fulllinks.append("https://pitchfork.com" + full)
            fulllinks = list(set(fulllinks))
    for fulllink in fulllinks:
        try:
            page_response = requests.get(fulllink)
            page_content = BeautifulSoup(page_response.content, "html.parser")
            title_box = page_content.find("h1", attrs={"class", "single-album-tombstone__review-title"})
            title = title_box.text.strip() 
            score_box = page_content.find("span", attrs={"class", "score"})
            score = score_box.text.strip()
            artist_box = page_content.find("ul", attrs={"class", "artist-links artist-list single-album-tombstone__artist-links"})
            artist = artist_box.text.strip()
            author_box = page_content.find("a", attrs={"class", "authors-detail__display-name"})
            author = author_box.text.strip()
            date_box = page_content.find("time", attrs={"class", "pub-date"})
            date = date_box.text.strip()
            if "hrs" in str(date):
                date = "March 6 2019"
            genre_box = page_content.find("li", attrs={"class", "genre-list__item"})
            genre = genre_box.text.strip()
            text_box = page_content.find("div", attrs={"class", "contents"})
            text = text_box.text.strip()
        except:
            print("error with getting data")
            continue
        try:
            f.writerow([title, artist, score, author, genre, date, text])
        except:
            print("error updating data file")
            continue
end = time.time()
doc.close()
print(end-start) 