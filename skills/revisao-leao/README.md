# 🦁 Skill: Revisão Leão — Checkup Mestre 360°

> **Resumo:** Suíte de auditoria completa desenvolvida para o ecossistema Talkative Automata (LCRM): validação E2E de 16 módulos operacionais, integração com a Evolution API v2, observabilidade em tempo real e conformidade regulatória (LGPD / GDPR / 18+).

---

## 📌 Os 16 Cenários Validados

1. **Autenticação & Sessão:** Login com e-mail/senha, emissão de JWT e verificação de maioridade legal (18+).
2. **Ciclo Completo de Contatos:** Cadastro, busca, formatação E.164 e exclusão de contato.
3. **Etiquetas & Tags:** Criação de tag com paleta de cores e limpeza de dados.
4. **Pipelines & Kanban:** Modo de edição e criação de funis de venda.
5. **Agentes de IA:** Cadastro de agente com instruções de sistema (prompts).
6. **Provedores LLM & Voz:** Configuração de chaves de API e vozes TTS (ElevenLabs).
7. **Instâncias WhatsApp:** Conexão com Evolution API v2 com terminologia em português ("Conectado", "Aguardando QR Code", "Desconectado").
8. **Automações de Mensagens:** Sequências de disparo por gatilhos.
9. **Disparos em Massa & Listas:** Mensagens interativas com botões e listas de transmissão.
10. **Mensagens Agendadas:** Agendamento e validação de calendário.
11. **Equipe & Convites:** Cadastro de atendentes e links assinados com expiração.
12. **Configurações do Workspace:** Edição de dados da empresa e suporte.
13. **Relatórios & NPS:** Painel de satisfação e gráficos analíticos.
14. **Logs & Diagnóstico:** Auditoria de requisições e eventos do sistema.
15. **Financeiro, Planos & Pix:** Visualização de faturas, contratação de extras e geração de cobrança Pix sem stubs.
16. **Super Admin & Saúde:** Governança global e métricas em tempo real (`GET /api/admin/system/health`).

---

## 🚀 Comandos Rápidos de Execução

```bash
# Execução completa em segundo plano (Headless)
python skills/revisao-leao/scripts/revisao_leao.py --password "SUA_SENHA" --headless

# Execução com visualização no navegador (Slow-Mo)
python skills/revisao-leao/scripts/revisao_leao.py --password "SUA_SENHA" --slow-mo 250

# Apenas limpeza de dados de testes residuais
python skills/revisao-leao/scripts/revisao_leao.py --clean-only
```

Consulte o arquivo [`SKILL.md`](./SKILL.md) para a especificação técnica completa.
