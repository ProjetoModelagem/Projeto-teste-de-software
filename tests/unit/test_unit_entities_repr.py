from src.models import base as models


def test_entities_repr_and_pk_consistency():
    """
    Em SQLAlchemy, igualdade padrão é por identidade do objeto, não por PK.
    Então testamos:
      - __repr__ gera string útil
      - objetos distintos podem ter o mesmo id (simulação pós-persistência)
      - a PK está definida e coerente
    """
    b1 = models.Book(title_nm="ABC", author_id=1, genre_nm=None, year_nbr=None)
    b2 = models.Book(title_nm="ABC", author_id=1, genre_nm=None, year_nbr=None)

    # simula PK atribuída pelo BD
    b1.id = 42
    b2.id = 42

    # __repr__ deve existir e mencionar a classe
    r = repr(b1)
    assert isinstance(r, str) and "Book" in r

    # Objetos diferentes (identidade diferente) mesmo com PK igual
    assert b1 is not b2
    assert b1.id == b2.id == 42
