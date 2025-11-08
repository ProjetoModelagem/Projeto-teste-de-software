from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session

T = TypeVar('T')

class Repository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]) -> None:
        self.session = session
        self.model = model

    def add(self, obj: T) -> T:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get(self, obj_id: int) -> T | None:
        return self.session.get(self.model, obj_id)

    def list(self) -> list[T]:
        return list(self.session.query(self.model))

    def delete(self, obj_id: int) -> bool:
        obj = self.get(obj_id)
        if not obj:
            return False
        self.session.delete(obj)
        self.session.commit()
        return True
