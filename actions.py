import click

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger

from scraper import get_episodes
from db import Base, Episode


engine = create_engine('sqlite:///episodes.db')
Session = sessionmaker(engine)
Base.metadata.create_all(engine)


@click.group
def cli():
    pass


@cli.command
def update_episodes():
    episodes = get_episodes()
    with Session() as session:
        logger.info(f'{len(episodes)} episodes scraped')
        i = 0
        for episode in episodes:
            if not session.query(Episode).filter_by(url=episode.url).first():
                logger.info(episode.url)
                i += 1
                db_episode = Episode(title=episode.title, url=episode.url)
                session.add(db_episode)
        session.commit()


if __name__ == '__main__':
    cli()
