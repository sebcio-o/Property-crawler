from requests_html import HTMLSession

session = HTMLSession()

r = session.get("http://1.1.1.1")
r.html.render(timeout=20)