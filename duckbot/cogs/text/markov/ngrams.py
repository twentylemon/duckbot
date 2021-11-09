from sqlalchemy import BigInteger, Column, ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Word(Base):
    """Database mapping words to a numeric identifier."""

    __tablename__ = "markov_words"

    word_id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    word = Column(String, unique=True, nullable=False)


class NgramWord(Base):
    """Database specifying ngram members and relative ordering."""

    __tablename__ = "markov_ngrams"

    # in general, we'd want to answer "give me the next words in the chain where the previous words are blah (and ngrams are constrained to a user)"
    # select ngram_id from ngrams natural join users where sequence_id=0 and word_id=0 and sequence_id=1 and word_id=1
    ngram_id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    sequence_id = Column(Integer, primary_key=True, nullable=False)
    word_id = Column(BigInteger, nullable=False)

    __table_args__ = (ForeignKeyConstraint(("word_id",), "markov_words.word_id"),)  # TODO maybe want an index on (word_id,sequence_id)


class NgramUser(Base):
    __tablename__ = "markov_ngram_users"

    user_id = Column(BigInteger, primary_key=True, nullable=False)
    ngram_id = Column(BigInteger, primary_key=True, nullable=False)
    frequency = Column(BigInteger, nullable=False)

    __table_args__ = (ForeignKeyConstraint(("ngram_id",), "markov_ngrams.ngram_id"),)


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
