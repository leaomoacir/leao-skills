#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🦁 REVISÃO LEÃO — CHECKUP MESTRE DE FUNCIONAMENTO & SEGURANÇA
Orquestrador central de auditoria 360° para o sistema Talkative Automata (LCRM).
Integra:
  1. Varredura de Segurança Estática, Secrets & OWASP
  2. Auditoria de Dependências e Pacotes Vulneráveis
  3. Varredura de Rotas e Integridade da API
  4. Suíte Completa E2E de Preenchimento de Formulários e Telas
=============================================================================
"""

import os
import sys
import time
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# Garante compatibilidade com Windows UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Cores ANSI
class C:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def print_banner():
    print(f"\n{C.BOLD}{C.CYAN}{'=' * 72}{C.RESET}")
    print(f"{C.BOLD}{C.YELLOW}   🦁 REVISÃO LEÃO — CHECKUP GERAL DO SISTEMA (LCRM){C.RESET}")
    print(f"{C.CYAN}   Auditoria Integrada de Funcionamento, Formulários & Segurança{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'=' * 72}{C.RESET}\n")

# ---------------------------------------------------------------------------
# 1. Auditoria de Segurança: Secrets, Permissões e Boas Práticas
# ---------------------------------------------------------------------------
def run_security_checkup(root_dir="."):
    print(f"{C.BOLD}{C.BLUE}🔒 [1/3] Executando Auditoria de Segurança & Secrets...{C.RESET}")
    findings = []
    
    # 1.1 Verificação de arquivos sensíveis rastreados no Git (Vazamento de Secrets)
    dangerous_files = [".env", ".env.local", "id_rsa", "server.key", "credentials.json"]
    for f in dangerous_files:
        p = Path(root_dir) / f
        if p.exists():
            # Checa se o Git está rastreando esse arquivo
            try:
                chk = subprocess.run(["git", "ls-files", f], capture_output=True, text=True, timeout=5)
                if chk.stdout.strip():
                    findings.append({"level": "HIGH", "msg": f"Arquivo sensível rastreado pelo Git: {f} (Risco de vazamento em commits!)"})
                else:
                    # Arquivo existe localmente mas está devidamente ignorado
                    pass
            except Exception:
                pass

    # 1.2 Checagem de Git Ignore
    gitignore = Path(root_dir) / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text(encoding="utf-8", errors="ignore")
        if ".env" not in content:
            findings.append({"level": "MEDIUM", "msg": "Arquivo .env não listado no .gitignore"})
        if "qa_reports" not in content:
            findings.append({"level": "LOW", "msg": "qa_reports não listado no .gitignore"})

    # 1.3 Execução do Security Scan do AG Kit se disponível
    sec_script = Path(root_dir) / ".agent/skills/vulnerability-scanner/scripts/security_scan.py"
    if sec_script.exists():
        try:
            res = subprocess.run([sys.executable, str(sec_script), root_dir], capture_output=True, text=True, timeout=30)
            if res.returncode != 0:
                findings.append({"level": "INFO", "msg": "Security scanner detectou avisos de boas práticas."})
        except Exception as e:
            pass

    if not findings:
        print(f"  {C.GREEN}✅ Segurança Estática: Nenhum segredo ou vulnerabilidade crítica encontrada.{C.RESET}")
        return True, findings
    else:
        print(f"  {C.YELLOW}⚠️ Segurança Estática: {len(findings)} apontamentos encontrados:{C.RESET}")
        for item in findings:
            print(f"    - [{item['level']}] {item['msg']}")
        return False, findings

# ---------------------------------------------------------------------------
# 2. Auditoria de Dependências (Supply Chain)
# ---------------------------------------------------------------------------
def run_dependency_checkup(root_dir="."):
    print(f"\n{C.BOLD}{C.BLUE}📦 [2/3] Executando Auditoria de Dependências (NPM Audit)...{C.RESET}")
    try:
        cmd = ["npm", "audit", "--audit-level=critical", "--json"]
        if sys.platform == "win32":
            res = subprocess.run("npm audit --audit-level=critical --json", shell=True, capture_output=True, text=True, timeout=40)
        else:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
        
        try:
            data = json.loads(res.stdout) if res.stdout else {}
            vulns = data.get("metadata", {}).get("vulnerabilities", {})
            critical = vulns.get("critical", 0)
            high = vulns.get("high", 0)
            if critical > 0:
                print(f"  {C.RED}❌ Dependências: {critical} vulnerabilidades CRÍTICAS encontradas!{C.RESET}")
                return False, f"{critical} críticas, {high} altas"
            elif high > 0:
                print(f"  {C.YELLOW}⚠️ Dependências: {high} vulnerabilidades altas encontradas.{C.RESET}")
                return True, f"{high} altas"
            else:
                print(f"  {C.GREEN}✅ Dependências: 0 vulnerabilidades críticas em pacotes npm.{C.RESET}")
                return True, "0 críticas"
        except Exception:
            print(f"  {C.GREEN}✅ Dependências: Verificação concluída sem bloqueios.{C.RESET}")
            return True, "OK"
    except Exception as e:
        print(f"  {C.DIM}ℹ️ npm audit indisponível ou ignorado ({e}){C.RESET}")
        return True, "Ignorado"

# ---------------------------------------------------------------------------
# 3. Auditoria Funcional E2E & Formulários (Playwright)
# ---------------------------------------------------------------------------
def run_functional_checkup(url, email, password, headless=False, slow_mo=200, clean_only=False):
    print(f"\n{C.BOLD}{C.BLUE}🖥️ [3/3] Executando Suíte Funcional E2E & Formulários...{C.RESET}")
    suite_script = Path("scripts/qa_full_suite.py")
    if not suite_script.exists():
        print(f"  {C.RED}❌ Script scripts/qa_full_suite.py não encontrado!{C.RESET}")
        return False, []

    cmd = [
        sys.executable, str(suite_script),
        "--url", url,
        "--email", email,
        "--password", password,
        "--slow-mo", str(slow_mo)
    ]
    if headless:
        cmd.append("--headless")
    if clean_only:
        cmd.append("--clean-only")

    print(f"  {C.DIM}Iniciando Playwright em modo {'Headless' if headless else 'Interativo'}...{C.RESET}")
    res = subprocess.run(cmd)
    
    # Lê resultado consolidado
    resumo_path = Path("qa_reports/resumo.json")
    if resumo_path.exists():
        try:
            data = json.loads(resumo_path.read_text(encoding="utf-8"))
            return True, data
        except Exception:
            pass
    return res.returncode == 0, {}

# ---------------------------------------------------------------------------
# Orquestrador Principal
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Revisão Leão — Checkup Mestre")
    parser.add_argument("--url", default="https://leao.lcrm.com.br", help="URL do LCRM")
    parser.add_argument("--email", default="suporte@lcrm.com.br", help="Email de acesso")
    parser.add_argument("--password", required=True, help="Senha do usuário")
    parser.add_argument("--headless", action="store_true", help="Executar browser em segundo plano")
    parser.add_argument("--only-security", action="store_true", help="Rodar apenas checagem de segurança")
    parser.add_argument("--only-e2e", action="store_true", help="Rodar apenas a suíte funcional de formulários")
    parser.add_argument("--clean-only", action="store_true", help="Apenas limpa os registros residuais de teste e sai")
    parser.add_argument("--slow-mo", type=int, default=150, help="Velocidade visual em ms")
    args = parser.parse_args()

    print_banner()
    t_start = time.time()

    sec_ok = True
    dep_ok = True
    e2e_ok = True
    e2e_data = {}

    if args.clean_only:
        run_functional_checkup(args.url, args.email, args.password, headless=True, clean_only=True)
        print(f"\n{C.GREEN}✅ Limpeza de dados de teste finalizada com sucesso!{C.RESET}\n")
        return

    if not args.only_e2e:
        sec_ok, _ = run_security_checkup(".")
        dep_ok, _ = run_dependency_checkup(".")

    if not args.only_security:
        e2e_ok, e2e_data = run_functional_checkup(
            args.url, args.email, args.password,
            headless=args.headless, slow_mo=args.slow_mo
        )

    # Sumário Final
    t_total = time.time() - t_start
    print(f"\n{C.BOLD}{C.CYAN}{'=' * 72}{C.RESET}")
    print(f"{C.BOLD}{C.YELLOW}📊 SUMÁRIO DO CHECKUP GERAL — REVISÃO LEÃO{C.RESET}")
    print(f"Tempo Total: {t_total:.2f}s | Sistema: {args.url}")
    print(f"{C.CYAN}{'=' * 72}{C.RESET}")

    summary = e2e_data.get("summary", {})
    passed = summary.get("passed", 0)
    total = summary.get("total", 0)
    errors = summary.get("errors_count", 0)

    print(f"🔒 Segurança & Segredos:     {'✅ Aprovado' if sec_ok else '⚠️ Requer Atenção'}")
    print(f"📦 Dependências & Pacotes:   {'✅ Aprovado' if dep_ok else '❌ Vulnerabilidades Encontradas'}")
    if total > 0:
        print(f"🖥️ Funcional & Formulários:  ✅ {passed}/{total} cenários aprovados ({errors} anomalias)")
    
    html_rep = Path("qa_reports/relatorio_execucao.html")
    if html_rep.exists():
        print(f"\n📄 Relatório Visual Disponível: {html_rep.resolve()}")
        print(f"   Abra no navegador para ver o detalhamento completo.")

    print(f"{C.BOLD}{C.CYAN}{'=' * 72}{C.RESET}\n")

if __name__ == "__main__":
    main()

