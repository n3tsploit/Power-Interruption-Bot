import bs4, requests, os
from pathlib import Path

res = requests.get('https://kplc.co.ke/category/view/50/planned-power-interruptions')
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text,'html.parser')

links = soup.select('.items .intro li a')
if not links:
    print('No content Found')
else:
    url = str(links[0].get('href'))
    print(url)
    os.makedirs('./content/', exist_ok=True)
    res = requests.get(url)
    res.raise_for_status()
    p = Path('./content/')
    print(list(p.glob('*.pdf')))
    os.remove(list(p.glob('*.pdf'))[0])
    with open('./content/'+os.path.basename(url),'wb') as r:
        r.write(res.content)