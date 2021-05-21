from bs4 import BeautifulSoup
import requests
import csv
import time


class Guitar:
    results = []
    headers = { "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding":" gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "dnt": "1",
                "pragma": "no-cache",
                "referer":" https://www.thebassplace.com/product-category/basses/4-string/",
               " sec-ch-ua":' "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                "sec-ch-ua-mobile":" ?0",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
                }

    def fetch(self, url):
        print("Http get url: %s"% url, end = " ")
        res = requests.get(url)
        print("Status_code : %s" %res.status_code)

        return res

    def parse(self, html):
        content = BeautifulSoup(html, "lxml")
        products = content.find_all('li', {'class': 'product-grid-view '})
        
        for product in products:
            self.results.append({
            	'image': product.find('img')['src'],
                'title': product.find('h3', {'class': 'product-title'}).text.strip(),
                'price': product.find('div', {'class': 'fusion-price-rating'}).text.strip(),
                'details': product.find('a')['href']
            })

    def to_csv(self):
         with open('basses.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()
        
            for result in self.results:
                writer.writerow(result)

    def run(self):
        url = 'https://www.thebassplace.com/product-category/basses/4-string/'
        
        for index in range(1, 4):
            if index == 1:
                next_page = url
            
            else:
                next_page = url + 'page/' + str(index) + '/'

            res = self.fetch(next_page)
            if res.status_code == 200:
                self.parse(res.text)
                time.sleep(2)
            else:
                print("something is wrong")
                continue

        self.to_csv()
if __name__ == '__main__':
    scraper = Guitar()
    scraper.run()                