import urllib.parse
import requests
from bs4 import BeautifulSoup
from slugify import slugify

def search(talk, year):
    # Init search URL
    talk = urllib.parse.quote(talk).replace('%20', '+')
    url = 'https://schedule.sxsw.com/'+str(year)+'/search?q='+talk

    # Get results HTML
    results = requests.get(url)

    # Find search results
    soup = BeautifulSoup(results.text, 'lxml')
    event_lists = soup.find(class_='event-list')
    event_list_links = event_lists.find_all('a')

    # Loop through links
    for event in event_list_links:
        if args.talk.lower() in event.getText().lower():
            # Download the talk
            download(event.getText(), event.get('href'))

def download(name, path):
    print('Found talk '+name)

    # Look for audio recording on event page
    ## Build URL
    url = 'https://schedule.sxsw.com'+path
    
    # Parse event page HTML
    event_html = requests.get(url)
    soup = BeautifulSoup(event_html.text, 'lxml')

    ## Find audio recording
    audio = soup.find('audio')
    if audio:
        audio_url = audio.get('src')
        print('- Found Recording '+ audio_url)
        ext = audio_url.split('.')[-1]

        # Save recording to disk
        filename = slugify(name)+'.'+ext
        print('- Saving Recording to '+filename)
        file = requests.get(audio_url)
        open(filename, 'wb').write(file.content)
    else:
        print('- No Audio found.')


if __name__ == "__main__":
    import argparse
    
    # Get arguments
    parser = argparse.ArgumentParser("SXSW Audio Downloader")
    parser.add_argument("year", help="Year.", type=int)
    parser.add_argument("talk", help="Name of the talk.", type=str)
    args = parser.parse_args()

    # Search
    search(args.talk, args.year)
