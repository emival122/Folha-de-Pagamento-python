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
    locale.setlocale(locale.LC_ALL, '')

COR_PRIMARIA = "#1A3366"
COR_SECUNDARIA = "#F4F7FA"
COR_TEXTO = "#2C3E50"
COR_ACENTO = "#27AE60"

# ================= CÁLCULOS =================


def calcular_inss(salario):
    return salario * 0.08


def calcular_irrf(base):
    return base * 0.075


def calcular_horas_extra(salario, horas):
    return horas * ((salario / 220) * 1.5)

# ================= LÓGICA =================


def obter_dados():
    try:
        return {
            "nome": e_nome.get(),
            "cpf": e_cpf.get(),
            "cargo": e_cargo.get(),
            "salario": float(e_salario.get().replace(',', '.') or 0),
            "horas": int(e_horas.get() or 0)
        }
    except ValueError:
        messagebox.showerror("Erro", "Use apenas números.")
        return None


def atualizar_resumo():
    d = obter_dados()
    if not d:
        return

    h = calcular_horas_extra(d['salario'], d['horas'])
    inss = calcular_inss(d['salario'])
    irrf = calcular_irrf(d['salario'] - inss)
    total = d['salario'] + h - inss - irrf

    lbl_salario.config(text=locale.currency(d['salario'], grouping=True))
    lbl_horas.config(text=locale.currency(h, grouping=True))
    lbl_inss.config(
        text=f"- {locale.currency(inss, grouping=True)}", fg="#E74C3C")
    lbl_irrf.config(
        text=f"- {locale.currency(irrf, grouping=True)}", fg="#E74C3C")
    lbl_final.config(text=locale.currency(total, grouping=True), fg=COR_ACENTO)

# ================= PDF =================


def gerar_pdf():
    d = obter_dados()
    if not d or not d['nome'] or not d['cpf']:
        messagebox.showwarning("Atenção", "Preencha Nome e CPF.")
        return

    inss = calcular_inss(d['salario'])
    h = calcular_horas_extra(d['salario'], d['horas'])
    irrf = calcular_irrf(d['salario'] - inss)
    total = d['salario'] + h - inss - irrf

    c = canvas.Canvas(f"Holerite_{d['nome'].split()[0]}.pdf", pagesize=letter)

    # ===== HEADER =====
    c.setFillColor(COR_PRIMARIA)
    c.rect(0, 700, 612, 112, fill=1, stroke=0)

    # LOGO NO CANTO SUPERIOR ESQUERDO
    logo = "logo_header.png"
    if os.path.exists(logo):
        c.drawImage(
            logo,
            40,      # X esquerdo
            735,     # Y topo
            width=150,
            height=55,
            mask="auto"
        )

    # TÍTULO À DIREITA
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(570, 755, "DEMONSTRATIVO DE PAGAMENTO")
    c.setFont("Helvetica", 10)
    c.drawRightString(570, 740, "Janeiro / 2026")

    # ===== DADOS =====
    c.setFillColor(COR_TEXTO)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 670, f"COLABORADOR: {d['nome'].upper()}")
    c.setFont("Helvetica", 10)
    c.drawString(40, 655, f"CPF: {d['cpf']}  |  CARGO: {d['cargo']}")

    # ===== TABELA =====
    dados_tabela = [
        ['DESCRIÇÃO', 'REF', 'PROVENTOS', 'DESCONTOS'],
        ['Salário Base', '30d', f"{d['salario']:,.2f}", ''],
        ['Horas Extras (50%)', f"{d['horas']}h", f"{h:,.2f}", ''],
        ['INSS', '8%', '', f"{inss:,.2f}"],
        ['IRRF', '7.5%', '', f"{irrf:,.2f}"],
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

    # ===== TOTAL =====
    c.setFillColor(COR_PRIMARIA)
    c.rect(343, 440, 228, 35, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(355, 452, "VALOR LÍQUIDO:")
    c.drawRightString(560, 452, f"R$ {total:,.2f}")

    c.save()
    messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")

# ================= INTERFACE =================


root = Tk()
root.title("PrimeSystems - Folha de Pagamento")
root.geometry("1100x750")
root.configure(bg=COR_SECUNDARIA)
root.resizable(True, True)

header = Frame(root, bg=COR_PRIMARIA, height=100)
header.pack(fill="x")
Label(header, text="SISTEMA DE FOLHA DE PAGAMENTO",
      bg=COR_PRIMARIA, fg="white",
      font=("Helvetica", 22, "bold")).pack(pady=30)

main = Frame(root, bg=COR_SECUNDARIA)
main.pack(fill="both", expand=True, padx=40, pady=30)
main.columnconfigure(0, weight=3)
main.columnconfigure(1, weight=1)

# Inputs
f_inputs = LabelFrame(main, text=" Cadastro do Colaborador ",
                      bg=COR_SECUNDARIA, font=("Helvetica", 14, "bold"),
                      padx=30, pady=30)
f_inputs.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

labels = ["Nome:", "CPF:", "Cargo:", "Salário Base:", "Horas Extras:"]
entries = []

for i, t in enumerate(labels):
    Label(f_inputs, text=t, bg=COR_SECUNDARIA,
          font=("Helvetica", 12)).grid(row=i, column=0, sticky="w", pady=12)
    e = Entry(f_inputs, font=("Helvetica", 14))
    e.grid(row=i, column=1, pady=12, sticky="ew")
    entries.append(e)

f_inputs.columnconfigure(1, weight=1)
e_nome, e_cpf, e_cargo, e_salario, e_horas = entries

# Resumo
f_resumo = LabelFrame(main, text=" Resumo ",
                      bg="white", font=("Helvetica", 14, "bold"),
                      padx=30, pady=30)
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
    Label(f_resumo, text=txt, bg="white",
          font=("Helvetica", 12)).grid(row=i, column=0, sticky="w", pady=10)
    lbl.grid(row=i, column=1, sticky="e")

ttk.Separator(f_resumo, orient="horizontal").grid(
    row=4, column=0, columnspan=2, sticky="ew", pady=20)

Label(f_resumo, text="LÍQUIDO:", bg="white",
      font=("Helvetica", 14, "bold")).grid(row=5, column=0, sticky="w")
lbl_final.grid(row=5, column=1, sticky="e")

# Botões
f_btns = Frame(root, bg=COR_SECUNDARIA)
f_btns.pack(pady=30)

Button(f_btns, text="CALCULAR", command=atualizar_resumo,
       bg=COR_ACENTO, fg="white",
       font=("Helvetica", 12, "bold"),
       width=25, height=2).pack(side="left", padx=20)

Button(f_btns, text="GERAR PDF", command=gerar_pdf,
       bg=COR_PRIMARIA, fg="white",
       font=("Helvetica", 12, "bold"),
       width=25, height=2).pack(side="left", padx=20)

root.mainloop()
