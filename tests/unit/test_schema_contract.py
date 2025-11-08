from sqlalchemy import String, Integer, Float
from src.models.base import Author, Book, Member, Loan, Payment

def _col(model, name):
    return model.__table__.columns[name]

def test_author_schema_contract():
    t = Author.__table__
    assert t.name == "author"
    # PK
    assert _col(Author, "author_id").primary_key is True
    # Not null e tipos/lengths
    assert _col(Author, "author_nm").nullable is False
    assert isinstance(_col(Author, "author_nm").type, String)
    assert _col(Author, "author_nm").type.length == 120
    # country_nm pode ser nulo
    assert _col(Author, "country_nm").nullable is True
    assert isinstance(_col(Author, "country_nm").type, String)
    assert _col(Author, "country_nm").type.length == 80

def test_book_schema_contract():
    t = Book.__table__
    assert t.name == "book"
    assert _col(Book, "book_id").primary_key is True
    assert _col(Book, "title_nm").nullable is False
    assert isinstance(_col(Book, "title_nm").type, String)
    assert _col(Book, "title_nm").type.length == 200

    # genre_nm pode ser nulo com length 80
    assert _col(Book, "genre_nm").nullable is True
    assert isinstance(_col(Book, "genre_nm").type, String)
    assert _col(Book, "genre_nm").type.length == 80

    # year_nbr pode ser nulo (inteiro)
    assert _col(Book, "year_nbr").nullable is True
    assert isinstance(_col(Book, "year_nbr").type, Integer)

    # FK obrigatória para author
    fkcol = _col(Book, "author_id")
    assert fkcol.nullable is False
    assert len(fkcol.foreign_keys) == 1
    assert next(iter(fkcol.foreign_keys)).target_fullname.endswith("author.author_id")

def test_member_schema_contract():
    t = Member.__table__
    assert t.name == "member"
    assert _col(Member, "member_id").primary_key is True
    assert _col(Member, "member_nm").nullable is False
    assert isinstance(_col(Member, "member_nm").type, String)
    assert _col(Member, "member_nm").type.length == 120

    email = _col(Member, "email_nm")
    assert email.nullable is False
    assert isinstance(email.type, String)
    assert email.type.length == 200
    # unique=True na coluna
    assert email.unique is True

def test_loan_schema_contract():
    t = Loan.__table__
    assert t.name == "loan"
    assert _col(Loan, "loan_id").primary_key is True

    member_id = _col(Loan, "member_id")
    assert member_id.nullable is False
    assert len(member_id.foreign_keys) == 1
    assert next(iter(member_id.foreign_keys)).target_fullname.endswith("member.member_id")

    book_id = _col(Loan, "book_id")
    assert book_id.nullable is False
    assert len(book_id.foreign_keys) == 1
    assert next(iter(book_id.foreign_keys)).target_fullname.endswith("book.book_id")

    # due_dt é obrigatório
    assert _col(Loan, "due_dt").nullable is False
    # return_dt pode ser nulo
    assert _col(Loan, "return_dt").nullable is True

def test_payment_schema_contract():
    t = Payment.__table__
    assert t.name == "payment"
    assert _col(Payment, "payment_id").primary_key is True

    member_id = _col(Payment, "member_id")
    assert member_id.nullable is False
    assert len(member_id.foreign_keys) == 1
    assert next(iter(member_id.foreign_keys)).target_fullname.endswith("member.member_id")

    amount = _col(Payment, "amount_amt")
    assert amount.nullable is False
    assert isinstance(amount.type, Float)

    # paid_dt pode ser nulo
    assert _col(Payment, "paid_dt").nullable is True

    reason = _col(Payment, "reason_txt")
    assert reason.nullable is False
    assert isinstance(reason.type, String)
    assert reason.type.length == 200
