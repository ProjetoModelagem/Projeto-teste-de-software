# Plano de Testes - Sistema Biblioteca (FastAPI)

## 1. Contexto
API de Biblioteca com arquitetura modular (Controllers → Service → Repository → SQLite/SQLAlchemy). Foco em qualidade com testes automatizados em múltiplos níveis.

## 2. Escopo e Objetivos
- **Provar funcionamento** (regras e fluxos essenciais)
- **Garantir testabilidade** (isolamento por camadas)
- **Qualidade mensurável** (cobertura ≥ 80%, mutação, benchmark)

### Funcionalidades críticas
- **CRUDs**: Authors, Books, Members, Loans, Payments
- **Regras de negócio**:
  - Limite de até **3 empréstimos ativos** por membro
  - **Bloqueio** de novo empréstimo se houver **pendência financeira**
  - **Multa R$ 2,00/dia** de atraso ao fechar empréstimo

## 3. Estratégia de Teste (níveis e critérios)
| Tipo | Objetivo | Critérios de aprovação |
|------|----------|------------------------|
| **Unitários** | Cobrir validações, branches e regras isoladas | 0 falhas, asserts relevantes |
| **Integração** | Exercitar Service + Repository + DB + API | 0 falhas, rollback/fixtures consistentes |
| **Funcionais (caixa‑preta)** | Validar regras e fluxos de negócio | Cenários de aceitação passam integralmente |
| **Cobertura** | Medir extensão da verificação | **Meta ≥ 80%** |
| **Mutação (incluído)** | Medir robustez da suíte | Nenhum mutante crítico deve sobreviver |
| **Benchmark** | Acompanhar tempo médio de operações | Estabilidade e tendência de melhoria |

## 4. Ambiente e Ferramentas
- **Python 3.12**, **FastAPI**, **SQLAlchemy/SQLite**
- **pytest**, **pytest-cov**, **pytest-html**
- **mutmut** (teste de mutação)
- **Relatos HTML**: unit/integration/functional/benchmark
  
## 5. Dados, Fixtures e Orquestração
- Seeds mínimos para autores, livros e membros
- Fixtures com **rollback** por cenário para isolamento
- TestClient FastAPI para integração/funcional

## 6. Riscos e Mitigações
| Risco | Mitigação |
|------|-----------|
| Cenários limite sub‑cobertos nas regras | Parametrização + casos derivados de mutantes sobreviventes |
| Baixa cobertura em `library.py` | Priorizar novos testes para ramos não cobertos |
| Estado compartilhado de DB | Fixtures de sessão + rollback por teste |

## 7. Métricas e Limiares
- **Cobertura Global**: alvo **≥ 80%** (atual: 84%)
- **Mutação**: **0 críticos sobreviventes** (atual: 27 sobreviventes não‑críticos)
- **Benchmark**: monitorar média (atual: ~68 ms) e tendência

## 8. Critérios de Entrada/Saída
**Entrada**: ambiente configurado, DB inicializado, dados mínimos prontos, scripts de teste disponíveis.  
**Saída**: testes críticos executados, cobertura ≥ meta, nenhum bug crítico em aberto, análise de mutação revisada.
