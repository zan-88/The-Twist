from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import spotipy
from spotipy.oauth2 import SpotifyOAuth

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get('https://music.apple.com/ca/playlist/alternative/pl.u-ABL3CxA2NRm')
driver.fullscreen_window()
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Preview"]')))

elem = driver.find_element(By.ID, 'page-container__first-linked-element')
playlistName = elem.text

albEl = driver.find_elements(By.XPATH, '//div[@class="songs-list__col songs-list__col--album typography-body"]//a')

titleEl = driver.find_elements(By.CLASS_NAME, "songs-list-row__song-name")

artEl = driver.find_elements(By.XPATH, '//div[@class="songs-list__col songs-list__col--artist typography-body"]//a[1]')

titles = []
albums = []
artists = []

ep = " - EP"
single = " - Single"

driver.implicitly_wait(200)
for i in titleEl:
    titles.append(i.text)

for i in artEl:
    artists.append(i.text)

for i in albEl:
    alb = i.text
    if alb.endswith(ep):
        alb = alb[:-5]
    elif alb.endswith(single):
        alb = alb[:-9]

    albums.append(alb)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-modify'))
user_id = sp.me()['id']
playlist_id = sp.user_playlist_create(user_id, 'alternative')['id']

song_uris = []
missed = []
for i in range(len(titles)):
    try:
        temp = sp.search(q="artist:" + artists[i] + " track:" + titles[i] + " album:" + albums[i], type="track")['tracks']['items'][0]['uri']
        song_uris.append(temp)
    except IndexError:
        try:
            temp = sp.search(q="artist:" + artists[i] + " track:" + titles[i], type="track")['tracks']['items'][0]['uri']
            song_uris.append(temp)
        except IndexError:
            missed.append(titles[i])

sp.playlist_add_items(playlist_id, song_uris)

print(missed)
