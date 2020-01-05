from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        if 'Image URL (for hotlinking/embedding)' in data:
            data = data.split()
            global img_url
            img_url = data[-1]

parser = MyHTMLParser()