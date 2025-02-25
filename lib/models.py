from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

# Freebie.dev returns the Dev instance for this Freebie.
# Freebie.company returns the Company instance for this Freebie.    
class Freebie(Base):
    __tablename__ = 'freebies'
    
    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())    
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))

    dev = relationship("Dev", back_populates="freebies")
    company = relationship("Company", back_populates="freebies")
    
    # Freebie.print_details()should return a string formatted as follows: {dev name} owns a {freebie item_name} from {company name}.
    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'
    
    def __repr__(self):
        return f'<Freebie {self.item_name}, Value: {self.value}>'

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    # Company.freebies returns a collection of all the freebies for the Company.
    freebies = relationship("Freebie", back_populates="company")
    
    # Company.give_freebie(dev, item_name, value) takes a dev (an instance of the Dev class), an item_name (string),
    # and a value as arguments, and creates a new Freebie instance associated with this company and the given dev.
    def give_freebie(self, dev, item_name, value):
        """Create a new Freebie instance associated with this company and the given dev"""
        the_freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        session.add(the_freebie)  
        session.commit()  
        return the_freebie
    
     # Class method Company.oldest_company()returns the Company instance with the earliest founding year.
    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()
    
    def __repr__(self):
        return f'<Company {self.name}, Founded:{self.founding_year}>'



class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    # Dev.freebies returns a collection of all the freebies that the Dev has collected.
    freebies = relationship("Freebie", back_populates="dev")
    
    # Dev.companiesreturns a collection of all the companies that the Dev has collected freebies from.
    @property
    def companies(self):
        return [freebie.company for freebie in self.freebies]
    # Dev.received_one(item_name) accepts an item_name (string) 
    # and returns True if any of the freebies associated with the dev has that item_name, otherwise returns False.
    def received_one(self, item_name):
        """Returns True if any of the freebies associated with the dev has that item_name, otherwise returns False."""
        return any(freebie.item_name == item_name for freebie in self.freebies)
    
    # Dev.give_away(dev, freebie) accepts a Dev instance and a Freebie instance,
    # changes the freebie's dev to be the given dev; your code should only make the change if the freebie belongs to the dev who's giving it away
    def give_away(self, dev, freebie):
        """changes the freebie's dev to be the given dev; only if the freebie belongs to the dev who's giving it away"""
        if freebie in self.freebies:
            freebie.dev = dev
            
    def __repr__(self):
        return f'<Dev {self.name}>'
    

    
engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()
        