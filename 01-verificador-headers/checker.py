"""Analisa cabeçalhos HTTP fornecidos em JSON, sem fazer conexões de rede."""

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any


RECOMMENDED_HEADERS = {
    "content-security-policy": "Restringe as origens de conteúdo que o navegador pode carregar.",
    "strict-transport-security": "Instrui o navegador a usar HTTPS em conexões futuras.",
    "x-content-type-options": "Ajuda a impedir a interpretação incorreta do tipo de conteúdo.",
    "x-frame-options": "Controla se a página pode ser carregada em frames.",
    "referrer-policy": "Controla quais informações de referência são compartilhadas.",
    "permissions-policy": "Controla o acesso da página a recursos do navegador.",
}

HEADER_LABELS = {
    "content-security-policy": "Content-Security-Policy",
    "strict-transport-security": "Strict-Transport-Security",
    "x-content-type-options": "X-Content-Type-Options",
    "x-frame-options": "X-Frame-Options",
    "referrer-policy": "Referrer-Policy",
    "permissions-policy": "Permissions-Policy",
}


def analyze_headers(response: dict[str, Any]) -> dict[str, list[str]]:
    """Compara cabeçalhos fornecidos com uma lista básica de recomendações."""
    headers = response.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("O campo 'headers' deve ser um objeto JSON de cabeçalhos.")

    normalized_headers = {
        name.strip().casefold()
        for name in headers
        if isinstance(name, str)
    }

    return {
        "present": sorted(
            name for name in RECOMMENDED_HEADERS if name in normalized_headers
        ),
        "missing": sorted(
            name for name in RECOMMENDED_HEADERS if name not in normalized_headers
        ),
    }


def load_response(path: Path) -> dict[str, Any]:
    """Carrega uma resposta HTTP simulada de um arquivo JSON local."""
    try:
        with path.open(encoding="utf-8") as response_file:
            response = json.load(response_file)
    except OSError as error:
        raise ValueError(f"Não foi possível ler o arquivo: {error}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"JSON inválido: {error}") from error

    if not isinstance(response, dict):
        raise ValueError("A raiz do arquivo JSON deve ser um objeto.")
    return response


def create_html_report(result: dict[str, list[str]]) -> str:
    """Cria um relatório HTML estático para abrir localmente no navegador."""
    present_headers = set(result["present"])
    rows = []

    for header, description in sorted(RECOMMENDED_HEADERS.items()):
        is_present = header in present_headers
        status = "Presente" if is_present else "Ausente"
        status_class = "present" if is_present else "missing"
        rows.append(
            "<tr>"
            f"<th scope=\"row\">{html.escape(HEADER_LABELS.get(header, header))}</th>"
            f"<td><span class=\"badge {status_class}\">{status}</span></td>"
            f"<td>{html.escape(description)}</td>"
            "</tr>"
        )

    summary = (
        f"{len(result['present'])} de {len(RECOMMENDED_HEADERS)} cabeçalhos "
        "recomendados encontrados"
    )
    return f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Relatório de cabeçalhos HTTP</title>
  <style>
    :root {{ color-scheme: light; font-family: system-ui, sans-serif; color: #24202a; background: #f5f2f7; }}
    body {{ max-width: 900px; margin: 0 auto; padding: 32px 16px; }}
    h1 {{ margin-bottom: 8px; }}
    .summary {{ color: #544c5f; }}
    .notice {{ padding: 12px 16px; background: #fff; border-left: 4px solid #7353ba; border-radius: 6px; }}
    .table-wrap {{ overflow-x: auto; margin-top: 24px; background: #fff; border-radius: 12px; box-shadow: 0 4px 16px #24202a14; }}
    table {{ width: 100%; border-collapse: collapse; text-align: left; }}
    th, td {{ padding: 14px 16px; border-bottom: 1px solid #e8e4ed; vertical-align: top; }}
    thead th {{ background: #f0edf5; }}
    tbody th {{ font-family: ui-monospace, monospace; font-size: 13px; }}
    .badge {{ display: inline-block; padding: 4px 9px; border-radius: 999px; font-size: 13px; font-weight: 650; }}
    .present {{ color: #17613a; background: #dcf4e5; }}
    .missing {{ color: #873334; background: #fde4e2; }}
    footer {{ margin-top: 20px; color: #625c69; font-size: 14px; }}
    @media (max-width: 600px) {{ th, td {{ padding: 10px 8px; }} }}
  </style>
</head>
<body>
  <main>
    <h1>Verificação de cabeçalhos HTTP</h1>
    <p class="summary">{summary}</p>
    <p class="notice">Relatório gerado a partir de dados simulados locais. Nenhum site foi acessado.</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th scope="col">Cabeçalho</th><th scope="col">Resultado</th><th scope="col">Descrição</th></tr></thead>
        <tbody>{"".join(rows)}</tbody>
      </table>
    </div>
  </main>
  <footer>
    <p>Este relatório é educativo; a presença de um cabeçalho não garante, por si só, a segurança do sistema.</p>
    <p>Criado por Douglas Honório.</p>
  </footer>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analisa cabeçalhos de uma resposta HTTP simulada em JSON local."
    )
    parser.add_argument("arquivo", type=Path, help="caminho do arquivo JSON de teste")
    parser.add_argument(
        "--html",
        type=Path,
        metavar="RELATORIO",
        help="salva um relatório visual HTML para abrir no navegador",
    )
    args = parser.parse_args()

    try:
        result = analyze_headers(load_response(args.arquivo))
        if args.html:
            args.html.write_text(
                create_html_report(result),
                encoding="utf-8",
            )
    except ValueError as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"Erro ao salvar o relatório: {error}", file=sys.stderr)
        return 2

    print("Cabeçalhos presentes:")
    if result["present"]:
        for header in result["present"]:
            print(f"  OK  {header}")
    else:
        print("  Nenhum dos cabeçalhos recomendados foi encontrado.")

    print("\nCabeçalhos ausentes:")
    if result["missing"]:
        for header in result["missing"]:
            print(f"  --  {header}: {RECOMMENDED_HEADERS[header]}")
    else:
        print("  Nenhum.")

    if args.html:
        print(f"\nRelatório HTML salvo em: {args.html.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
