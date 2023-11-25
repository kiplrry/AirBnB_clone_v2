#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import storagetype


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    if storagetype == 'db':
        name = Column(String(128), nullable=False)        
        cities = relationship('City', cascade='all, delete', backref='state')
    else:
        @property
        def cities(self):
            from models import storage
            related_cities = []
            cities = storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    related_cities.append(city)
            return related_cities
