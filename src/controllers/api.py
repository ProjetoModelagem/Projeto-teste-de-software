from fastapi import FastAPI, Depends, HTTPException, Path, Query
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from ..models.db import get_session, init_db
from ..services.library import LibraryService, BusinessError
from ..utils.logging_setup import setup_logging
from fastapi.responses import RedirectResponse, PlainTextResponse, Response
from typing import Iterator

app = FastAPI(title="Biblioteca API")

def get_service() -> Iterator[LibraryService]:
    session: Session = get_session()
    svc = LibraryService(session)
    try:
        yield svc
    finally:
        # fecha a conexão, liberando o pool em TODA requisição
        session.close()

@app.on_event("startup")
def _startup():
    setup_logging()
    init_db()

# -------------------------------------------------
# Schemas de entrada usados pelos endpoints
# -------------------------------------------------
class AuthorIn(BaseModel):
    author_nm: str = None
    country_nm: str | None = None

class BookIn(BaseModel):
    title_nm: str = Field(..., min_length=1)
    author_id: int
    genre_nm: str | None = None
    year_nbr: int | None = None

class MemberIn(BaseModel):
    member_nm: str = Field(..., min_length=2)
    email_nm: EmailStr

class LoanOpenIn(BaseModel):
    member_id: int
    book_id: int
    days_nbr: int = 7

class PaymentIn(BaseModel):
    member_id: int
    amount_amt: float = Field(..., gt=0)
    paid_dt: str | None = None
    reason_txt: str | None = None

# -------------------------------------------------
# CONTRATO EXISTENTE (não mexer, os testes dependem)
# -------------------------------------------------
@app.post("/authors")
def create_author(payload: AuthorIn, svc: LibraryService = Depends(get_service)):
    return svc.create_author(**payload.model_dump())

@app.post("/books")
def create_book(payload: BookIn, svc: LibraryService = Depends(get_service)):
    return svc.create_book(**payload.model_dump())

@app.post("/members")
def create_member(payload: MemberIn, svc: LibraryService = Depends(get_service)):
    return svc.create_member(**payload.model_dump())

@app.post("/loans/open")
def open_loan(payload: LoanOpenIn, svc: LibraryService = Depends(get_service)):
    try:
        return svc.open_loan(**payload.model_dump())
    except BusinessError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/loans/{loan_id}/close")
def close_loan(loan_id: int, svc: LibraryService = Depends(get_service)):
    try:
        return svc.close_loan(loan_id)
    except BusinessError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/books/search")
def search_books(
    author_nm: str | None = None,
    genre_nm: str | None = None,
    order_by: str | None = None,
    svc: LibraryService = Depends(get_service),
):
    return svc.search_books(author_nm=author_nm, genre_nm=genre_nm, order_by=order_by)

@app.get("/loans/status/{status_cd}")
def loans_by_status(status_cd: str, svc: LibraryService = Depends(get_service)):
    return svc.loans_by_status(status_cd)

@app.get("/reports/loans/export")
def export_loans(svc: LibraryService = Depends(get_service)):
    return {"file_path": svc.export_loans_report_csv()}

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.get("/healthz", include_in_schema=False)
def healthz():
    return PlainTextResponse("ok")

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

# IMPORTANTE: mantenha GET /books como "não permitido" para não quebrar o teste
@app.get("/books", include_in_schema=False)
def _disallow_get_books():
    # o teste funcional espera 405 aqui
    raise HTTPException(status_code=405, detail="Method Not Allowed")

# -------------------------------------------------
# CRUDs COMPLETOS EM NAMESPACE ADMIN
# NÃO CONFLITAM COM OS TESTES EXISTENTES
# -------------------------------------------------

# --- AUTHORS CRUD ---
@app.post("/admin/authors")
def admin_create_author(payload: AuthorIn, svc: LibraryService = Depends(get_service)):
    return svc.create_author(**payload.model_dump())

@app.get("/admin/authors")
def admin_list_authors(svc: LibraryService = Depends(get_service)):
    return svc.list_authors()

