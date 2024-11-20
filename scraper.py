from playwright.sync_api import sync_playwright

from pydantic import BaseModel


class Episode(BaseModel):
    title: str
    url: str

    def __str__(self):
        return self.title


def get_episodes() -> list[Episode]:
    url = 'https://www.wcostream.tv/anime/adventure-time'
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)
    episodes = []
    links = page.locator('#catlist-listview li > a').all()
    for link in links:
        episode = Episode(title=link.inner_text(), url=link.get_attribute('href'))
        episodes.append(episode)
    return episodes
