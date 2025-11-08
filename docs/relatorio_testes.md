# Relatório de Testes - Sistema Biblioteca (FastAPI)

## 1. Resumo Executivo
- **Suíte executada com sucesso** (sem falhas)
- **Cobertura global:** **84%**
- **Mutação:** 27 sobreviventes (nenhum crítico)
- **Benchmark:** média ~**68,30 ms** no cenário de busca de livros
- **Total:** 101 *passed*, 1 *skipped*

## 2. Resultados Consolidados
| Categoria | Resultado |
|-----------|-----------|
| Unitários | **66 passed**, 0 falhas |
| Integração | **17 passed**, **1 skipped** |
| Funcionais | **18 passed**, 0 falhas |
| Cobertura | **84%** global |
| Mutação | **27 sobreviventes**, plano de reforço descrito abaixo |
| Benchmark | **Mean ≈ 68,30 ms**, Min 53,62 ms, Max 93,41 ms |

## 3. Evidências e Relatórios (HTML)
- Unit: `report_unit.html`
- Integração: `report_integration.html`
- Funcionais: `functional_report.html`
- Benchmark: `benchmark_report.html`
- Planejamento: `plano_testes.md`
- Execução: `relatorio_testes.md`

> Observação: os arquivos acima constam na pasta de evidências do projeto.

## 4. Análise por Nível

### 4.1. Testes Unitários
- **Cobertura de validações e ramos** (schemas, API validations, regras do serviço com mocks/stubs).
- Resultado: **66/66 passed**.

### 4.2. Testes de Integração
- Escopo: **Service + Repository + DB + API (contratos/políticas)**.
- Resultado: **17 passed / 1 skipped**.
- Técnicas: **fixtures de sessão** e **rollback** entre cenários.

### 4.3. Testes Funcionais (Caixa‑Preta)
- Cobriu regras de negócio e fluxos (cadastro de membro, busca por filtros, fluxo de empréstimo).
- Resultado: **18/18 passed**.

### 4.4. Cobertura
- **Global:** **84%**
- Foco de melhoria: **`src/services/library.py`** (70% atualmente).

### 4.5. Teste de Mutação
- **27 sobreviventes** mapeados (ex.: alterações em PKs/`__tablename__` e razões de multa).
- **Plano de reforço**:
  - Adicionar asserts cobrindo **integridade de PK** e **strings de negócio** (razão de multa).
  - Criar casos direcionados para **branches não cobertos** em `library.py`.
  - Complementar cenários de integração para falhas “silenciosas”.

### 4.6. Benchmark / Desempenho
- Cenário: **busca de livros**.
- Estatísticas: **Mean ≈ 68,30 ms**; **Min 53,62 ms**; **Max 93,41 ms**; **OPS ≈ 14,64**; **Rounds: 5**.
- Interpretação: latência estável e dentro do esperado para SQLite local; acompanhar tendência a cada release.

## 4.7 Testes Específicos

- **API / REST** — [integration/contracts](https://github.com/ProjetoModelagem/Projeto-teste-de-software/blob/main/tests/integration/test_integration_contracts.py) · [functional/acceptance](https://github.com/ProjetoModelagem/Projeto-teste-de-software/blob/main/tests/functional/test_functional_acceptance.py)

- **Exceções** — [unit/repository_errors](https://github.com/ProjetoModelagem/Projeto-teste-de-software/blob/main/tests/unit/test_unit_repository_errors.py) · [integration/idempotency](https://github.com/ProjetoModelagem/Projeto-teste-de-software/blob/main/tests/integration/test_integration_idempotency.py)

- **Mocks / Stubs** — [test_service_with_mocks.py](https://github.com/ProjetoModelagem/Projeto-teste-de-software/blob/main/tests/unit/test_service_with_mocks.py)
- **Performance / Carga (benchmark)** — [test_performance_benchmark.py](https://github.com/ProjetoModelagem/Projeto-teste-de-software/blob/main/tests/integration/test_performance_benchmark.py)
- **Orientação a Objetos (OO)** — [test_oop_design.py](https://github.com/ProjetoModelagem/Projeto-teste-de-software/blob/main/tests/unit/test_oop_design.py)

## 4.8 Screenshots das Evidências
| Unidade | Integração | Funcional |
|:--:|:--:|:--:|
| ![Unit](./test-unit.png) | ![Integration](./test-integration.png) | ![Functional](./test-functional.png) |

**Cobertura & Mutação**

![Cobertura](./coverage.png)
![Mutação](./mutant-test.png)


## 5. Conclusão
- **Meta de cobertura atingida** (≥ 80%).
- Regras essenciais validadas (limite empréstimos, pendências, multa).
- **Suíte robusta**; mutação revelou pontos para próximo ciclo sem achados críticos.
- Requisitos do alcançados.