from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from os import environ


class DBStorage:
    
    __engine = None
    __session = None

    def __init__(self):
        classes = self.classes()
        USER = environ['HBNB_MYSQL_USER']
        PASS = environ['HBNB_MYSQL_PWD']
        HOST = environ['HBNB_MYSQL_HOST']
        DB = environ['HBNB_MYSQL_DB']
        self.__engine = create_engine(f'mysql+mysqldb://{USER}:{PASS}@{HOST}/{DB}', pool_pre_ping=True)
        if environ.get('HBNB_ENV') == 'test':
            classes['Base'].metadata.drop_all()


    def all(self, cls=None):
        classes = self.classes()
        if cls:
            allarr = self.__session.query(cls).all()
        else:
            allarr = []
            for clss in classes.values():
                allarr.append(self.__session.query(clss).all())

        alldict = {}
        for obj in allarr:
            alldict[f'{obj.__class__.__name__}.{obj.id}'] = obj

        return alldict

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        self.classes()['Base'].metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory=session_factory)
        self.__session = Session()

    @staticmethod
    def classes():
        """returns all valid classes"""
        from models.base_model import BaseModel, Base
        from models.user import User
        from models.review import Review
        from models.amenity import Amenity
        from models.place import Place
        from models.state import State
        from models.city import City

        classes = {
            "Base": Base,
            "BaseModel": BaseModel,
            "User": User,
            "City": City,
            "State": State,
            "Amenity": Amenity,
            "Review": Review,
            "Place": Place
            }
        return classes
