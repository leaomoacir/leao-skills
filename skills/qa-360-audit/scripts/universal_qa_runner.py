#!/usr/bin/env python3
"""
Template Universal de Testes 360° — Playwright
Compatível com qualquer aplicação web ou API.
"""

import sys
import time
import argparse
from playwright.sync_api import sync_playwright

class UniversalQASuite:
    def __init__(self, base_url: str, headless: bool = True, slow_mo: int = 0):
        self.base_url = base_url.rstrip("/")
        self.headless = headless
        self.slow_mo = slow_mo
        self.console_errors = []
        self.network_errors = []
        self.results = []

    def setup_listeners(self, page):
        """Intercepta exceções no console e status de erro na rede (4xx/5xx)."""
        page.on("console", lambda msg: self.console_errors.append(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)
        page.on("response", lambda res: self.network_errors.append(f"{res.status} {res.url}") if res.status >= 400 else None)

    def run_scenario(self, name: str, test_fn):
        """Executa um cenário cronometrado."""
        print(f"\n🔹 Executando: {name}...")
        start = time.time()
        status = "FAIL"
        error_msg = ""
        try:
            test_fn()
            status = "PASS"
            print(f"  ✅ [PASS] {name} ({time.time() - start:.2f}s)")
        except Exception as e:
            error_msg = str(e)
            print(f"  ❌ [FAIL] {name}: {error_msg}")
        finally:
            self.results.append({
                "name": name,
                "status": status,
                "duration": time.time() - start,
                "error": error_msg
            })

    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless, slow_mo=self.slow_mo)
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()
            self.setup_listeners(page)

            # Cenário 1: Handshake de rota
            self.run_scenario("Handshake Inicial da Aplicação", lambda: page.goto(self.base_url))

            browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runner Universal de Testes 360°")
    parser.add_argument("--url", default="http://localhost:3000", help="URL base da aplicação sob teste")
    parser.add_argument("--headless", action="store_true", help="Execução silenciosa (CI/CD)")
    parser.add_argument("--slow-mo", type=int, default=0, help="Atraso em ms para inspeção visual")
    args = parser.parse_args()

    suite = UniversalQASuite(args.url, args.headless, args.slow_mo)
    suite.run()
