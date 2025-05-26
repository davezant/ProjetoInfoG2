import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

# Example model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

# Create a fresh in-memory SQLite test database for each test
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_insert_user(db_session):
    user = User(username="alice")
    db_session.add(user)
    db_session.commit()
    assert user.id is not None

def test_query_user(db_session):
    user = User(username="bob")
    db_session.add(user)
    db_session.commit()
    # Query user back
    user_db = db_session.query(User).filter_by(username="bob").first()
    assert user_db is not None
    assert user_db.username == "bob"

def test_unique_constraint(db_session):
    user1 = User(username="carol")
    user2 = User(username="carol")
    db_session.add(user1)
    db_session.commit()
    db_session.add(user2)
    with pytest.raises(Exception):
        db_session.commit()

def test_update_user(db_session):
    user = User(username="dave")
    db_session.add(user)
    db_session.commit()
    user.username = "davezant"
    db_session.commit()
    updated = db_session.query(User).filter_by(username="davezant").first()
    assert updated is not None

def test_delete_user(db_session):
    user = User(username="eve")
    db_session.add(user)
    db_session.commit()
    db_session.delete(user)
    db_session.commit()
    gone = db_session.query(User).filter_by(username="eve").first()
    assert gone is None

def test_raw_sql(db_session):
    db_session.execute(text("INSERT INTO users (username) VALUES (:username)"), {"username": "frank"})
    db_session.commit()
    result = db_session.execute(text("SELECT username FROM users")).fetchall()
    assert ("frank",) in result
