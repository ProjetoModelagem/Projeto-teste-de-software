from sqlalchemy.orm import Session
from ..models.base import Author, Book, Member, Loan, Payment
from .repository import Repository
from sqlalchemy import select, func, and_

class AuthorRepository(Repository[Author]):
    def __init__(self, session: Session): super().__init__(session, Author)

class BookRepository(Repository[Book]):
    def __init__(self, session: Session): super().__init__(session, Book)

    def search(self, author_nm: str | None=None, genre_nm: str | None=None, order_by: str | None=None):
        stmt = select(Book).join(Author)
        if author_nm:
            stmt = stmt.where(func.lower(Author.author_nm).like(f"%{author_nm.lower()}%"))
        if genre_nm:
            stmt = stmt.where(func.lower(Book.genre_nm).like(f"%{genre_nm.lower()}%"))
        if order_by == "title":
            stmt = stmt.order_by(Book.title_nm.asc())
        elif order_by == "year":
            stmt = stmt.order_by(Book.year_nbr.desc())
        return list(self.session.scalars(stmt))

class MemberRepository(Repository[Member]):
    def __init__(self, session: Session): super().__init__(session, Member)

    def active_loans_count(self, member_id: int) -> int:
        stmt = select(func.count(Loan.loan_id)).where(and_(Loan.member_id==member_id, Loan.return_dt==None))
        return self.session.execute(stmt).scalar_one()

    def has_pending_payments(self, member_id: int) -> bool:
        stmt = select(func.count(Payment.payment_id)).where(and_(Payment.member_id==member_id, Payment.paid_dt==None))
        return self.session.execute(stmt).scalar_one() > 0

class LoanRepository(Repository[Loan]):
    def __init__(self, session: Session): super().__init__(session, Loan)

    def list_by_status(self, status_cd: str):
        today = func.current_date()
        if status_cd == "active":
            cond = and_(Loan.return_dt==None, Loan.due_dt >= today)
        elif status_cd == "late":
            cond = and_(Loan.return_dt==None, Loan.due_dt < today)
        else: # closed
            cond = Loan.return_dt != None
        stmt = select(Loan).where(cond).order_by(Loan.due_dt.asc())
        return list(self.session.scalars(stmt))

class PaymentRepository(Repository[Payment]):
    def __init__(self, session: Session): super().__init__(session, Payment)
