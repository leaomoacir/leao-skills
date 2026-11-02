# 🎯 Skill: QA 360° Audit — Protocolo Universal de Testes

> **Resumo:** Protocolo agnóstico de testes automatizados E2E, submissão real de formulários, interceptação de erros assíncronos no console/rede, higienização de dados e geração de relatórios visuais HTML/JSON para **qualquer projeto web ou API**.

---

## 📌 Parâmetros Técnicos Universais (CLI Spec)

| Parâmetro | Padrão | Finalidade |
|---|---|---|
| `--target-url <URL>` | `http://localhost:3000` | Endereço base do ambiente testado (local, staging ou prod). |
| `--auth-user <USER>` | *(Opcional)* | Credencial de login automático para inicialização de sessão. |
| `--auth-password <PASS>` | *(Opcional)* | Senha do usuário de teste. |
| `--headless` | `False` | Execução em segundo plano para pipelines de CI/CD. |
| `--slow-mo <MS>` | `0` | Velocidade reduzida (ex: 200ms) para inspeção visual humana. |
| `--scenario <ID>` | `all` | Execução isolada de um cenário de teste específico. |
| `--filter <REGEX>` | `""` | Filtra cenários por nome ou tags. |
| `--clean-only` | `False` | Executa exclusivamente a purga de dados residuais criados nos testes. |
| `--only-security` | `False` | Executa apenas os gates de segurança e verificação de segredos. |
| `--report-dir <DIR>` | `./qa_reports` | Diretório de destino dos relatórios visuais e capturas de tela. |

---

## 🚀 Como Utilizar em Outros Projetos

1. Copie a pasta `skills/qa-360-audit/` para a pasta `.agent/skills/` do seu projeto.
2. Invoque o agente com:
   ```markdown
   🤖 Applying knowledge of @[skills/qa-360-audit]...
   ```
3. Execute o runner base:
   ```bash
   python skills/qa-360-audit/scripts/universal_qa_runner.py --url "http://localhost:3000" --headless
   ```

Consulte o arquivo [`SKILL.md`](./SKILL.md) para a especificação técnica completa.
