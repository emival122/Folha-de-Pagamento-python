import os
import locale
from tkinter import *
from tkinter import messagebox, ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle

# ================= CONFIGURAÇÕES =================
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    pass

COR_PRIMARIA = "#1A3366"
COR_SECUNDARIA = "#F4F7FA"
COR_TEXTO = "#2C3E50"
COR_ACENTO = "#27AE60"


def moeda(valor):
    # Formatação manual robusta para evitar conflitos de locale
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ================= CÁLCULOS =================


def calcular_inss(salario):
    # Tabelas 2024/2025 (Valores aproximados conforme sua lógica)
    faixas = [
        (1412.00, 0.075),
        (2666.68, 0.09),
        (4000.03, 0.12),
        (7786.02, 0.14)
    ]
    desconto = 0
    limite_anterior = 0

    if salario <= 0:
        return 0

    for limite, aliquota in faixas:
        if salario > limite:
            desconto += (limite - limite_anterior) * aliquota
            limite_anterior = limite
        else:
            desconto += (salario - limite_anterior) * aliquota
            return round(desconto, 2)
    return 908.85


def calcular_irrf(base):
    if base <= 2259.20:
        return 0
    elif base <= 2826.65:
        return (base * 0.075) - 169.44
    elif base <= 3751.05:
        return (base * 0.15) - 381.44
    elif base <= 4664.68:
        return (base * 0.225) - 662.77
    else:
        return (base * 0.275) - 896.00


def calcular_horas_extra(salario, horas):
    if salario <= 0 or horas <= 0:
        return 0
    return horas * ((salario / 220) * 1.5)

# ================= LÓGICA DE DADOS =================


def obter_dados():
    try:
        # Limpeza para aceitar diversos formatos de entrada numérica
        sal_limpo = e_salario.get().replace('R$', '').replace(
            '.', '').replace(',', '.').strip()
        horas_limpas = e_horas.get().replace(',', '.').strip()

        return {
            "nome": e_nome.get().strip(),
            "cpf": e_cpf.get().strip(),
            "cargo": e_cargo.get().strip(),
            "salario": float(sal_limpo or 0),
            "horas": float(horas_limpas or 0)
        }
    except ValueError:
        messagebox.showerror(
            "Erro de Valor", "Verifique o Salário e as Horas. Use apenas números.")
        return None


def atualizar_resumo():
    d = obter_dados()
    if not d:
        return

    h = calcular_horas_extra(d['salario'], d['horas'])
    inss = calcular_inss(d['salario'])
    # Base IRRF = Salário + Horas - INSS
    base_irrf = (d['salario'] + h) - inss
    irrf = max(0, calcular_irrf(base_irrf))
    total = (d['salario'] + h) - inss - irrf

    lbl_salario.config(text=moeda(d['salario']))
    lbl_horas.config(text=moeda(h))
    lbl_inss.config(text=f"- {moeda(inss)}", fg="#E74C3C")
    lbl_irrf.config(text=f"- {moeda(irrf)}", fg="#E74C3C")
    lbl_final.config(text=moeda(total), fg=COR_ACENTO)

# ================= GERAÇÃO DE PDF =================


