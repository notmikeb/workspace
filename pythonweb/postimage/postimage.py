import requests
import datetime

class mypost():
    def __init__(self):
        self.s = requests.Session()
        self.login()

    def login(self):
        s = self.s
        g1 = s.get('http://192.168.0.30:8089/login/' )
        self.g2 = s.post('http://192.168.0.30:8089/login/' , {'username': 'day2', 'password':'test1234', 'csrfmiddlewaretoken': g1.cookies['csrftoken']} )

    def postImage(self, filename = 'smile.jpg'):
        g2 = self.g2
        s = self.s
        if 200 == g2.status_code:
            pass
            g3 = s.get('http://192.168.0.30:8089')
            if g3.status_code != 200 or 'login' in g3.url:
                print("failed login")
            else:
                print("login success")
                ## post a photo
            
                g5 = s.get('http://192.168.0.30:8089/post/new/')
                multiple_files = [
                ('csrfmiddlewaretoken', (None, g5.cookies['csrftoken'])), 
                ('title', (None, 'atitle')),
                ('content', (None, 'acontent {}'.format(datetime.datetime.now())) ),
                ('image', (filename, open(filename, 'rb'), 'image/jpeg'))]
                g4 = s.post('http://192.168.0.30:8089/post/new/', files = multiple_files)
                print("result ", g4.status_code)


if __name__ == "__main__":
    m1 = mypost()
    import sys
    for fn in sys.argv:
        if 'jpg' in fn:
            m1.postImage(fn) #'smile.jpg')
