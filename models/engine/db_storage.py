from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from os import environ
from models.base_model import BaseModel, Base
from models.user import User
from models.review import Review
from models.amenity import Amenity
from models.place import Place
from models.state import State
from models.city import City

class DBStorage:
    
    __engine = None
    __session = None

    def __init__(self):
        USER = environ['HBNB_MYSQL_USER']
        PASS = environ['HBNB_MYSQL_PWD']
        HOST = environ['HBNB_MYSQL_HOST']
        DB = environ['HBNB_MYSQL_DB']
        self.__engine = create_engine(f'mysql+mysqldb://{USER}:{PASS}@{HOST}/{DB}', pool_pre_ping=True)
        if environ.get('HBNB_ENV') == 'test':
            meta = MetaData()
            meta.drop_all(bind=self.__engine)

    def all(self, cls=None):
        classes = self.classes()
        # al = self.__session.query(State).all()
        # print(al)
        # return {}
        # if cls:
        #     allarr = self.__session.query(cls).all()
        # else:
        #     allarr = []
        #     for clss in classes.values():
        #         print(f'clss: {clss}')
        #         allarr.append(self.__session.query(clss).all())

        # alldict = {}

        # print(f'obj: {allarr}')
        # for obj in allarr:
        #     alldict[f'{obj.__class__.__name__}.{obj.id}'] = obj

        # return alldict
        dct = {}
        if cls is None:
            for c in classes.values():
                objs = self.__session.query(c).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    dct[key] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                dct[key] = obj
        return dct

    def new(self, obj):
        if obj:
            print('new detected')
            self.__session.add(obj)
            # self.__session.refresh(obj)

    def save(self):
        print('saving')
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        from models.base_model import Base
        meta = MetaData()
        meta.create_all(self.__engine)
        # print(f'tables: {meta.tables}'
        # from models.state import State
        # from models.city import City
        Base.metadata.create_all(self.__engine)
        print('reloadeddddddds')
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory=session_factory)
        self.__session = Session()

    @staticmethod
    def classes():
        """returns all valid classes"""

        classes = {
            "City": City,
            "State": State,
            }
        return classes
