from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)
creator_engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=creator_engine)
session = Session()

Base = declarative_base(metadata=metadata)
company_dev = Table('company_devs', Base.metadata, Column('company_id', ForeignKey('companies.id'), primary_key = True), Column('dev_id', ForeignKey('devs.id'), primary_key = True))

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship('Frieebies', backref=backref('company'))
    devs = relationship('Dev', secondary=company_dev, back_populates='companies')


    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    freebies = relationship('Freebie', back_populates='dev')
    companies = relationship('Company', secondary='freebies', back_populates='devs')


    def __repr__(self):
        return f'<Dev {self.name}>'

class Freebie(Base):

    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    dev_id = Column(Integer(), ForeignKey('devs.id'))
   # The backref and back_populates keywords generate attributes in the related data model that map to records from the current data model.
    dev = relationship('Devs', back_populates='freebies')

    company_id = Column(Integer(), ForeignKey('companies.id'))
    company = relationship('Company', back_populates='freebies')

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"

    @classmethod
    def give_away(cls, dev, freebie):
        if freebie.dev == dev:
            freebie.dev = None

    @classmethod
    def received_one(cls, item_name):
        return cls.query.filter_by(item_name=item_name).first() is not None

    @classmethod
    def create_freebie(cls, dev, company, item_name, value):
        freebie = cls(dev=dev, company=company, item_name=item_name, value=value)
        # session.add(freebie)
        # session.commit()

    @classmethod
    def oldest_company(cls):
        return Company.query.order_by(Company.founding_year).first()