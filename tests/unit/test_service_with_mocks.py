from src.services.library import LibraryService

def test_service_open_loan_with_stubbed_repo(mocker):
    session = mocker.Mock()
    svc = LibraryService(session=session)

    svc.loans = mocker.Mock()
    svc.members = mocker.Mock()
    svc.books = mocker.Mock()

    svc.members.get_by_id.return_value = object()
    svc.books.get_by_id.return_value = object()
    svc.members.active_loans_count.return_value = 0
    svc.members.has_pending_payments.return_value = False
    svc.loans.add.return_value = {"loan_id": 123}

    out = svc.open_loan(member_id=1, book_id=2)
    assert out == {"loan_id": 123}
    svc.loans.add.assert_called_once()
