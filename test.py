from sqlalchemy import create_engine, Column, Integer, String, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

engine = create_engine("postgresql+psycopg2://hng_user:hng_password@localhost:5432/profiledb", echo=True)


class BaseMixin:
    def to_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self)
        }

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    age = Column(Integer)

    def __repr__(self):
        return f"Person(id={self.id}, name={self.name}, age={self.age})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age
        }


Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

new_person = Person(name="chinaza", age=29)
session.add(new_person)
print(new_person.to_dict())
session.commit()
session.refresh(new_person)
print(new_person.to_dict())
