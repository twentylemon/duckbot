from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Ngram2(Base):
    __tablename__ = "markov_ngram_2"

    userid = Column(BigInteger, primary_key=True)
    word1 = Column(String, primary_key=True)
    word2 = Column(String, primary_key=True)
