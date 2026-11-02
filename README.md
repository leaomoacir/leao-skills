# 🦁 Leão Skills Hub (`leao-skills`)

> **Repositório Oficial de Skills, Protocolos de Auditoria e Diretrizes Técnicas Personalizadas do Ecossistema Leão.**

Este repositório centraliza exclusivamente as **skills proprietárias e customizadas** desenvolvidas para elevar a qualidade de engenharia, a automação de testes de ponta a ponta e a governança operacional com Inteligência Artificial.

---

## 📚 Skills Disponíveis no Hub

| Skill | Escopo | Objetivo Principal | Documentação |
|---|---|---|---|
| [**`qa-360-audit`**](./skills/qa-360-audit/) | **Universal (Qualquer Projeto)** | Protocolo agnóstico de testes 360°: submissões profundas, ciclo CRUD real, captura de exceções de console/rede, higienização de banco e relatórios HTML. | [Ver Resumo](./skills/qa-360-audit/README.md) · [SKILL.md](./skills/qa-360-audit/SKILL.md) |
| [**`revisao-leao`**](./skills/revisao-leao/) | **Talkative Automata (LCRM)** | Checkup mestre 360° de funcionamento E2E (16 cenários reais), proxy Evolution API v2, observabilidade e conformidade com a LGPD e GDPR. | [Ver Resumo](./skills/revisao-leao/README.md) · [SKILL.md](./skills/revisao-leao/SKILL.md) |

---

## 🛠️ Como Utilizar em Seus Projetos

### 1. Clonar ou Adicionar como Submódulo Git
Para plugar as skills do Leão em qualquer repositório de desenvolvimento:

```bash
# Adicionar como submódulo dentro da pasta .agent/
git submodule add https://github.com/leaomoacir/leao-skills.git .agent/leao-skills
```

### 2. Copiar Apenas a Skill Desejada
Se preferir copiar apenas a skill universal para outro projeto (ex: um frontend Next.js ou backend FastAPI):
```bash
cp -r skills/qa-360-audit /caminho/do/seu/projeto/.agent/skills/
```

### 3. Invocação no Prompt do Agente
Quando estiver pareando com o assistente de IA (Antigravity, Cursor, Claude Code, Windsurf), declare:
```markdown
🤖 Applying knowledge of @[skills/qa-360-audit]...
```

---

## ⚖️ Governança & Licença
Desenvolvido por **Moacir Leão** para padronização de automações, testes e engenharia de software de alta performance.
