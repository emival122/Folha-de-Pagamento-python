# 🏦 Payroll Pro – Sistema de Folha de Pagamento

![GitHub License](https://img.shields.io/github/license/emival122/folha-pagamento?style=flat-square&color=1A3366)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python)
![Repo Size](https://img.shields.io/github/repo-size/emival122/folha-pagamento?style=flat-square)

<p align="center">
  <img src="./assets/screenshot_sistema.png" alt="Interface do Sistema" width="800px">
</p>

<p align="center">
  <img src="./assets/Holerite.png" alt="holerite Gerado" width="600px">
</p>

---
---

---

## 📌 Sobre o Projeto
O **Payroll Pro** é uma solução desktop para automação de cálculos trabalhistas e emissão de demonstrativos de pagamento. 
Desenvolvido com foco em **precisão fiscal**, o sistema realiza cálculos complexos de impostos (INSS/IRRF) conforme a legislação vigente (referência 2026), oferecendo uma interface intuitiva e geração de documentos profissionais em PDF.

---

## ✨ Funcionalidades
- 🧮 **Cálculo Tributário:** Automação total de descontos progressivos de INSS e IRRF.
- ⏱️ **Gestão de Horas Extras:** Cálculo preciso com adicional de 50%.
- 📄 **Emissão de Holerites:** Geração de relatórios profissionais em PDF com tabelas e identidade visual.
- 💰 **Resumo em Tempo Real:** Visualização instantânea dos valores bruto e líquido.
- 🛡️ **Segurança de Dados:** Validação de entradas numéricas e tratamento de erros de câmbio monetário.

---

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.10+
- **Interface Gráfica:** Tkinter
- **Geração de Documentos:** ReportLab
- **Internacionalização:** Módulo `locale` (Moeda R$)
- **Documentação:** Markdown

---

## 📘 Documentação
Consulte nossos manuais detalhados para entender as regras de cálculo e operação:

* [📄 **Documentação Técnica**](./docs/tecnico.md): Detalhamento das alíquotas, lógica de impostos e estrutura de arquivos.
* [👤 **Manual do Usuário**](./docs/manual_usuario.md): Guia de preenchimento, cálculo e exportação de PDFs.

---

## 🚀 Melhorias Futuras
- [ ] 📊 **Dashboards:** Gráficos de custos anuais por colaborador.
- [ ] 📧 **Envio Automático:** Enviar holerites diretamente por e-mail.
- [ ] 🗄️ **Banco de Dados:** Integração com SQLite para histórico de pagamentos.
- [ ] 📅 **13º e Férias:** Módulo para cálculo de benefícios sazonais.

---

## 📄 Licença
Este projeto está sob a **Licença MIT**. Sinta-se à vontade para utilizar para fins educacionais ou profissionais.

---

## ⚙️ Instalação e Execução

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/emival122/folha-pagamento.git](https://github.com/emival122/folha-pagamento.git)
