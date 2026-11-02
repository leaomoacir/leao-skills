---
name: revisao-leao
description: "Checkup mestre 360° para Talkative Automata (LCRM): auditoria completa de funcionamento E2E (rotas, formulários, modais, dados), integração Evolution API v2, observabilidade e auditoria de segurança (vulnerabilidades, secrets, conformidade LGPD/GDPR e OWASP)."
when_to_use: "Quando o usuário solicitar revisão do leao, checkup do sistema, auditoria de funcionamento, testes de formulários, auditoria de segurança, verificação de webhooks Evolution API ou verificação pré-deploy."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# 🦁 Skill: Revisão Leão — Checkup Mestre 360° (Funcionamento, Evolution API & Segurança)

> "Um sistema robusto não apenas compila: ele valida cada formulário, protege cada tenant, audita webhooks em tempo real e impede qualquer brecha de segurança ou conformidade legal antes do cliente final notar."

Esta skill fornece o protocolo e o ecossistema de scripts automatizados para executar um **checkup 360°** no sistema **Talkative Automata (LCRM)**, cobrindo tanto a **estabilidade operacional (UX/E2E)** quanto a **postura de segurança defensiva, conformidade regulatória (LGPD/GDPR/18+) e conectividade de mensageria**.

---

## 🛠️ Matriz de Scripts de Auditoria