@app.get("/admin/authors/{author_id}")
def admin_get_author(author_id: int = Path(..., gt=0), svc: LibraryService = Depends(get_service)):
    return svc.get_author(author_id)

@app.put("/admin/authors/{author_id}")
def admin_update_author(author_id: int, payload: AuthorIn, svc: LibraryService = Depends(get_service)):
    return svc.update_author(author_id, **payload.model_dump())

@app.delete("/admin/authors/{author_id}", status_code=204)
def admin_delete_author(author_id: int, svc: LibraryService = Depends(get_service)):
    svc.delete_author(author_id)
    return Response(status_code=204)

# --- BOOKS CRUD ---
@app.post("/admin/books")
def admin_create_book(payload: BookIn, svc: LibraryService = Depends(get_service)):
    return svc.create_book(**payload.model_dump())

@app.get("/admin/books")
def admin_list_books(
    author_id: int | None = Query(default=None),
    svc: LibraryService = Depends(get_service),
):
    # você pode aceitar filtros opcionais aqui
    return svc.list_books(author_id=author_id)

@app.get("/admin/books/{book_id}")
def admin_get_book(book_id: int, svc: LibraryService = Depends(get_service)):
    return svc.get_book(book_id)

@app.put("/admin/books/{book_id}")
def admin_update_book(book_id: int, payload: BookIn, svc: LibraryService = Depends(get_service)):
    return svc.update_book(book_id, **payload.model_dump())

@app.delete("/admin/books/{book_id}", status_code=204)
def admin_delete_book(book_id: int, svc: LibraryService = Depends(get_service)):
    svc.delete_book(book_id)
    return Response(status_code=204)

# --- MEMBERS CRUD ---
@app.get("/admin/members")
def admin_list_members(svc: LibraryService = Depends(get_service)):
    return svc.list_members()

@app.get("/admin/members/{member_id}")
def admin_get_member(member_id: int, svc: LibraryService = Depends(get_service)):
    return svc.get_member(member_id)

@app.put("/admin/members/{member_id}")
def admin_update_member(member_id: int, payload: MemberIn, svc: LibraryService = Depends(get_service)):
    return svc.update_member(member_id, **payload.model_dump())

@app.delete("/admin/members/{member_id}", status_code=204)
def admin_delete_member(member_id: int, svc: LibraryService = Depends(get_service)):
    svc.delete_member(member_id)
    return Response(status_code=204)

# --- PAYMENTS CRUD ---
@app.post("/admin/payments")
def admin_create_payment(payload: PaymentIn, svc: LibraryService = Depends(get_service)):
    return svc.create_payment(**payload.model_dump())

@app.get("/admin/payments")
def admin_list_payments(member_id: int | None = None, svc: LibraryService = Depends(get_service)):
    return svc.list_payments(member_id=member_id)

@app.get("/admin/payments/{payment_id}")
def admin_get_payment(payment_id: int, svc: LibraryService = Depends(get_service)):
    return svc.get_payment(payment_id)

@app.put("/admin/payments/{payment_id}")
def admin_update_payment(payment_id: int, payload: PaymentIn, svc: LibraryService = Depends(get_service)):
    return svc.update_payment(payment_id, **payload.model_dump())

@app.delete("/admin/payments/{payment_id}", status_code=204)
def admin_delete_payment(payment_id: int, svc: LibraryService = Depends(get_service)):
    svc.delete_payment(payment_id)
    return Response(status_code=204)

# --- LOANS leitura/cancelamento ---
@app.get("/admin/loans")
def admin_list_loans(status_cd: str | None = None, svc: LibraryService = Depends(get_service)):
    return svc.list_loans(status_cd=status_cd)

@app.get("/admin/loans/{loan_id}")
def admin_get_loan(loan_id: int, svc: LibraryService = Depends(get_service)):
    return svc.get_loan(loan_id)

@app.delete("/admin/loans/{loan_id}", status_code=204)
def admin_cancel_loan(loan_id: int, svc: LibraryService = Depends(get_service)):
    # Regra típica: só cancelar se não tiver return_dt
    svc.cancel_loan(loan_id)
    return Response(status_code=204)
