#!/usr/bin/env python3
"""
Calculadora de IMC com CLI
Uso: python main.py --peso 70 --altura 1.75
     python main.py --historico
"""

import argparse
import csv
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    # Fallback: sem cores
    class _Dummy:
        def __getattr__(self, name):
            return ""
    Fore = _Dummy()
    Style = _Dummy()

# ── Configurações ────────────────────────────────────────────────────────────
HISTORICO_CSV = Path("historico_imc.csv")
CABECALHO_CSV = ["data", "hora", "peso_kg", "altura_m", "imc", "classificacao"]

# ── Classificações OMS (6 faixas) ────────────────────────────────────────────
FAIXAS = [
    (0.0,  18.5, "Abaixo do peso",      Fore.CYAN),
    (18.5, 25.0, "Peso normal",          Fore.GREEN),
    (25.0, 30.0, "Sobrepeso",            Fore.YELLOW),
    (30.0, 35.0, "Obesidade Grau I",     Fore.RED),
    (35.0, 40.0, "Obesidade Grau II",    Fore.RED),
    (40.0, float("inf"), "Obesidade Grau III (Mórbida)", Fore.RED),
]


def calcular_imc(peso: float, altura: float) -> float:
    """Calcula o IMC dado peso (kg) e altura (m)."""
    if altura <= 0:
        raise ValueError("Altura deve ser maior que zero.")
    return peso / (altura ** 2)


def classificar_imc(imc: float) -> tuple:
    """Retorna (classificação, cor) para o valor de IMC."""
    for minimo, maximo, classificacao, cor in FAIXAS:
        if minimo <= imc < maximo:
            return classificacao, cor
    return "Valor inválido", Fore.WHITE


def salvar_historico(peso: float, altura: float, imc: float, classificacao: str):
    """Salva o registro no CSV de histórico."""
    agora = datetime.now()
    nova_linha = {
        "data": agora.strftime("%Y-%m-%d"),
        "hora": agora.strftime("%H:%M:%S"),
        "peso_kg": f"{peso:.2f}",
        "altura_m": f"{altura:.2f}",
        "imc": f"{imc:.2f}",
        "classificacao": classificacao,
    }

    arquivo_existe = HISTORICO_CSV.exists()
    with open(HISTORICO_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CABECALHO_CSV)
        if not arquivo_existe:
            writer.writeheader()
        writer.writerow(nova_linha)


