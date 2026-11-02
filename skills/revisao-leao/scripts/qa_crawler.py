import sys
import time
import json
import argparse
from playwright.sync_api import sync_playwright

ROUTES_TO_TEST = [
    ("/app", "Dashboard"),
    ("/agents", "Agentes de IA"),
    ("/instances", "Instâncias WhatsApp"),
    ("/llm", "Provedores LLM"),
    ("/conversations", "Conversas / Chat"),
    ("/pipelines", "Funis / Pipelines"),
    ("/labels", "Etiquetas"),
    ("/automations", "Automações"),
    ("/settings", "Configurações"),
    ("/team", "Equipe / Atendentes"),
    ("/contacts", "Contatos"),
    ("/nps", "Pesquisa NPS"),
    ("/reports", "Relatórios"),
    ("/broadcasts", "Disparos em Massa"),
    ("/scheduled", "Mensagens Agendadas"),
    ("/billing", "Assinatura & Planos"),
    ("/ajuda", "Central de Ajuda"),
    ("/leao", "Painel Super Admin"),
    ("/logs", "Logs do Sistema"),
]

def run_qa_crawler(base_url: str, email: str, password: str, headless: bool = True):
    print(f"\n=======================================================")
    print(f"🤖 QA AUTONOMOUS CRAWLER — TALKATIVE AUTOMATA (LCRM)")
    print(f"Target: {base_url}")
    print(f"User: {email}")
    print(f"=======================================================\n")

    captured_errors = []
    captured_warnings = []
    visited_pages = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 QA-Agent/1.0"
        )
        page = context.new_page()

        # Listeners de erros
        def on_console(msg):
            text = msg.text
            if msg.type == "error":
                if "favicon" not in text and "apple-touch-icon" not in text:
                    captured_errors.append({"url": page.url, "type": "Console Error", "message": text})
                    print(f"  ❌ [Console Error] {text[:140]}")
            elif msg.type == "warning" and "DevTools" not in text:
                captured_warnings.append({"url": page.url, "message": text})

        def on_page_error(err):
            captured_errors.append({"url": page.url, "type": "Uncaught Exception", "message": str(err)})
            print(f"  🔥 [Page Crash] {str(err)[:140]}")

        def on_response(response):
            if response.status >= 400 and "favicon" not in response.url:
                msg = f"HTTP {response.status} em {response.request.method} {response.url}"
                captured_errors.append({"url": page.url, "type": f"HTTP {response.status}", "message": msg})
                print(f"  ❌ [{response.status}] {response.request.method} {response.url}")

        page.on("console", on_console)
        page.on("pageerror", on_page_error)
        page.on("response", on_response)

        # 1. Login
        print(f"🔑 Realizando autenticação em {base_url}/auth...")
        page.goto(f"{base_url}/auth", wait_until="networkidle")
        page.wait_for_timeout(2000)

        try:
            # Garante que a aba Entrar esteja ativa
            login_tab = page.locator('[role="tab"]:has-text("Entrar")')
            if login_tab.count() > 0:
                login_tab.first.click()
                page.wait_for_timeout(500)

            email_input = page.locator('form input[type="email"]')
            password_input = page.locator('form input[type="password"]')
            
            if email_input.count() > 0 and password_input.count() > 0:
                email_input.first.fill(email)
                password_input.first.fill(password)
                
                submit_btn = page.locator('form button[type="submit"]:visible')
                if submit_btn.count() > 0:
                    print("  Submetendo credenciais...")
                    submit_btn.first.click()
                    print("  Aguardando resposta do login...")
                    page.wait_for_timeout(5000)
            else:
                print("  Campos de login não detectados diretamente.")
        except Exception as e:
            print(f"  Erro no preenchimento de login: {e}")

        # Verifica se o token foi gravado
        token = page.evaluate("() => localStorage.getItem('access_token')")
        if token:
            print(f"  ✅ Autenticado com sucesso! Token: {token[:20]}...")
        else:
            print(f"  ⚠️ Nenhum token encontrado no localStorage após submissão de login.")

        # 2. Navegação em todas as rotas
        for path, label in ROUTES_TO_TEST:
            target_url = f"{base_url}{path}"
            print(f"\n🌐 Testando rota: {label} ({path})")
            start_errors_count = len(captured_errors)
            
            try:
                page.goto(target_url, wait_until="networkidle", timeout=15000)
                page.wait_for_timeout(2500)
                
                content_len = len(page.content())
                
                # Procura botões e abas navegáveis
                buttons = page.locator('button:visible, [role="tab"]:visible')
                btn_count = min(buttons.count(), 5)
                
                for i in range(btn_count):
                    try:
                        btn = buttons.nth(i)
                        btn_text = btn.inner_text().strip()
                        danger_words = ["sair", "logout", "excluir", "deletar", "delete", "cancelar", "remover"]
                        if btn_text and not any(w in btn_text.lower() for w in danger_words):
                            btn.click(timeout=1500)
                            page.wait_for_timeout(500)
                    except Exception:
                        pass

                page_errors = len(captured_errors) - start_errors_count
                status = "✅ OK" if page_errors == 0 else f"❌ {page_errors} erros"
                visited_pages.append({
                    "path": path,
                    "label": label,
                    "status": status,
                    "errors_count": page_errors
                })
                print(f"  Status: {status} (Tamanho DOM: {content_len} bytes)")

            except Exception as e:
                captured_errors.append({"url": target_url, "type": "Navigation Crash", "message": str(e)})
                print(f"  💥 Falha de navegação na rota {path}: {e}")
                visited_pages.append({
                    "path": path,
                    "label": label,
                    "status": "💥 Falha",
                    "errors_count": 1
                })

        browser.close()

    # Relatório final
    print(f"\n=======================================================")
    print(f"📊 RESUMO DO AUDIT DE QA")
    print(f"Total de Páginas Testadas: {len(visited_pages)}")
    print(f"Total de Erros Capturados: {len(captured_errors)}")
    print(f"=======================================================\n")

    for p in visited_pages:
        print(f"- {p['label']} ({p['path']}): {p['status']}")

    if captured_errors:
        print(f"\n🔍 DETALHAMENTO DOS ERROS ({len(captured_errors)}):")
        for idx, err in enumerate(captured_errors, 1):
            print(f"{idx}. [{err['type']}] na URL {err['url']}:")
            print(f"   {err['message']}\n")
    else:
        print("\n🎉 ZERO ERROS NO CONSOLE DO REACT! Todas as páginas carregaram perfeitamente.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QA Autonomous Crawler")
    parser.add_argument("--url", default="https://leao.lcrm.com.br", help="Base URL")
    parser.add_argument("--email", default="suporte@lcrm.com.br", help="User email")
    parser.add_argument("--password", required=True, help="User password")
    parser.add_argument("--headed", action="store_true", help="Run with browser visible")
    args = parser.parse_args()

    run_qa_crawler(args.url, args.email, args.password, headless=not args.headed)
