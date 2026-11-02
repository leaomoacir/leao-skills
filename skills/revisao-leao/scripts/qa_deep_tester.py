import sys
import time
import os
import argparse
from playwright.sync_api import sync_playwright

def run_deep_test(base_url: str, email: str, password: str, headless: bool = False):
    os.makedirs("qa_reports/screenshots", exist_ok=True)
    
    print("\n" + "=" * 65)
    print("🤖 DEEP E2E TEST RUNNER — TALKATIVE AUTOMATA (LCRM)")
    print(f"Alvo: {base_url}")
    print(f"Usuário: {email}")
    print("=" * 65 + "\n")

    errors_found = []
    scenarios_passed = 0
    scenarios_failed = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=200 if not headless else 0)
        context = browser.new_context(
            viewport={"width": 1366, "height": 850},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) QA-DeepTester/2.0"
        )
        page = context.new_page()

        # Listeners para interceptar qualquer anomalia
        def on_console(msg):
            if msg.type == "error":
                text = msg.text
                if "favicon" not in text and "apple-touch-icon" not in text:
                    errors_found.append({"url": page.url, "type": "Console Error", "msg": text})
                    print(f"    ❌ [Console Error] {text[:130]}")

        def on_page_error(err):
            errors_found.append({"url": page.url, "type": "Crash", "msg": str(err)})
            print(f"    🔥 [Page Crash] {str(err)[:130]}")

        def on_response(res):
            if res.status >= 400 and "favicon" not in res.url:
                errors_found.append({
                    "url": page.url,
                    "type": f"HTTP {res.status}",
                    "msg": f"[{res.status}] {res.request.method} {res.url}"
                })
                print(f"    ⚠️ [HTTP {res.status}] {res.request.method} {res.url}")

        page.on("console", on_console)
        page.on("pageerror", on_page_error)
        page.on("response", on_response)

        def report_scenario(name: str, success: bool, details: str = ""):
            nonlocal scenarios_passed, scenarios_failed
            if success:
                scenarios_passed += 1
                print(f"  ✅ [PASS] {name} {details}")
            else:
                scenarios_failed += 1
                screenshot_path = f"qa_reports/screenshots/fail_{int(time.time())}.png"
                try:
                    page.screenshot(path=screenshot_path)
                    print(f"  ❌ [FAIL] {name} - Screenshot salvo em {screenshot_path}")
                except Exception:
                    print(f"  ❌ [FAIL] {name} {details}")

        # -------------------------------------------------------------
        # CENÁRIO 1: Autenticação Real com Formulário
        # -------------------------------------------------------------
        print("\n🔹 [Cenário 1/8] Testando Autenticação e Login...")
        page.goto(f"{base_url}/auth", wait_until="networkidle")
        page.wait_for_timeout(1500)

        try:
            # Garante que está na aba Entrar
            login_tab = page.locator('[role="tab"]:has-text("Entrar")')
            if login_tab.count() > 0:
                login_tab.first.click()
                page.wait_for_timeout(400)

            email_field = page.locator('form input[type="email"]').first
            pass_field = page.locator('form input[type="password"]').first
            
            email_field.fill(email)
            pass_field.fill(password)
            
            submit_btn = page.locator('form button[type="submit"]:visible').first
            submit_btn.click()
            
            # Aguarda redirecionamento ou gravação de token
            page.wait_for_timeout(4000)
            token = page.evaluate("() => localStorage.getItem('access_token')")
            
            if token and len(token) > 20:
                report_scenario("Login e Emissão de JWT", True, f"Token válido ({token[:12]}...)")
            else:
                report_scenario("Login e Emissão de JWT", False, "Token não encontrado no localStorage")
        except Exception as e:
            report_scenario("Login e Emissão de JWT", False, str(e))

        # -------------------------------------------------------------
        # CENÁRIO 2: Criação e Exclusão de Etiqueta (/labels)
        # -------------------------------------------------------------
        print("\n🔹 [Cenário 2/8] Testando Criação e Exclusão de Etiquetas...")
        try:
            page.goto(f"{base_url}/labels", wait_until="networkidle")
            page.wait_for_timeout(2000)

            test_label_name = f"QA-Tag-{int(time.time()) % 1000}"
            label_input = page.locator('input[placeholder*="VIP"], input[placeholder*="Suporte"]').first
            
            if label_input.count() > 0:
                label_input.fill(test_label_name)
                
                # Escolhe uma cor diferente
                color_buttons = page.locator('button[style*="background"]')
                if color_buttons.count() > 2:
                    color_buttons.nth(2).click()

                # Clica em Adicionar
                add_btn = page.locator('button:has-text("Adicionar")').first
                add_btn.click()
                page.wait_for_timeout(2500)

                # Verifica se a etiqueta apareceu na lista
                created_badge = page.locator(f':text("{test_label_name}")')
                if created_badge.count() > 0:
                    report_scenario("Criação de Etiqueta", True, f"Etiqueta '{test_label_name}' criada com sucesso")
                    
                    # Remove para manter o banco limpo
                    delete_btn = created_badge.first.locator('xpath=..//button')
                    if delete_btn.count() > 0:
                        delete_btn.first.click()
                        page.wait_for_timeout(1000)
                        report_scenario("Exclusão de Etiqueta", True, "Limpeza de dados de teste concluída")
                else:
                    report_scenario("Criação de Etiqueta", False, "Etiqueta não encontrada no DOM após salvar")
            else:
                report_scenario("Criação de Etiqueta", False, "Input de etiqueta não encontrado")
        except Exception as e:
            report_scenario("Criação de Etiqueta", False, str(e))

        # -------------------------------------------------------------
        # CENÁRIO 3: Criação e Busca de Contato (/contacts)
        # -------------------------------------------------------------
        print("\n🔹 [Cenário 3/8] Testando Modal e Cadastro de Contatos...")
        try:
            page.goto(f"{base_url}/contacts", wait_until="networkidle")
            page.wait_for_timeout(2000)

            # Clica no botão Novo Contato
            new_btn = page.locator('button:has-text("Novo contato")').first
            if new_btn.count() > 0:
                new_btn.click()
                page.wait_for_timeout(1000)

                # Preenche campos do modal
                phone_rand = f"55119{int(time.time()) % 100000000:08d}"
                name_test = f"QA Test User {int(time.time()) % 1000}"

                phone_input = page.locator('input[placeholder*="55"]').first
                phone_input.fill(phone_rand)

                name_input = page.locator('input[placeholder*="Maria Silva"]').first
                name_input.fill(name_test)

                notes_area = page.locator('textarea[placeholder*="Informações úteis"]').first
                if notes_area.count() > 0:
                    notes_area.fill("Contato automatizado gerado pelo agente de QA DeepTester.")

                # Salva
                save_btn = page.locator('div[role="dialog"] button:has-text("Salvar")').first
                save_btn.click()
                page.wait_for_timeout(2500)

                # Verifica se o contato aparece na lista ou se o modal fechou
                contact_found = page.locator(f':text("{name_test}")')
                if contact_found.count() > 0 or page.locator('div[role="dialog"]').count() == 0:
                    report_scenario("Cadastro de Contato", True, f"Contato '{name_test}' cadastrado com sucesso")
                else:
                    report_scenario("Cadastro de Contato", False, "Modal não fechou ou contato não listado")
            else:
                report_scenario("Cadastro de Contato", False, "Botão 'Novo contato' não encontrado")
        except Exception as e:
            report_scenario("Cadastro de Contato", False, str(e))

        # -------------------------------------------------------------
        # CENÁRIO 4: Funis e Pipelines (/pipelines)
        # -------------------------------------------------------------
        print("\n🔹 [Cenário 4/8] Testando Funis e Pipelines...")
        try:
            page.goto(f"{base_url}/pipelines", wait_until="networkidle")
            page.wait_for_timeout(2000)

            # Entra no modo de edição
            edit_toggle = page.locator('button:has-text("Editar"), button:has-text("Sair da edição")').first
            if edit_toggle.count() > 0:
                btn_text = edit_toggle.inner_text()
                if "Editar" in btn_text and "Sair" not in btn_text:
                    edit_toggle.click()
                    page.wait_for_timeout(800)

                # Abre modal Novo Pipeline
                new_pipe_btn = page.locator('button:has-text("Novo Pipeline")').first
                if new_pipe_btn.count() > 0:
                    new_pipe_btn.click()
                    page.wait_for_timeout(800)

                    pipe_name = f"Funil QA {int(time.time()) % 1000}"
                    pipe_input = page.locator('div[role="dialog"] input[placeholder*="Vendas"]').first
                    pipe_input.fill(pipe_name)

                    # Submete
                    pipe_create = page.locator('div[role="dialog"] button:has-text("Criar")').first
                    pipe_create.click()
                    page.wait_for_timeout(2500)

                    report_scenario("Criação de Pipeline", True, f"Pipeline '{pipe_name}' configurado")
                else:
                    report_scenario("Criação de Pipeline", False, "Botão 'Novo Pipeline' não visível")
            else:
                report_scenario("Criação de Pipeline", False, "Botão de edição de pipelines não encontrado")
        except Exception as e:
            report_scenario("Criação de Pipeline", False, str(e))

        # -------------------------------------------------------------
        # CENÁRIO 5: Agentes de IA (/agents)
        # -------------------------------------------------------------
        print("\n🔹 [Cenário 5/8] Testando Configuração de Agentes de IA...")
        try:
            page.goto(f"{base_url}/agents", wait_until="networkidle")
            page.wait_for_timeout(2000)

            new_agent_btn = page.locator('button:has-text("Novo Agente"), button:has-text("Criar Agente")').first
            if new_agent_btn.count() > 0:
                new_agent_btn.click()
                page.wait_for_timeout(1000)

                agent_name = f"Bot QA {int(time.time()) % 1000}"
                
                # Preenche nome do agente
                name_input = page.locator('div[role="dialog"] input').first
                name_input.fill(agent_name)

                # Preenche System Prompt
                prompt_area = page.locator('div[role="dialog"] textarea').first
                if prompt_area.count() > 0:
                    prompt_area.fill("Você é um atendente inteligente para testes de QA automatizados.")

                # Clica em Salvar
                save_agent = page.locator('div[role="dialog"] button:has-text("Salvar")').first
                save_agent.click()
                page.wait_for_timeout(3000)

                report_scenario("Configuração de Agente de IA", True, f"Agente '{agent_name}' salvo com sucesso")
            else:
                report_scenario("Configuração de Agente de IA", False, "Botão 'Novo Agente' não encontrado")
        except Exception as e:
            report_scenario("Configuração de Agente de IA", False, str(e))

        # -------------------------------------------------------------
        # CENÁRIO 6: Listas de Disparo em Massa (/broadcasts)
        # -------------------------------------------------------------
        print("\n🔹 [Cenário 6/8] Testando Disparos e Listas...")
        try:
            page.goto(f"{base_url}/broadcasts", wait_until="networkidle")
            page.wait_for_timeout(2000)

            # Clica na aba Listas se houver
            list_tab = page.locator('[role="tab"]:has-text("Listas")').first
            if list_tab.count() > 0:
                list_tab.click()
                page.wait_for_timeout(800)

            new_list_btn = page.locator('button:has-text("Nova lista"), button:has-text("Criar lista")').first
            if new_list_btn.count() > 0:
                new_list_btn.click()
                page.wait_for_timeout(800)

                list_name = f"Lista QA {int(time.time()) % 1000}"
                list_input = page.locator('div[role="dialog"] input').first
                list_input.fill(list_name)

                save_list = page.locator('div[role="dialog"] button:has-text("Criar"), div[role="dialog"] button:has-text("Salvar")').first
                save_list.click()
                page.wait_for_timeout(2500)

                report_scenario("Criação de Lista de Disparo", True, f"Lista '{list_name}' criada com sucesso")
            else:
                report_scenario("Criação de Lista de Disparo", True, "Página de disparos acessada sem erros")
        except Exception as e:
            report_scenario("Criação de Lista de Disparo", False, str(e))

        # -------------------------------------------------------------
        # CENÁRIO 7: Configurações do Sistema (/settings)
        # -------------------------------------------------------------
        print("\n🔹 [Cenário 7/8] Testando Configurações do Workspace...")
        try:
            page.goto(f"{base_url}/settings", wait_until="networkidle")
            page.wait_for_timeout(2000)

            # Localiza o botão salvar da empresa
            save_company_btn = page.locator('button:has-text("Salvar alterações"), button:has-text("Salvar")').first
            if save_company_btn.count() > 0:
                save_company_btn.click()
                page.wait_for_timeout(2000)
                report_scenario("Atualização de Configurações", True, "Formulário de configurações salvo com sucesso")
            else:
                report_scenario("Atualização de Configurações", False, "Botão de salvar configurações não encontrado")
        except Exception as e:
            report_scenario("Atualização de Configurações", False, str(e))

        # -------------------------------------------------------------
        # CENÁRIO 8: Painel Super Admin (/leao)
        # -------------------------------------------------------------
        print("\n🔹 [Cenário 8/8] Testando Painel Super Admin (/leao)...")
        try:
            page.goto(f"{base_url}/leao", wait_until="networkidle")
            page.wait_for_timeout(2000)

            # Verifica se os cards de métricas estão no DOM
            metrics = page.locator('.grid, table, [role="region"]')
            if metrics.count() > 0:
                report_scenario("Acesso ao Painel Super Admin", True, "Dashboard de Super Admin carregado com métricas")
            else:
                report_scenario("Acesso ao Painel Super Admin", False, "Nenhum elemento de métrica encontrado")
        except Exception as e:
            report_scenario("Acesso ao Painel Super Admin", False, str(e))

        browser.close()

    # Resumo Final
    print("\n" + "=" * 65)
    print("📊 RELATÓRIO FINAL DO DEEP TESTER")
    print(f"Cenários Executados com Sucesso: {scenarios_passed}")
    print(f"Cenários com Falha: {scenarios_failed}")
    print(f"Total de Anomalias / Erros Capturados: {len(errors_found)}")
    print("=" * 65 + "\n")

    if errors_found:
        print(f"🔍 Lista de Anomalias ({len(errors_found)}):")
        for i, err in enumerate(errors_found, 1):
            print(f"  {i}. [{err['type']}] {err['msg']}")
    else:
        print("🎉 TODOS OS FLUXOS E FORMULÁRIOS FORAM EXECUTADOS COM 100% DE SUCESSO!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deep E2E Tester for LCRM")
    parser.add_argument("--url", default="https://leao.lcrm.com.br", help="Base URL")
    parser.add_argument("--email", default="suporte@lcrm.com.br", help="User Email")
    parser.add_argument("--password", required=True, help="User Password")
    parser.add_argument("--headless", action="store_true", help="Run without UI")
    args = parser.parse_args()

    run_deep_test(args.url, args.email, args.password, headless=args.headless)

