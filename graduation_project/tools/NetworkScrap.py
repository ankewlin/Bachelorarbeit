import requests
from bs4 import BeautifulSoup

url = "https://item.jd.com/10060561769481.html#comment"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

comments = []
comment_con = soup.find_all('div', {'class': 'comment-con'})

for comment in comment_con:
    print(comment)
    comments.append(comment.text.strip())

print(comments)
