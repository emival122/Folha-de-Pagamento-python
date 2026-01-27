def calcular_inss(salario_bruto):
    if salario_bruto <= 1212.00:
        return salario_bruto * 0.075
    elif salario_bruto <= 2427.35:
        return salario_bruto * 0.09
    elif salario_bruto <= 3641.03:
        return salario_bruto * 0.12
    elif salario_bruto <= 7087.22:
        return salario_bruto * 0.14
    else:
        return 751.99


def calcular_irrf(salario_liquido):
    if salario_liquido <= 1903.98:
        return 0
    elif salario_liquido <= 2826.65:
        return (salario_liquido * 0.075) - 142.80
    elif salario_liquido <= 3751.05:
        return (salario_liquido * 0.15) - 354.80
    elif salario_liquido <= 4664.68:
        return (salario_liquido * 0.225) - 636.13
    else:
        return (salario_liquido * 0.275) - 869.36


def calcular_horas_extra(salario_bruto, horas_extras_trabalhadas):
    valor_hora = salario_bruto / 220
    adicional_hora_extra = valor_hora * 0.5
    return horas_extras_trabalhadas * (valor_hora + adicional_hora_extra)


salario_bruto = float(input("Digite seu salário bruto do trabalhador: R$ "))
horas_extras_trabalhadas = int(
    input("Digite o número de horas extras trabalhadas no mês: "))

desconto_inss = calcular_inss(salario_bruto)
salario_liquido = salario_bruto - desconto_inss

desconto_irrf = calcular_irrf(salario_liquido)
provento_horas_extras = calcular_horas_extra(
    salario_bruto, horas_extras_trabalhadas)

salario_final = salario_liquido - desconto_irrf + provento_horas_extras

print("\n*** Folha de Pagamento ***")
print(f"Salário Bruto: R$ {salario_bruto:.2f}")
print(f"Proventos por horas extras: R$ {provento_horas_extras:.2f}")
print(f"Desconto INSS: R$ {desconto_inss:.2f}")
print(f"Desconto IRRF: R$ {desconto_irrf:.2f}")
print("-------------------------------")
print(f"Salário Final: R$ {salario_final:.2f}")
