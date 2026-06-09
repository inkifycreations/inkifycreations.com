import urllib.request

try:
    response = urllib.request.urlopen("http://127.0.0.1:8000/mugs")
    print("Status code:", response.getcode())
    html = response.read().decode('utf-8')
    print("Page fetched successfully! Length:", len(html))
    if "Mug" in html:
        print("Found 'Mug' in page HTML!")
except Exception as e:
    print("Error connecting to server:", e)
