from .models import Uid, Todo

class GreatTodo():
    """ great for todo """
    def __init__(self, uid: int, username: str):
        self.uid = self.get_or_create(uid, username)
        self.username = username
        self.error = []

    @staticmethod
    def get_or_create(uid: int, username: str):        
        UserUid = Uid.objects.filter(id=uid).first()
        if UserUid is None:
            UserUid = Uid.objects.create(id=uid, username=username)            

        return UserUid

    def validate_title(self, s: str) -> bool:
        """ validate str title """
        if 10 > len(s) or len(s) > 369:
            self.error.append(f'Описание должно быть больше 10 и меньше 369 символов!')
            return False
        
        return True

    def add(self, s: str) -> int | bool:
        res = False
        if self.validate_title(s=s) is False:
            return res
        
        Tod = Todo.objects.filter(uid=self.uid.id, title=s).first()
        if Tod is not None:
            self.error.append(f'Такая задача №{Tod.id} уже есть!')
            return res

        Tod = Todo.objects.create(uid=self.uid, title=s)
        res = Tod.id

        return res

    def dell(self, id: int)->None:
        Todo.objects.filter(id=id).delete()

    def update(self, id: int, s: str) -> int | bool:
        res = False        
        Tod = Todo.objects.filter(id=id).first()
        if Tod is None:
            self.error.append(f'Такой задачи - №{id} нету!')
            return res

        if self.validate_title(s=s) is False:
            return res

        Tod.title = s
        Tod.save(update_fields=["title"])
        res = Tod.id
        
        return res