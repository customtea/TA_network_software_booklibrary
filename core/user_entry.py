import typing as tp
from enum import IntEnum
from hashlib import sha256
from net.teaauth import TeaPublicKey #, TeaSecretKey

class UserType(IntEnum):
    USER    = 1000
    MANAGER = 2000
    ADMIN   = 3000
    DISABLE = 4000


class UserEntry():
    def __init__(self, uid: int, name: str, utype: UserType, pubkey: str, booklist: tp.List[int], note: tp.Any=None) -> None:
        self.__userid = uid
        self.__name = name
        self.__user_type = utype
        self.__pubkey: TeaPublicKey = TeaPublicKey(pubkey)
        self.__lending_booklist: tp.List[int] = booklist
        self.__note = note
    
    @classmethod
    def new(cls, uid, name, pubkey, note: tp.Any=None) -> None:
        return cls(uid, name, UserType.USER, pubkey, [], note)
    
    @classmethod
    def load(cls, uid, name, utype, pubkey, lendinglist, note):
        return cls(uid, name, UserType(utype), pubkey, lendinglist, note)

    @classmethod
    def load_dict(cls, d):
        for atr, val in d.items():
            if "__userid" in atr:
                uid = int(val)
            elif "__name" in atr:
                name = val
            elif "__user_type" in atr:
                user_type = UserType(int(val))
            # elif "__passwd_hash" in atr:
            # This Statement used to Convert from old Hashed Password to PublicKey
            #     pubkey = TeaSecretKey(val).get_publickey()
            elif "__pubkey" in atr:
                pubkey = val
            elif "__lending_booklist" in atr:
                lending_booklist = list(val)
            elif "__note" in atr:
                note = val
            else:
                pass
        return cls(uid, name, user_type, pubkey, lending_booklist, note)
    

    def __str__(self) -> str:
        return f"{self.__userid}:{self.__name}"
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return NotImplemented
        return self.__userid == __o.__userid
    
    def __lt__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return NotImplemented
        return self.__userid < __o.__userid

    
    def userid(self) -> int:
        return self.__userid
    
    def name(self) -> str:
        return self.__name
    
    def note(self) -> tp.Any:
        return self.__note
    
    def auth_pubkey(self, signature, data) -> bool:
        return self.__pubkey.verify(signature, data)

    def change_pubkey(self, new_pubkey:str) -> bool:
        self.__pubkey = TeaPublicKey(new_pubkey)
        return True
    
    def get_lendinglist(self) -> tp.List[int]:
        return self.__lending_booklist
    
    def add_lendinglist(self, bookid: int) -> bool:
        self.__lending_booklist.append(bookid)
        return True
    
    def remove_lendinglist(self, bookid: int) -> bool:
        if bookid in self.__lending_booklist:
            self.__lending_booklist.remove(bookid)
            return True
        return False
    
    def user_type(self):
        return self.__user_type
    
    def set_user_type(self, typ: UserType):
        self.__user_type = typ

