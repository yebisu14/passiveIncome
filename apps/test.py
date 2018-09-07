import urllib.request
    
url = 'https://chart.googleapis.com/chart'
params = {
    'chs': '300x300',
    'cht': 'qr',
    'chl': 'testAddress',
    'choe': 'UTF-8'
}
req = '{}?{}'.format(url, urllib.parse.urlencode(params))
urllib.request.urlretrieve(req, 'qr.png')