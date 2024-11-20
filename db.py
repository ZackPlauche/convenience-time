from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Episode(Base):
    __tablename__ = 'episode'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    url: Mapped[str]
    watched: Mapped[bool] = mapped_column(default=False)

    def __str__(self):
        return self.title