| Script | Foco | O Que Executa | Como Rodar |
|---|---|---|---|
| [`scripts/revisao_leao.py`](file:///c:/Users/MKT-G/Documents/GitHub/talkative-automata/scripts/revisao_leao.py) | **Mestre 360°** | Segurança + Dependências + Suíte Funcional E2E Completa | `python scripts/revisao_leao.py --password "..."` |
| [`scripts/qa_full_suite.py`](file:///c:/Users/MKT-G/Documents/GitHub/talkative-automata/scripts/qa_full_suite.py) | **Funcional / E2E (16 Cenários)** | 16 cenários com formulários reais, modais, billing e HTML report | `python scripts/qa_full_suite.py --password "..."` |
| [`scripts/qa_deep_tester.py`](file:///c:/Users/MKT-G/Documents/GitHub/talkative-automata/scripts/qa_deep_tester.py) | **Ciclo de Vida CRUD** | Criação e exclusão real de tags, contatos e agentes | `python scripts/qa_deep_tester.py --password "..."` |
| [`scripts/qa_crawler.py`](file:///c:/Users/MKT-G/Documents/GitHub/talkative-automata/scripts/qa_crawler.py) | **Varredura P0** | Crawl em todas as rotas com captura de console e crashes de página | `python scripts/qa_crawler.py --password "..."` |
| `.agent/scripts/checklist.py` | **Qualidade & Lint** | Lint, tipos TypeScript, integridade de schema Prisma | `python .agent/scripts/checklist.py .` |
| `.agent/skills/vulnerability-scanner/scripts/security_scan.py` | **Segurança Estática** | Scan de vulnerabilidades de código, segredos e tokens | `python .agent/skills/vulnerability-scanner/scripts/security_scan.py .` |

---

## 📋 1. Checkup de Funcionamento & Formulários (16 Cenários)

A suíte funcional testa ativamente o comportamento do usuário final na interface web, simulando preenchimentos e submissões reais:

### Módulos Validados na Suíte Completa:
1. **Autenticação & Emissão de JWT (`/auth`)**: Preenchimento de login com e-mail/senha, emissão de JWT, gravação no `localStorage` e verificação de maioridade legal (18+).
2. **Ciclo Completo de Contatos (`/contacts`)**: Abertura do modal "Novo contato", preenchimento de nome, telefone WhatsApp no formato internacional e notas, submissão e filtro na listagem.
3. **Etiquetas & Tags (`/labels`)**: Adição de nova etiqueta, seleção de cor na paleta interativa, validação de renderização no DOM e exclusão (limpeza de dados).
4. **Kanban & Funis de Vendas (`/pipelines`)**: Alternância para modo de edição, abertura do modal e cadastro de novo pipeline.
5. **Agentes de IA (`/agents`)**: Modal de novo agente, preenchimento de nome e System Instructions / Prompts, verificação na listagem.
6. **Provedores de IA & Voz (`/llm`)**: Configuração de credenciais de modelos (OpenAI, Groq, Anthropic) e parâmetros de voz Text-to-Speech (ElevenLabs).
7. **Instâncias WhatsApp & Evolution API (`/instances`)**: Validação do formulário de criação de instâncias, resolução de proxy Evolution API e nomenclatura em português ("Conectado", "Aguardando QR Code", "Desconectado").
8. **Automações de Mensagens (`/automations`)**: Configuração de sequências de disparo disparadas por inatividade ou gatilhos de etiqueta.
9. **Disparos em Massa & Listas (`/broadcasts`)**: Criação de listas de destinatários, mensagens interativas com botões e validação do fluxo de campanhas.
10. **Mensagens Agendadas (`/scheduled`)**: Agendamento de mensagens futuras e validação de datas.
11. **Gestão de Equipe & Convites (`/team`)**: Modal de convite de membros e formulário de cadastro de atendentes.
12. **Configurações do Workspace (`/settings`)**: Edição dos dados da empresa, telefone de suporte e persistência de dados.
13. **NPS & Pesquisas de Satisfação (`/nps` & `/reports`)**: Carregamento de relatórios, gráficos analíticos e notas de promotores/detratores.
14. **Logs do Sistema & Auditoria (`/logs`)**: Painel de registros de eventos e requisições HTTP do sistema.
15. **Financeiro, Planos & Assinaturas (`/billing`)**: Verificação da visualização de faturas, contratação de extras, geração de Pix e cancelamentos (sem stubs).
16. **Super Admin & Saúde do Sistema (`/leao`)**: Governança global de instâncias, aba de Usuários blindada e painel de Saúde do Sistema em tempo real (`GET /api/admin/system/health`).

### Geração de Relatórios Visuais
Após a execução de `qa_full_suite.py` ou `revisao_leao.py`:
- **Relatório HTML**: Salvo em `qa_reports/relatorio_execucao.html` contendo cards de resumo, tempo de resposta por formulário e console logs.
- **Relatório JSON**: Salvo em `qa_reports/resumo.json` para ingestão em pipelines de CI/CD.
- **Screenshots Automáticos**: Salvos em `qa_reports/screenshots/` em caso de qualquer quebra ou falha visual.

---

## 🔌 2. Protocolo de Integração com a Evolution API v2

A comunicação entre o LCRM e a Evolution API v2 (`https://mwapi.lcrm.com.br`) obedece a regras rígidas de compatibilidade:

1. **Payload Aninhado de Webhook (`POST /webhook/set/{instance}`)**:
   - A partir da versão 2.3.x da Evolution API, os parâmetros de webhook devem ser aninhados sob a chave `"webhook": { enabled, url, byEvents, events }`.
   - Caso enviado na raiz, a API rejeita com `400 Bad Request: instance requires property "webhook"`.
2. **Resolução de Instância por Query String**:
   - O webhook deve ser cadastrado com `?instance={instance_name}` para garantir que o worker consiga identificar o registro da instância mesmo quando a Evolution não enviar o nome no corpo.
3. **Eventos Mandatórios**:
   - Mensagens: `MESSAGES_UPSERT`, `MESSAGES_UPDATE`, `MESSAGES_DELETE`, `SEND_MESSAGE`.
   - Conectividade: `CONNECTION_UPDATE`, `QRCODE_UPDATED`.
   - Sincronização: `CONTACTS_SET`, `CONTACTS_UPSERT`, `CONTACTS_UPDATE`, `CHATS_SET`, `CHATS_UPSERT`, `CHATS_UPDATE`.
4. **Recepção em Zero-Delay**:
   - O controller `/api/webhooks/evolution` devolve `200 OK` imediatamente em menos de 20ms e encaminha o payload para a fila BullMQ Redis. O worker faz o processamento pesado e emite instantaneamente via Socket.io (`new_message`, `conversation_updated`).

---

## ⚖️ 3. Conformidade Legal & Proteção de Dados (LGPD / GDPR / 18+)

O LCRM implementa governança de dados e proteção à privacidade por design:

| Requisito Legal | Implementação no LCRM | Referência Legal |
|---|---|---|
| **Restrição de Idade (18+)** | Checkbox mandatório no cadastro (`Auth.tsx`) e persistência de metadados de auditoria (`auth.controller.ts`). | ECA (Lei 8.069/90) / COPPA |
| **Consentimento de Cookies** | Componente flutuante [`CookieConsentBanner.tsx`](file:///c:/Users/MKT-G/Documents/GitHub/talkative-automata/src/components/CookieConsentBanner.tsx) para visitantes com separação entre cookies essenciais e analíticos. | LGPD Art. 7º e 8º / GDPR |
| **Transparência & Direitos** | Páginas públicas [`/terms`](/terms) e [`/privacy`](/privacy) detalhando finalidade de tratamento e contato com Encarregado de Dados (DPO). | LGPD Art. 18 |
| **Mecanismo Anti-Spam (Opt-Out)** | Detecção automática de palavras-chave (`SAIR`, `PARAR`, `CANCELAR`, `STOP`, `DESCADASTRAR`, `NÃO QUERO`) no webhook worker, pausando a IA e marcando etiqueta `OPT_OUT`. | Anatel / Meta WhatsApp Business Policy |

---

## 🔒 4. Checkup de Segurança Defensiva & OWASP

### Checklist de Segurança Obrigatório

| Verificação | O Que Auditar | Risco Mitigado |
|---|---|---|
| **Isolamento Multi-Tenant** | Todas as queries Prisma filtram `tenant_id` explicitamente | **A01: Quebra de Controle de Acesso (IDOR)** |
| **Sanitização de Secrets** | Ausência de `.env`, senhas ou chaves de API commitadas | **A04: Falhas Criptográficas** |
| **Validação de Token JWT** | Verificação de assinatura e expiração no backend | **A07: Falhas de Identificação/Autenticação** |
| **Injeções SQL & NoSQL** | Uso estrito de Prisma ORM parametrizado | **A05: Injection** |
| **Proteção de Headers** | Helmet habilitado, CORS restrito ao domínio leao | **A02: Configuração Incorreta** |
| **Dependências & Supply Chain** | `npm audit` sem vulnerabilidades críticas | **A03: Dependências Vulneráveis** |

---

## 🚀 5. Comandos de Execução Rápida

### A. Executar o Checkup Completo 360° (Recomendado)
```powershell
python scripts/revisao_leao.py --password "SUA_SENHA_AQUI"
```

### B. Executar com Visualização Interativa do Navegador (Slow-Mo)
```powershell
python scripts/revisao_leao.py --password "SUA_SENHA_AQUI" --slow-mo 250
```

### C. Executar em Segundo Plano (Headless / Silencioso)
```powershell
python scripts/revisao_leao.py --password "SUA_SENHA_AQUI" --headless
```

### D. Executar Apenas Limpeza de Dados de Testes Residuais (Purge)
```powershell
python scripts/revisao_leao.py --password "SUA_SENHA_AQUI" --clean-only
```

### E. Executar Apenas Auditoria de Segurança & Dependências
```powershell
python scripts/revisao_leao.py --password "qualquer" --only-security
```

### F. Executar Apenas Testes de Rotas e Telas Rápidas
```powershell
python scripts/qa_crawler.py --password "SUA_SENHA_AQUI"
```
