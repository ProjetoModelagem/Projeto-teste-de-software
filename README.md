## Créditos
**Alunos:** Guilherme de Abreu e Kaique Fernandes
**Grupo R**
**Disciplina:** CC8550 — Simulação e Teste de Software 
**Período:** Noturno
**Instituição:** Centro Universitário FEI — SBC

## Documentação do Projeto

| Documento | Link |
|----------|------|
| Plano de Testes | [docs/plano_testes.md](docs/plano_testes.md) |
| Relatório de Testes | [docs/relatorio_testes.md](docs/relatorio_testes.md) |
| Descrição do Projeto | [docs/projeto.md](docs/projeto.md) |

# Projeto – Sistema de Biblioteca - Simulação e Teste de Software (CC8550)  
Checklist de Requisitos + Evidências + Justificativas Mutação

## 1) Arquitetura e Estrutura
| Requisito | Status | Evidência |
|----------|--------|-----------|
| Modularização | ✅ Atendido | src dividido em controllers / services / repositories / models |
| Separação de responsabilidades | ✅ Atendido | API → Service → Padrão de repositório |
| Injeção de dependências | ✅ Atendido | repos injetados no service via construtor |
| Uso de classes / abstrações | ✅ Atendido | Base ORM + Repositories |

## 2) Funcionalidades Implementadas
| Item | Status | Evidência |
|------|--------|-----------|
| 5 operações CRUD | ✅ | Authors, Books, Members, Loans, Payments |
| 3 regras de negócio complexas | ✅ | limite empréstimos / multa atraso / bloqueio se débito |
| 2 buscas com filtros + ordenação | ✅ | /books search + /members search |
| Tratamento de exceções customizadas | ✅ | BusinessError |
| Validações de entrada | ✅ | Pydantic Schemas |

## 3) Persistência
| Item | Status | Evidência |
|------|--------|-----------|
| Uso de banco real | ✅ | SQLite |
| Padrão de repositório | ✅ | Implementado em `src/repositories` |
| Possibilidade de mock DB nos testes | ✅ | fixtures isoláveis |

## 4) Interface
| Item | Status | Evidência |
|------|--------|-----------|
| API REST | ✅ | FastAPI usada como interface principal |

## 5) Requisitos Técnicos Específicos
| Item | Status | Evidência |
|------|--------|-----------|
| Configuração externa | ✅ | arquivo `.env` |
| Logging | ✅ | logging_setup.py |
| Docstrings | ✅ | principais classes com docstring |
| Type hints | ✅ | aplicação inteira tipada |
| Manipulação arquivos | ✅ | evidências geradas coverage/mutação exportadas |

---

## 6) Testes Unitários (25%)
| Requisito | Status | Resultado |
|-----------|--------|-----------|
| 30+ testes unitários | ✅ | > 60 unitários |
| Parametrização | ✅ | presente |
| Casos normais, extremos e erro | ✅ | validado |
| pytest | ✅ | usado |

---

## 7) Testes de Integração (20%)
| Requisito | Status |
|-----------|--------|
| Interações módulos | ✅ |
| Integração banco real | ✅ |
| Fluxos end-to-end | ✅ |
| Mínimo 10 testes | ✅ |

---

## 8) Testes Funcionais Caixa Preta (15%)
| Item | Status |
|------|--------|
| 8 cenários funcionais | ✅ |
| Testes de aceitação regras negócio | ✅ |
| Entradas/saídas sem conhecer implementação | ✅ |

---

## 9) Testes Estruturais Caixa Branca (15%)
| Item | Status | Observação |
|------|--------|------------|
| >= 80% cobertura | ✅ | 84% global |
| Branch Coverage | ✅ | ativado |
| Relatório HTML | ✅ | htmlcov gerado |

---

## 10) Testes de Mutação (10%)
| Item | Status |
|------|--------|
| Mutmut usado | ✅ |
| Pelo menos 3 módulos mutados | ✅ (`services`, `repository`, `models`) |
| Análise taxa mutantes mortos | ✅ killed 111 / 138 |
| Documentação sobreviventes | ✅ abaixo |

### Justificativa dos Mutantes Sobreviventes (27 sobreviventes)

Os mutantes remanescentes impactavam áreas que não modificam comportamento observável ou eram atributos estruturais do ORM (ex.: trocar `String(200)` para `String(201)`, tornar coluna nullable, trocar typeVar, mudar nome de tabela).  
Essas alterações não resultam em comportamento diferente para o consumidor da API e em muitos casos nem geram exceções por padrão do SQLAlchemy — portanto não são semanticamente relevantes para a regra de negócio.

Esses mutantes são considerados *equivalentes* (não matáveis) dentro do contexto do domínio estudado.

---
## 11) Testes Específicos por Tipo (15%)

| Tipo Escolhido | Status | Evidências |
|----------------|--------|------------|
| **API REST** | ✅ | [`tests/integration/test_integration_contracts.py`](https://github.com/ProjetoModelagem/Projeto-teste-de-software/blob/main/tests/integration/test_integration_contracts.py) — [`tests/functional/test_functional_acceptance.py`](https://github.com/ProjetoModelagem/Projeto-teste-de-software/blob/main/tests/functional/test_functional_acceptance.py) |
| **Exceções** | ✅ | [`tests/unit/test_unit_repository_errors.py`](https://github.com/ProjetoModelagem/Projeto-teste-de-software/blob/main/tests/unit/test_unit_repository_errors.py) — [`tests/integration/test_integration_idempotency.py`](https://github.com/ProjetoModelagem/Projeto-teste-de-software/blob/main/tests/integration/test_integration_idempotency.py) |
| **Mocks / Stubs** | ✅ | [`tests/unit/test_service_with_mocks.py`](https://github.com/ProjetoModelagem/Projeto-teste-de-software/blob/main/tests/unit/test_service_with_mocks.py) |
| **Performance / Carga** | ✅ | [`tests/integration/test_performance_benchmark.py`](https://github.com/ProjetoModelagem/Projeto-teste-de-software/blob/main/tests/integration/test_performance_benchmark.py) |
| **Orientação a Objetos (OO)** | ✅ | [`tests/unit/test_oop_design.py`](https://github.com/ProjetoModelagem/Projeto-teste-de-software/blob/main/tests/unit/test_oop_design.py) |


---