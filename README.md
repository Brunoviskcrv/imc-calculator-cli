# 🏋️ Calculadora de IMC CLI

Calculadora de Índice de Massa Corporal (IMC) com interface de linha de comando, saída colorida e histórico persistido em CSV.

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

### Calcular IMC
```bash
python main.py --peso 70 --altura 1.75
python main.py --peso 55.5 --altura 1.60
```

### Ver histórico
```bash
python main.py --historico
```

### Limpar histórico
```bash
python main.py --limpar
```

### Demo (sem argumentos)
```bash
python main.py
```

## Classificações OMS

| IMC          | Classificação              |
|--------------|----------------------------|
| < 18.5       | Abaixo do peso             |
| 18.5 – 24.9  | Peso normal                |
| 25.0 – 29.9  | Sobrepeso                  |
| 30.0 – 34.9  | Obesidade Grau I           |
| 35.0 – 39.9  | Obesidade Grau II          |
| ≥ 40.0       | Obesidade Grau III (Mórbida) |

## Histórico

Os registros são salvos em `historico_imc.csv` com as colunas:
`data, hora, peso_kg, altura_m, imc, classificacao`