def gerar_pdf():
    d = obter_dados()
    if not d:
        return

    if not d['nome'] or not d['cpf'] or not d['cargo']:
        messagebox.showwarning("Campos Obrigatórios",
                               "Atenção! Preencha NOME, CPF e CARGO para gerar o PDF.")
        return

    h = calcular_horas_extra(d['salario'], d['horas'])
    inss = calcular_inss(d['salario'])
    base_irrf = (d['salario'] + h) - inss
    irrf = max(0, calcular_irrf(base_irrf))
    total = (d['salario'] + h) - inss - irrf

    nome_arquivo = f"Holerite_{d['nome'].replace(' ', '_')}.pdf"
    c = canvas.Canvas(nome_arquivo, pagesize=letter)

    # Design do Cabeçalho
    c.setFillColor(COR_PRIMARIA)
    c.rect(0, 700, 612, 112, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, 750, "PRIME SYSTEMS - PAYROLL")
    c.setFont("Helvetica", 10)
    c.drawRightString(570, 755, "DEMONSTRATIVO DE PAGAMENTO")
    c.drawRightString(570, 740, "Janeiro / 2026")

    # Informações do Colaborador
    c.setFillColor(COR_TEXTO)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 670, f"COLABORADOR: {d['nome'].upper()}")
    c.setFont("Helvetica", 10)
    c.drawString(40, 655, f"CPF: {d['cpf']}  |  CARGO: {d['cargo']}")

    # Tabela de Lançamentos
    dados_tabela = [
        ['DESCRIÇÃO', 'REF', 'PROVENTOS', 'DESCONTOS'],
        ['Salário Base', '30d', moeda(d['salario']), ''],
        ['Horas Extras (50%)', f"{d['horas']}h", moeda(h), ''],
        ['INSS', '', '', moeda(inss)],
        ['IRRF', '', '', moeda(irrf)],
    ]

    t = Table(dados_tabela, colWidths=[2.5*inch, 0.8*inch, 1.2*inch, 1.2*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COR_PRIMARIA),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COR_SECUNDARIA])
    ]))
    t.wrapOn(c, 40, 500)
    t.drawOn(c, 40, 500)

    # Totalizador
    c.setFillColor(COR_PRIMARIA)
    c.rect(343, 440, 228, 35, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(355, 452, "VALOR LÍQUIDO:")
    c.drawRightString(560, 452, moeda(total))

    c.save()
    messagebox.showinfo("Sucesso", f"O PDF '{nome_arquivo}' foi gerado!")

# ================= INTERFACE GRÁFICA =================


root = Tk()
root.title("PrimeSystems - Folha de Pagamento")
root.geometry("1100x750")
root.configure(bg=COR_SECUNDARIA)

# Header
header = Frame(root, bg=COR_PRIMARIA, height=100)
header.pack(fill="x")
Label(header, text="WageCore System", bg=COR_PRIMARIA,
      fg="white", font=("Helvetica", 27, "bold")).pack(pady=30)

# Layout Principal
main = Frame(root, bg=COR_SECUNDARIA)
main.pack(fill="both", expand=True, padx=40, pady=30)
main.columnconfigure(0, weight=3)
main.columnconfigure(1, weight=1)

# Seção de Cadastro
f_inputs = LabelFrame(main, text=" Cadastro do Colaborador ", bg=COR_SECUNDARIA, font=(
    "Helvetica", 14, "bold"), padx=30, pady=30)
f_inputs.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

labels = ["Nome:", "CPF:", "Cargo:", "Salário Bruto:", "Horas Extras:"]
entries = []

for i, text_label in enumerate(labels):
    Label(f_inputs, text=text_label, bg=COR_SECUNDARIA, font=(
        "Helvetica", 12)).grid(row=i, column=0, sticky="w", pady=12)
    e = Entry(f_inputs, font=("Helvetica", 14))
    e.grid(row=i, column=1, pady=12, sticky="ew")
    entries.append(e)

f_inputs.columnconfigure(1, weight=1)
e_nome, e_cpf, e_cargo, e_salario, e_horas = entries

# Seção de Resumo Lateral
f_resumo = LabelFrame(main, text=" Resumo ", bg="white",
                      font=("Helvetica", 14, "bold"), padx=30, pady=30)
f_resumo.grid(row=0, column=1, sticky="nsew")

lbl_salario = Label(f_resumo, text="R$ 0,00",
                    bg="white", font=("Helvetica", 13))
lbl_horas = Label(f_resumo, text="R$ 0,00", bg="white", font=("Helvetica", 13))
lbl_inss = Label(f_resumo, text="R$ 0,00", bg="white", font=("Helvetica", 13))
lbl_irrf = Label(f_resumo, text="R$ 0,00", bg="white", font=("Helvetica", 13))
lbl_final = Label(f_resumo, text="R$ 0,00", bg="white",
                  font=("Helvetica", 22, "bold"), fg=COR_ACENTO)

res = [("Bruto:", lbl_salario), ("Extras:", lbl_horas),
       ("INSS:", lbl_inss), ("IRRF:", lbl_irrf)]

for i, (txt, lbl) in enumerate(res):
    Label(f_resumo, text=txt, bg="white", font=("Helvetica", 12)).grid(
        row=i, column=0, sticky="w", pady=10)
    lbl.grid(row=i, column=1, sticky="e")

ttk.Separator(f_resumo, orient="horizontal").grid(
    row=4, column=0, columnspan=2, sticky="ew", pady=20)
Label(f_resumo, text="LÍQUIDO:", bg="white", font=(
    "Helvetica", 14, "bold")).grid(row=5, column=0, sticky="w")
lbl_final.grid(row=5, column=1, sticky="e")

# Botões de Ação
f_btns = Frame(root, bg=COR_SECUNDARIA)
f_btns.pack(pady=30)

Button(f_btns, text="CALCULAR", command=atualizar_resumo, bg=COR_ACENTO, fg="white", font=(
    "Helvetica", 12, "bold"), width=25, height=2, cursor="hand2").pack(side="left", padx=20)
Button(f_btns, text="GERAR PDF", command=gerar_pdf, bg=COR_PRIMARIA, fg="white", font=(
    "Helvetica", 12, "bold"), width=25, height=2, cursor="hand2").pack(side="left", padx=20)

root.mainloop()
