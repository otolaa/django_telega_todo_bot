from .models import Uid, Todo

ru_tuple = (
    'Дел нету, добавте /add',
    'Дело успешно добавлено - №',
    'Введите не менее 10 и не более 369 знаков ↓',
    'Описание должно быть больше 10 и меньше 369 символов!',
    'Для удаления введите номер дела ↓',
    'Дело успешно удалено',
)

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
            self.error.append(ru_tuple[3])
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

    def dell(self, id: int)->bool:
        """ dell """
        Tod = Todo.objects.filter(id=id, uid=self.uid.id).first()
        if Tod is None:
            self.error.append(f'Такой задачи - №{id} нету!')
            return False
        
        Tod.delete()
        return True

    def update(self, id: int, s: str) -> int | bool:
        """ up """
        Tod = Todo.objects.filter(id=id, uid=self.uid.id).first()
        if Tod is None:
            self.error.append(f'Такой задачи - №{id} нету!')
            return False

        if self.validate_title(s=s) is False:
            return False

        Tod.title = s
        Tod.save(update_fields=["title"])        
        
        return Tod.id

def add_teg(text_str, tegs = [], plus = '') -> str:
    if len(tegs) == 0:
        return text_str
    
    pre_teg = ''.join(['<'+str(p)+'>' for p in tegs])
    tegs.reverse()
    suf_teg = ''.join(['</'+str(s)+'>' for s in tegs])
    
    return pre_teg + str(text_str) + suf_teg + plus