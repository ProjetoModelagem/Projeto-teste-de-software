from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Date, ForeignKey, Float
from datetime import date

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "author"
    author_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_nm: Mapped[str] = mapped_column(String(120), nullable=False)
    country_nm: Mapped[str] = mapped_column(String(80), nullable=True)
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "book"
    book_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title_nm: Mapped[str] = mapped_column(String(200), nullable=False)
    genre_nm: Mapped[str] = mapped_column(String(80), nullable=True)
    year_nbr: Mapped[int] = mapped_column(Integer, nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.author_id"), nullable=False)
    author = relationship("Author", back_populates="books")
    loans = relationship("Loan", back_populates="book")

class Member(Base):
    __tablename__ = "member"
    member_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    member_nm: Mapped[str] = mapped_column(String(120), nullable=False)
    email_nm: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    join_dt: Mapped[date] = mapped_column(Date, default=date.today)
    loans = relationship("Loan", back_populates="member")
    payments = relationship("Payment", back_populates="member")

class Loan(Base):
    __tablename__ = "loan"
    loan_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.member_id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.book_id"), nullable=False)
    start_dt: Mapped[date] = mapped_column(Date, default=date.today)
    due_dt: Mapped[date] = mapped_column(Date, nullable=False)
    return_dt: Mapped[date | None] = mapped_column(Date, nullable=True)
    member = relationship("Member", back_populates="loans")
    book = relationship("Book", back_populates="loans")

class Payment(Base):
    __tablename__ = "payment"
    payment_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.member_id"), nullable=False)
    amount_amt: Mapped[float] = mapped_column(Float, nullable=False)
    paid_dt: Mapped[date | None] = mapped_column(Date, nullable=True)
    reason_txt: Mapped[str] = mapped_column(String(200), nullable=False)
    member = relationship("Member", back_populates="payments")
