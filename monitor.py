"""Monitor de sites: verifica se estao no ar e salva um relatorio em CSV."""
import csv
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

TIMEOUT = 5  # segundos de espera por site


def ler_sites(caminho):
    """Le a lista de sites, ignorando linhas vazias e comentarios (#)."""
    with open(caminho, encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo]
    return [l for l in linhas if l and not l.startswith("#")]


def esta_no_ar(status):
    """Considera 'no ar' qualquer status HTTP de 200 a 399."""
    return status is not None and 200 <= status < 400


def checar_site(url):
    """Acessa o site e devolve status, tempo de resposta e se esta no ar."""
    inicio = time.time()
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as resposta:
            status = resposta.status
    except urllib.error.HTTPError as erro:
        status = erro.code  # o site respondeu, mas com erro (404, 500...)
    except Exception:
        status = None  # sem resposta (DNS, timeout, conexao recusada)
    tempo_ms = round((time.time() - inicio) * 1000)
    return {
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "url": url,
        "status": status if status is not None else "SEM RESPOSTA",
        "tempo_ms": tempo_ms,
        "no_ar": "SIM" if esta_no_ar(status) else "NAO",
    }


def salvar_relatorio(resultados, caminho="relatorio.csv"):
    """Adiciona os resultados ao final do CSV (cria o arquivo se nao existir)."""
    campos = ["data_hora", "url", "status", "tempo_ms", "no_ar"]
    try:
        novo = open(caminho).read(1) == ""
    except FileNotFoundError:
        novo = True
    with open(caminho, "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        if novo:
            escritor.writeheader()
        escritor.writerows(resultados)


def main():
    sites = ler_sites("sites.txt")
    resultados = []
    for url in sites:
        r = checar_site(url)
        resultados.append(r)
        print(f"[{r['no_ar']}] {r['url']} - status {r['status']} - {r['tempo_ms']} ms")
    salvar_relatorio(resultados)
    fora = [r for r in resultados if r["no_ar"] == "NAO"]
    if fora:
        print(f"\nATENCAO: {len(fora)} site(s) fora do ar.")
        sys.exit(1)  # codigo 1 = falha (util para automacao)
    print("\nTodos os sites estao no ar.")


if __name__ == "__main__":
    main()
