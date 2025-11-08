# Sistema de Biblioteca - FastAPI

## Descrição Geral
Este projeto implementa um sistema de Biblioteca utilizando FastAPI, com foco em arquitetura limpa, regras de negócio bem definidas e alta qualidade de testes automatizados.  
O sistema permite o cadastro de autores, livros, membros e o fluxo completo de empréstimos, incluindo cálculo de multas por atraso.

O objetivo deste projeto é demonstrar domínio de engenharia de software + validação de qualidade por diferentes níveis de testes automatizados (unitário, integração, funcional, cobertura, mutação e performance).

## Funcionalidades Principais
- Cadastro e gerenciamento de **Authors**
- Cadastro e gerenciamento de **Books**
- Cadastro e gerenciamento de **Members**
- Fluxo completo de empréstimos (**Loans**)
- Controle de pagamentos / multas (**Payments**)

## Regras de Negócio Implementadas
| Regra | Descrição |
|-------|-----------|
| Limite de Empréstimo | Membro pode ter no máximo 3 empréstimos ativos |
| Pendências Financeiras Bloqueiam Empréstimo | Se houver pagamento pendente → novo empréstimo é bloqueado |
| Multa por Atraso | R$2,00 por dia de atraso no fechamento do empréstimo |

## Stack Tecnológica
| Camada | Tecnologia |
|--------|------------|
| API / Controller | FastAPI |
| Serviço / Business Rules | Python / Services |
| ORM | SQLAlchemy |
| Banco | SQLite |
| Testes | pytest, pytest-cov, pytest-html, mutmut |

## Arquitetura (Visão Simplificada)

![Diagrama da Arquitetura](./diagrama.png)

## Diferenciais Técnicos do Projeto
- Testes Automatizados em múltiplos níveis
- Teste de Mutação incluído como métrica de robustez dos testes
- Métricas reais coletadas e reportadas com benchmark + cobertura
- Código modular favorecendo isolamentos e mocks

## Objetivo Educacional do Projeto
Este sistema foi desenvolvido como base para prática aprofundada de Engenharia de Software com foco em Qualidade de Software, não apenas entrega funcional.

O foco principal:
1) Provar funcionamento  
2) Provar testabilidade  
3) Provar qualidade mensurável via métricas

## Autores / Equipe
- **Guilherme de Abreu – 22.222.028-7**  
- **Kaique Fernandes – 22.221.011-4**