def exibir_historico():
    """Lê e exibe o histórico salvo em CSV."""
    if not HISTORICO_CSV.exists():
        print(f"{Fore.YELLOW}Nenhum histórico encontrado.{Style.RESET_ALL}")
        return

    with open(HISTORICO_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        registros = list(reader)

    if not registros:
        print(f"{Fore.YELLOW}Histórico vazio.{Style.RESET_ALL}")
        return

    print(f"\n{Style.BRIGHT}{'─'*65}")
    print(f" {'HISTÓRICO DE IMC':^63} ")
    print(f"{'─'*65}{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}{'Data':<12} {'Hora':<10} {'Peso':>7} {'Altura':>8} {'IMC':>7}  {'Classificação':<30}{Style.RESET_ALL}")
    print(f"{'─'*65}")

    for r in registros:
        imc_val = float(r["imc"])
        _, cor = classificar_imc(imc_val)
        print(
            f"{r['data']:<12} {r['hora']:<10} "
            f"{float(r['peso_kg']):>6.1f}kg "
            f"{float(r['altura_m']):>6.2f}m "
            f"{imc_val:>6.2f}  "
            f"{cor}{r['classificacao']:<30}{Style.RESET_ALL}"
        )

    print(f"{'─'*65}")
    print(f"  Total de registros: {Style.BRIGHT}{len(registros)}{Style.RESET_ALL}\n")


def exibir_resultado(peso: float, altura: float, imc: float, classificacao: str, cor: str):
    """Exibe o resultado formatado no terminal."""
    print(f"\n{Style.BRIGHT}{'═'*45}")
    print(f"  CALCULADORA DE IMC")
    print(f"{'═'*45}{Style.RESET_ALL}")
    print(f"  Peso   : {Style.BRIGHT}{peso:.2f} kg{Style.RESET_ALL}")
    print(f"  Altura : {Style.BRIGHT}{altura:.2f} m{Style.RESET_ALL}")
    print(f"  {'─'*41}")
    print(f"  IMC    : {Style.BRIGHT}{cor}{imc:.2f}{Style.RESET_ALL}")
    print(f"  Status : {Style.BRIGHT}{cor}{classificacao}{Style.RESET_ALL}")
    print()

    # Barra visual
    _exibir_barra(imc)
    print(f"{'═'*45}\n")


def _exibir_barra(imc: float):
    """Exibe uma barra visual indicando a posição do IMC."""
    limites = [16, 18.5, 25, 30, 35, 40, 45]
    labels  = ["<16", "18.5", "25", "30", "35", "40", "45+"]
    cores   = [Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.RED, Fore.RED]
    largura = 6  # caracteres por segmento

    print(f"  {'─'*41}")
    print(f"  Escala OMS:", end="")

    barra = ""
    posicao_marcada = False
    for i, (minimo, cor) in enumerate(zip(limites[:-1], cores)):
        maximo = limites[i + 1]
        segmento = "▓" * largura
        if minimo <= imc < maximo and not posicao_marcada:
            segmento = ("▓" * (largura // 2 - 1)) + "◆" + ("▓" * (largura // 2))
            posicao_marcada = True
        barra += cor + segmento
    if not posicao_marcada:  # imc >= 40
        barra = barra[:-largura] + Fore.RED + ("▓" * (largura - 1)) + "◆"

    print(f"\n  {barra}{Style.RESET_ALL}")
    escala_str = "".join(f"{l:<{largura}}" for l in labels)
    print(f"  {escala_str}")


def demo_mode():
    """Executa uma demonstração sem argumentos."""
    print(f"{Style.BRIGHT}Demo: calculando IMC para peso=70kg, altura=1.75m{Style.RESET_ALL}")
    peso, altura = 70.0, 1.75
    imc = calcular_imc(peso, altura)
    classificacao, cor = classificar_imc(imc)
    exibir_resultado(peso, altura, imc, classificacao, cor)
    salvar_historico(peso, altura, imc, classificacao)
    print(f"{Fore.GREEN}Histórico salvo em: {HISTORICO_CSV}{Style.RESET_ALL}")
    print(f"\nUso real: python main.py --peso 70 --altura 1.75")
    print(f"Histórico: python main.py --historico")


def parse_args():
    parser = argparse.ArgumentParser(
        prog="imc",
        description="Calculadora de IMC com histórico em CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exemplos:\n"
            "  python main.py --peso 70 --altura 1.75\n"
            "  python main.py --peso 55.5 --altura 1.60\n"
            "  python main.py --historico\n"
            "  python main.py --historico --limpar\n"
        ),
    )
    parser.add_argument("--peso",    type=float, help="Peso em quilogramas (ex: 70.5)")
    parser.add_argument("--altura",  type=float, help="Altura em metros (ex: 1.75)")
    parser.add_argument("--historico", action="store_true", help="Exibe o histórico de medições")
    parser.add_argument("--limpar",    action="store_true", help="Remove o arquivo de histórico")
    return parser


def main():
    parser = parse_args()
    args = parser.parse_args()

    # Modo demo (sem argumentos)
    if len(sys.argv) == 1:
        demo_mode()
        sys.exit(0)

    # Limpar histórico
    if args.limpar:
        if HISTORICO_CSV.exists():
            HISTORICO_CSV.unlink()
            print(f"{Fore.GREEN}Histórico removido com sucesso.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Nenhum histórico para remover.{Style.RESET_ALL}")
        if not args.historico:
            sys.exit(0)

    # Exibir histórico
    if args.historico:
        exibir_historico()
        sys.exit(0)

    # Cálculo de IMC
    if args.peso is None or args.altura is None:
        print(f"{Fore.RED}Erro: --peso e --altura são obrigatórios para calcular o IMC.{Style.RESET_ALL}")
        parser.print_help()
        sys.exit(1)

    if args.peso <= 0:
        print(f"{Fore.RED}Erro: Peso deve ser maior que zero.{Style.RESET_ALL}")
        sys.exit(1)

    if args.altura <= 0 or args.altura > 3.0:
        print(f"{Fore.RED}Erro: Altura deve estar entre 0 e 3.0 metros.{Style.RESET_ALL}")
        sys.exit(1)

    if args.peso > 500:
        print(f"{Fore.RED}Erro: Peso parece inválido (máximo aceito: 500 kg).{Style.RESET_ALL}")
        sys.exit(1)

    try:
        imc = calcular_imc(args.peso, args.altura)
        classificacao, cor = classificar_imc(imc)
        exibir_resultado(args.peso, args.altura, imc, classificacao, cor)
        salvar_historico(args.peso, args.altura, imc, classificacao)
        print(f"{Fore.GREEN}✔ Registro salvo em: {HISTORICO_CSV}{Style.RESET_ALL}")
    except ValueError as e:
        print(f"{Fore.RED}Erro: {e}{Style.RESET_ALL}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
