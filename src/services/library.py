from datetime import date, timedelta
from sqlalchemy.orm import Session
from ..models.base import Author, Book, Member, Loan, Payment
from ..repositories.entities import AuthorRepository, BookRepository, MemberRepository, LoanRepository, PaymentRepository
from ..utils.settings import get_settings
import csv, os

class BusinessError(Exception): ...

class LibraryService:
    def __init__(self, session: Session) -> None:
        self.authors = AuthorRepository(session)
        self.books = BookRepository(session)
        self.members = MemberRepository(session)
        self.loans = LoanRepository(session)
        self.payments = PaymentRepository(session)

    # CRUDs (5 entidades)
    def create_author(self, author_nm: str, country_nm: str | None=None) -> Author:
        return self.authors.add(Author(author_nm=author_nm, country_nm=country_nm))

    def create_book(self, title_nm: str, author_id: int, genre_nm: str | None=None, year_nbr: int | None=None) -> Book:
        return self.books.add(Book(title_nm=title_nm, author_id=author_id, genre_nm=genre_nm, year_nbr=year_nbr))

    def create_member(self, member_nm: str, email_nm: str) -> Member:
        return self.members.add(Member(member_nm=member_nm, email_nm=email_nm))

    # Regras complexas aplicadas em empréstimos e pagamentos
    def open_loan(self, member_id: int, book_id: int, days_nbr: int=7) -> Loan:
        # Regra 1: no máximo 3 empréstimos ativos
        if self.members.active_loans_count(member_id) >= 3:
            raise BusinessError("limite_empréstimos_ativos_excedido_flg")

        # Regra 3: bloquear empréstimo se houver pagamentos pendentes
        if self.members.has_pending_payments(member_id):
            raise BusinessError("membro_com_pendência_financeira_flg")

        due = date.today() + timedelta(days=days_nbr)  # Regra 2 (due date automático)
        return self.loans.add(Loan(member_id=member_id, book_id=book_id, due_dt=due))

    def close_loan(self, loan_id: int, return_dt: date | None=None) -> Loan:
        loan = self.loans.get(loan_id)
        if not loan:
            raise BusinessError("emprestimo_nao_encontrado_flg")
        loan.return_dt = return_dt or date.today()

        # Regra 2: multa R$2 por dia de atraso
        if loan.return_dt > loan.due_dt:
            days = (loan.return_dt - loan.due_dt).days
            self.payments.add(Payment(member_id=loan.member_id, amount_amt=2.0*days, paid_dt=None, reason_txt="multa_atraso_txt"))
        self.loans.session.commit()
        self.loans.session.refresh(loan)
        return loan

    def pay_payment(self, payment_id: int) -> Payment:
        p = self.payments.get(payment_id)
        if not p: raise BusinessError("pagamento_nao_encontrado_flg")
        p.paid_dt = date.today()
        self.payments.session.commit()
        self.payments.session.refresh(p)
        return p

    # Consultas com filtro/ordenação
    def search_books(self, author_nm: str | None=None, genre_nm: str | None=None, order_by: str | None=None) -> list[Book]:
        return self.books.search(author_nm=author_nm, genre_nm=genre_nm, order_by=order_by)

    def loans_by_status(self, status_cd: str) -> list[Loan]:
        return self.loans.list_by_status(status_cd)

    # Export (manipulação de arquivos)
    def export_loans_report_csv(self, path: str | None=None) -> str:
        settings = get_settings()
        reports_dir = settings.reports_dir
        os.makedirs(reports_dir, exist_ok=True)
        fname = path or os.path.join(reports_dir, "loans_report.csv")
        with open(fname, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["loan_id", "member_id", "book_id", "start_dt", "due_dt", "return_dt"])
            for l in self.loans.list():
                w.writerow([l.loan_id, l.member_id, l.book_id, l.start_dt, l.due_dt, l.return_dt])
        return fname
