import tkinter as tk
import calculos as cl
from tkinter import ttk
import sqlite3

# --- CONFIGURAÇÃO DO BANCO DE DADOS (SQLite3) ---
def inicializar_banco():
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE
        )
    """)
    conexao.commit()
    conexao.close()

# Inicializa o banco antes de renderizar a tela
inicializar_banco()


# --- FUNÇÕES (Lógica mantida, adicionada a função de cadastro) ---

def run_cadastro():
    nome_val = nome_entry.get().strip()
    cpf_val = cpf_entry.get().strip()
    
    if not nome_val or not cpf_val:
        mostrar_cadastro.config(text="Preencha todos os campos!", foreground="red")
        return

    try:
        conexao = sqlite3.connect("sistema.db")
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO pessoas (nome, cpf) VALUES (?, ?)", (nome_val, cpf_val))
        conexao.commit()
        conexao.close()
        
        mostrar_cadastro.config(text="Usuário cadastrado com sucesso!", foreground="green")
        nome_entry.delete(0, tk.END)
        cpf_entry.delete(0, tk.END)
    except sqlite3.IntegrityError:
        mostrar_cadastro.config(text="Erro: CPF já cadastrado.", foreground="red")
    except Exception as e:
        mostrar_cadastro.config(text="Erro ao salvar no banco.", foreground="red")

def run_imc():
    try:
        peso_ = float(peso.get())
        altura_ = float(altura.get())
        resultado = cl.imc(peso_, altura_)
        r = round(resultado, 2)
        mostrar_imc.config(text=f"IMC: {r}", foreground="#0066cc")
    except ValueError:
        mostrar_imc.config(text="Insira valores válidos", foreground="red")

def run_calculo_h():
    try:
        carga_ = float(carga.get())
        salario_ = float(salario.get())
        resultado = cl.calculo_sal_hora(carga_, salario_)
        r = round(resultado, 2)
        mostrar_sal.config(text=f"R$ {r} / hora", foreground="#0066cc")
    except ValueError:
        mostrar_sal.config(text="Insira carga e salário", foreground="red")

def run_extra():
    try:
        q = int(quantidade.get())
        carga_ = float(carga.get())
        salario_ = float(salario.get())
        resultado = cl.calculo_sal_hora(carga_, salario_)
        r = round(resultado, 2)
        rs = cl.calculo_quantidade_extra50(q, r)
        mostrar_extra.config(text=f"Total Extra: R$ {round(rs, 2)}", foreground="#0066cc")
    except ValueError:
        mostrar_extra.config(text="Preencha todos os campos", foreground="red")


# --- INTERFACE GRÁFICA ---

janela = tk.Tk()
janela.title("Sistema de Cálculos e Cadastro")
janela.geometry("420x400")
janela.configure(bg="#f0f0f0")

# Estilização Moderna
style = ttk.Style()
style.theme_use("clam")
style.configure(".", font=("Helvetica", 11), background="#f0f0f0")
style.configure("TLabel", foreground="#333333")
style.configure("Header.TLabel", font=("Helvetica", 14, "bold"), foreground="#2b2b2b")
style.configure("Resultado.TLabel", font=("Helvetica", 13, "bold"))
style.configure("TButton", font=("Helvetica", 11, "bold"), padding=6)

# Criando as Abas
notebook = ttk.Notebook(janela)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# ---- ABA NOVA: CADASTRO DE PESSOAS ----
aba_cadastro = ttk.Frame(notebook, padding=15)
notebook.add(aba_cadastro, text="Cadastro")

ttk.Label(aba_cadastro, text="Cadastrar Nova Pessoa", style="Header.TLabel").grid(column=0, row=0, columnspan=2, pady=(0, 15))

ttk.Label(aba_cadastro, text="Nome Completo:").grid(column=0, row=1, sticky="w", pady=5)
nome_entry = ttk.Entry(aba_cadastro, font=("Helvetica", 11))
nome_entry.grid(column=0, row=2, columnspan=2, pady=5, sticky="we")

ttk.Label(aba_cadastro, text="CPF:").grid(column=0, row=3, sticky="w", pady=5)
cpf_entry = ttk.Entry(aba_cadastro, font=("Helvetica", 11))
cpf_entry.grid(column=0, row=4, columnspan=2, pady=5, sticky="we")

bt_salvar = ttk.Button(aba_cadastro, text="Salvar no Banco", command=run_cadastro)
bt_salvar.grid(column=0, row=5, columnspan=2, pady=20, sticky="we")

mostrar_cadastro = ttk.Label(aba_cadastro, text="", font=("Helvetica", 11, "bold"))
mostrar_cadastro.grid(column=0, row=6, columnspan=2, pady=5)


# ---- ABA 1: IMC ----
aba_imc = ttk.Frame(notebook, padding=15)
notebook.add(aba_imc, text="IMC")

ttk.Label(aba_imc, text="Cálculo de IMC", style="Header.TLabel").grid(column=0, row=0, columnspan=2, pady=(0, 15))

ttk.Label(aba_imc, text="Peso (kg):").grid(column=0, row=1, sticky="w", pady=5)
peso = ttk.Entry(aba_imc, font=("Helvetica", 11))
peso.grid(column=0, row=2, padx=(0, 10), pady=5, sticky="we")

ttk.Label(aba_imc, text="Altura (m):").grid(column=1, row=1, sticky="w", pady=5)
altura = ttk.Entry(aba_imc, font=("Helvetica", 11))
altura.grid(column=1, row=2, pady=5, sticky="we")

bt_imc = ttk.Button(aba_imc, text="Calcular IMC", command=run_imc)
bt_imc.grid(column=0, row=3, columnspan=2, pady=20, sticky="we")

mostrar_imc = ttk.Label(aba_imc, text="", style="Resultado.TLabel")
mostrar_imc.grid(column=0, row=4, columnspan=2, pady=5)


# ---- ABA 2: SALÁRIO E HORA EXTRA ----
aba_salario = ttk.Frame(notebook, padding=15)
notebook.add(aba_salario, text="Salário & Horas")

ttk.Label(aba_salario, text="Cálculo de Salário Hora", style="Header.TLabel").grid(column=0, row=0, columnspan=2, pady=(0, 10))

ttk.Label(aba_salario, text="Carga Horária:").grid(column=0, row=1, sticky="w", pady=2)
carga = ttk.Entry(aba_salario, font=("Helvetica", 11))
carga.grid(column=0, row=2, padx=(0, 10), pady=2, sticky="we")

ttk.Label(aba_salario, text="Salário Base:").grid(column=1, row=1, sticky="w", pady=2)
salario = ttk.Entry(aba_salario, font=("Helvetica", 11))
salario.grid(column=1, row=2, pady=2, sticky="we")

bt_sal = ttk.Button(aba_salario, text="Calcular Hora", command=run_calculo_h)
bt_sal.grid(column=0, row=3, columnspan=2, pady=10, sticky="we")

mostrar_sal = ttk.Label(aba_salario, text="", style="Resultado.TLabel")
mostrar_sal.grid(column=0, row=4, columnspan=2, pady=2)

# Divisor visual
ttk.Separator(aba_salario, orient="horizontal").grid(column=0, row=5, columnspan=2, sticky="we", pady=10)

ttk.Label(aba_salario, text="Quantidade de Horas Extras:").grid(column=0, row=6, sticky="w", pady=2)
quantidade = ttk.Entry(aba_salario, font=("Helvetica", 11))
quantidade.grid(column=0, row=7, padx=(0, 10), pady=2, sticky="we")

bt_ex = ttk.Button(aba_salario, text="Calcular Extra", command=run_extra)
bt_ex.grid(column=1, row=7, pady=2, sticky="we")

mostrar_extra = ttk.Label(aba_salario, text="", style="Resultado.TLabel")
mostrar_extra.grid(column=0, row=8, columnspan=2, pady=10)


# Configuração de redimensionamento de colunas
aba_cadastro.columnconfigure(0, weight=1)
aba_cadastro.columnconfigure(1, weight=1)
aba_imc.columnconfigure(0, weight=1)
aba_imc.columnconfigure(1, weight=1)
aba_salario.columnconfigure(0, weight=1)
aba_salario.columnconfigure(1, weight=1)

janela.mainloop()