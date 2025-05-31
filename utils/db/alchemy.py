from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    BigInteger,
    func,
    VARCHAR,
    desc,
)
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from data.config import DB_URI
import json

engine = create_engine(DB_URI)
Base = declarative_base()


class User(Base):
    __tablename__ = "user_giveaway"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cid = Column(BigInteger, unique=True)
    phonenumber = Column(String, default="+998945387472")
    whois = Column(String, default="user")
    status = Column(String, default="active")
    cache = Column(String, default="none")
    channels = Column(String, default="[]")
    gws = Column(String, default="[]")


class Giveaway(Base):
    __tablename__ = "giveaway_giveaway"
    id = Column(Integer, primary_key=True, autoincrement=True)
    gwo = Column(BigInteger)
    period = Column(String)
    status = Column(String)
    winner = Column(String)
    users = Column(String)
    winner_cnt = Column(Integer, default=1) 


class Channels(Base):
    __tablename__ = "channels_giveaway"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cid = Column(String, default="None", unique=True)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def get_all_user():
    try:
        x = session.query(User.cid).all()
        res = [i[0] for i in x]
        return res
    finally:
        session.close()


def get_all_gw():
    try:
        x = session.query(Giveaway).all()
        res = [i for i in x]
        return res
    finally:
        session.close()

def get_own_gws(gwo):
    try:
        x = session.query(Giveaway).filter_by(gwo=int(gwo)).all()
        return x 
    finally:
        session.close()

def user_count():
    try:
        x = session.query(func.count(User.id)).first()
        return x[0]
    finally:
        session.close()


def create_user(cid, cache="none"):
    try:
        user = User(
            cid=int(cid), whois="user", status="active", cache=cache
        )
        session.add(user)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()


def delete_channel_gwo(gwo, value):
    try:
        x = session.query(User).filter_by(cid=gwo).first()
        channels = json.loads(x.channels)
        print(1, channels)
        channels = set(channels)
        channels.discard(value)
        print(2, channels)
        x.channels = json.dumps(list(channels))
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        print(e)
    finally:
        session.close()


def add_channel_gwo(gwo, value):
    try:
        x = session.query(User).filter_by(cid=gwo).first()
        channels = json.loads(x.channels)
        channels.append(value)
        print(value)
        x.channels = json.dumps(channels)
        print("channels", x.channels, channels)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        print("ERROR IN ADD GWO CHANNEL", e)
    finally:
        session.close()


def is_there(cid) -> bool:
    x = session.query(User).filter_by(cid=cid).first()
    return x is not None


def get_info(cid, type_data):
    try:
        x = session.query(User).filter_by(cid=int(cid)).first()
        print(x)
        if type_data == "status":
            return x.status if x else None
        elif type_data == "whois":
            return x.whois if x else None
        elif type_data == "phonenumber":
            return x.phonenumber if x else "null"
        elif type_data == "cache":
            return x.cache if x else "none"
        elif type_data == "channels":
            return json.loads(x.channels)
        elif type_data == "gws":
            return json.loads(x.gws)
    finally:
        session.close()


def change_info(cid, type_data, value):
    try:
        x = session.query(User).filter_by(cid=int(cid)).first()
        if type_data == "status":
            x.status = value
        elif type_data == "whois":
            x.whois = value
        elif type_data == "phonenumber":
            x.phonenumber = value
        elif type_data == "cache":
            x.cache = value
        elif type_data == "add_gws":
            gws = json.loads(x.gws)
            gws.append(value)
            gws = list(set(gws))
            x.gws = json.dumps(gws)
        session.commit()
        session.close()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
        return False


def get_admins():
    try:
        x = session.query(User.cid).filter_by(whois="admin").all()
        return [x[0][0]] if x else []
    finally:
        session.close()


def manage_admin(cid: int, action: str) -> bool:
    try:
        x = session.query(User).filter_by(cid=cid).first()
        if action == "add":
            x.whois = "admin"
        elif action == "rm":
            x.whois = "user"
        else:
            print("Noaniq harakat")
            return False

        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(e)
        return False
    finally:
        session.close()


def get_members():
    try:
        x = session.query(User).where(User.cid >= 0).all()
        return x
    finally:
        session.close()


def put_channel(channel: str):
    try:
        x = Channels(cid=channel)
        session.add(x)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
        return False


def get_channel():
    try:
        x = session.query(Channels).all()
        res = [i.cid for i in x]
        return res
    finally:
        session.close()


def get_channel_with_id():
    try:
        x = session.query(Channels).all()
        res = ""
        for channel in x:
            res += f"\nID: {channel.id} \nCID: {channel.cid}"
        return res
    finally:
        session.close()


def delete_channel(ch_id):
    try:
        x = session.query(Channels).filter_by(id=int(ch_id)).first()
        if x:
            session.delete(x)
            session.commit()
            return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
        return False


def create_giveaway(gwo, period,winner_cnt):
    try:
        gw = Giveaway(gwo=gwo, period=period, status="open", winner="nobody", users="[]",winner_cnt=int(winner_cnt))
        session.add(gw)
        session.commit()
        return gw.id
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
        return False

def change_info_gw(id, x_type, value):
    try:
        x = session.query(Giveaway).filter_by(id=id).first()
        if x_type == "winner":
            x.winner = value
        elif x_type == "status":
            x.status = value
        elif x_type == "add_user":
            users = json.loads(x.users)
            users.append(value)
            users = list(set(users))
            print("GW users", users)
            x.users = json.dumps(users)
        session.commit()
        session.close()
    except Exception as e:
        print("ERROR IN GV CHANGE INFO", e)
        session.rollback()
    finally:
        session.close()


def get_info_gw(id, x_type):
    try:
        x = session.query(Giveaway).filter_by(id=id).first()
        if x:
            if x_type == "winner":
                return x.winner
            elif x_type == "status":
                return x.status
            elif x_type == "gwo":
                return x.gwo
            elif x_type == "users":
                return list(set(json.loads(x.users)))
            elif x_type == "period":
                return x.period
            elif x_type == "object":
                return x
    finally:
        session.close()
