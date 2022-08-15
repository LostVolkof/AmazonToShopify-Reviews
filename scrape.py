from dataclasses import replace
from requests_html import HTMLSession
import json
import time
import emoji




char = int(input('Filter by characters: '))

class Reviws:
    def __init__(self, asin) -> None:
        self.asin = asin
        self.asin = input('Enter ASIN Again: ')
        self.getUrl = input('Enter URL: ')
        self.session = HTMLSession()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
        self.url = f'{self.getUrl}{self.asin}/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&reviewerType=all_reviews&filterByStar=five_star&pageNumber='

    def pagination(self, page):
        r = self.session.get(self.url + str(page), headers=self.headers)
        if not r.html.find('div[data-hook="review"]'):
            return False
        else:
            return r.html.find('div[data-hook="review"]')
    
    def parse(self, reviews):
        total = []
        for review in reviews:
            title = review.find('a[data-hook="review-title"]', first=True).text
            rating = review.find('i[data-hook="review-star-rating"] span', first=True).text
            body = review.find('span[data-hook="review-body"] span', first=True).text.replace('\n',' ').strip()
            date = review.find('span[data-hook="review-date"]', first=True).text

            data = {
                'title': title,
                'rating': rating,
                'body': body[:1000000000],
                'date': date
            }
            if data['body'] == '':
                continue
            if len(data['body']) < char:
                continue
            total.append(data)
        return total
        

    def save(self, results):
        with open(self.asin + '-reviews.json', 'w') as f:
            json.dump(results, f)
        for emote in open(self.asin + '-reviews.json', 'r'):
            emoji.replace_emoji(emote, ' ')

if __name__ == '__main__':
    inputas = input('Enter ASIN: ')
    amz = Reviws(inputas)
    results = []
    for x in range(1, 300):
        print('getting page', x)
        time.sleep(0.3)
        reviews = amz.pagination(x)
        if reviews is not False:
            results.extend(amz.parse(reviews))
        else:
            print('No More Pages')
            break
amz.save(results)
