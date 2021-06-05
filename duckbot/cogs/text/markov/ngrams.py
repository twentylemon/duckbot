from sqlalchemy import BigInteger, Column, String, Index
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Ngram1(Base):
    __tablename__ = "markov_ngram_1"

    userid = Column(BigInteger, primary_key=True)
    word1 = Column(String, primary_key=True)
    frequency = Column(BigInteger, nullable=False)

    __table_args__ = (Index("markov_search", userid),)


class Ngram2(Base):
    __tablename__ = "markov_ngram_2"

    userid = Column(BigInteger, primary_key=True)
    word1 = Column(String, primary_key=True)
    word2 = Column(String, primary_key=True)
    frequency = Column(BigInteger, nullable=False)

    __table_args__ = (Index("markov_search", userid, word1),)


class Ngram3(Base):
    __tablename__ = "markov_ngram_3"

    userid = Column(BigInteger, primary_key=True)
    word1 = Column(String, primary_key=True)
    word2 = Column(String, primary_key=True)
    word3 = Column(String, primary_key=True)
    frequency = Column(BigInteger, nullable=False)

    __table_args__ = (Index("markov_search", userid, word1, word2),)


class Ngram4(Base):
    __tablename__ = "markov_ngram_4"

    userid = Column(BigInteger, primary_key=True)
    word1 = Column(String, primary_key=True)
    word2 = Column(String, primary_key=True)
    word3 = Column(String, primary_key=True)
    word4 = Column(String, primary_key=True)
    frequency = Column(BigInteger, nullable=False)

    __table_args__ = (Index("markov_search", userid, word1, word2, word3),)
