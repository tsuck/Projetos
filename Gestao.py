import tkinter as tk
from tkinter import messagebox

class GestaoFinanceira:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gestão Financeira Doméstica")
        self.contas = []
        
        # Função para remover foco de qualquer campo
        def remover_foco(event):
            event.widget.focus_set()
        
        # Adiciona o evento para todos os frames principais
        self.root.bind_class('Frame', '<Button-1>', remover_foco)
        self.root.bind_class('LabelFrame', '<Button-1>', remover_foco)
        self.root.bind('<Button-1>', remover_foco)
        
        # Frame para entrada de salário e comida
        frame_dados = tk.LabelFrame(self.root, text="Dados Principais", padx=5, pady=5)
        frame_dados.pack(fill="x", padx=10, pady=5)
        
        # Função para validar entrada apenas de números
        def validar_numero(P):
            # Permite campo vazio ou números com até um ponto decimal
            if P == "" or (P.replace(".", "", 1).isdigit() and P.count(".") <= 1):
                return True
            return False
            
        # Função para validar apenas números inteiros
        def validar_inteiro(P):
            # Permite campo vazio ou apenas números inteiros
            if P == "" or P.isdigit():
                return True
            return False

        # Registra a validação
        validacao_numero = self.root.register(validar_numero)
        validacao_inteiro = self.root.register(validar_inteiro)
        
        # Função para formatar números com pontuação
        def formatar_numero(event, entry):
            texto = entry.get().replace(",", "").replace(".", "")
            if texto:
                try:
                    numero = int(texto)
                    texto_formatado = "{:,}".format(numero)
                    entry.delete(0, tk.END)
                    entry.insert(0, texto_formatado)
                except ValueError:
                    pass
            return True

        # Função para limpar formatação ao focar no campo
        def limpar_formatacao(event, entry):
            texto = entry.get().replace(",", "")
            entry.delete(0, tk.END)
            entry.insert(0, texto)
            return True

        # Função para aplicar formatação em um Entry
        def configurar_formatacao(entry):
            entry.bind('<FocusOut>', lambda e, entry=entry: formatar_numero(e, entry))
            entry.bind('<FocusIn>', lambda e, entry=entry: limpar_formatacao(e, entry))
        
        # Função para limpar zero inicial
        def limpar_zero_inicial(event):
            if event.widget.get() == "0":
                event.widget.delete(0, tk.END)

        # Função para restaurar zero se vazio
        def restaurar_zero(event):
            if event.widget.get() == "":
                event.widget.insert(0, "0")

        # Função para configurar comportamento do zero
        def configurar_zero(entry):
            entry.bind('<FocusIn>', limpar_zero_inicial)
            entry.bind('<FocusOut>', restaurar_zero)

        # Campo de salário com R$
        tk.Label(frame_dados, text="Salário:      R$").grid(row=0, column=0, sticky="e")
        self.salario_entry = tk.Entry(frame_dados, validate="key", 
                                    validatecommand=(validacao_numero, '%P'))
        self.salario_entry.grid(row=0, column=1)
        
        # Frame para gastos com comida
        frame_comida = tk.LabelFrame(frame_dados, text="Alimentação", padx=5, pady=5)
        frame_comida.grid(row=1, column=0, columnspan=3, pady=5, sticky="ew")
        
        # Subframe para composição familiar
        frame_composicao = tk.Frame(frame_comida)
        frame_composicao.grid(row=0, column=0, columnspan=5, pady=(0,5))
        
        # Campos de composição familiar
        tk.Label(frame_composicao, text="Quantidade de Adultos:").grid(row=0, column=0, sticky="e")
        self.adultos_entry = tk.Entry(frame_composicao, width=5, validate="key",
                                    validatecommand=(validacao_inteiro, '%P'))
        self.adultos_entry.grid(row=0, column=1)
        self.adultos_entry.insert(0, "0")
        configurar_zero(self.adultos_entry)
        self.adultos_entry.bind('<Return>', lambda e: self.criancas_entry.focus())
        self.adultos_entry.bind('<FocusOut>', self.recalcular_composicao)
        
        tk.Label(frame_composicao, text="Quantidade de Crianças:").grid(row=0, column=2, sticky="e", padx=(10,0))
        self.criancas_entry = tk.Entry(frame_composicao, width=5, validate="key",
                                     validatecommand=(validacao_inteiro, '%P'))
        self.criancas_entry.grid(row=0, column=3)
        self.criancas_entry.insert(0, "0")
        configurar_zero(self.criancas_entry)
        self.criancas_entry.bind('<Return>', self.recalcular_composicao)
        self.criancas_entry.bind('<FocusOut>', self.recalcular_composicao)
        
        # Subframe para entrada manual
        frame_manual = tk.Frame(frame_comida)
        frame_manual.grid(row=1, column=0, columnspan=5)
        
        tk.Label(frame_manual, text="Valor Mensal:").grid(row=0, column=0, sticky="e", padx=(0,10))
        tk.Label(frame_manual, text="R$").grid(row=0, column=1, sticky="e", padx=(0,5))
        self.gasto_comida_entry = tk.Entry(frame_manual, validate="key",
                                         validatecommand=(validacao_numero, '%P'))
        self.gasto_comida_entry.grid(row=0, column=2)
        self.gasto_comida_entry.insert(0, "0")
        configurar_zero(self.gasto_comida_entry)
        self.gasto_comida_entry.bind('<FocusOut>', self.recalcular_composicao)

        # Botão de ajuda com tooltip
        class CreateToolTip(object):
            def __init__(self, widget, text):
                self.widget = widget
                self.text = text
                self.tooltip = None
                self.widget.bind('<Enter>', self.enter)
                self.widget.bind('<Leave>', self.leave)

            def enter(self, event=None):
                x, y, _, _ = self.widget.bbox("insert")
                x += self.widget.winfo_rootx() + 25
                y += self.widget.winfo_rooty() + 20
                
                self.tooltip = tk.Toplevel(self.widget)
                self.tooltip.wm_overrideredirect(True)
                self.tooltip.wm_geometry(f"+{x}+{y}")
                
                label = tk.Label(self.tooltip, text=self.text, justify='left',
                               background="#ffffe0", relief='solid', borderwidth=1,
                               wraplength=400, padx=4, pady=4)
                label.pack()

            def leave(self, event=None):
                if self.tooltip:
                    self.tooltip.destroy()
                    self.tooltip = None

        help_button = tk.Label(frame_manual, text="?", font=("Arial", 10, "bold"),
                             fg="blue", cursor="hand2")
        help_button.grid(row=0, column=3, padx=(5,0))

        tooltip_text = (
            "Cálculo automático por pessoa baseado em dados do IBGE/DIEESE:\n\n"
            "Adulto (mensal):\n"
            "• Almoço durante trabalho: R$25,00 × 22 dias = R$550,00\n"
            "• Compras mensais (cesta básica ampliada): R$750,00\n"
            "Total adulto: R$1.300,00\n\n"
            "Criança:\n"
            "• 75% do valor da cesta básica\n"
            "• Não inclui almoço (considera merenda escolar)\n"
            "Total criança: R$562,50\n\n"
            "Valores baseados em dados do IBGE (POF),\n"
            "DIEESE (Cesta Básica) e CONAB (2024)\n\n"
            "Você também pode inserir o valor manualmente neste campo."
        )

        CreateToolTip(help_button, tooltip_text)
        
        # Frame para contas fixas
        frame_contas = tk.LabelFrame(self.root, text="Contas Fixas", padx=5, pady=5)
        frame_contas.pack(fill="x", padx=10, pady=5)
        
        # Lista de contas fixas
        self.contas_fixas = {
            'Aluguel': tk.StringVar(),
            'Energia': tk.StringVar(),
            'Água': tk.StringVar(),
            'Internet': tk.StringVar(),
            'Condomínio': tk.StringVar()
        }
        
        # Criar campos para cada conta fixa
        for i, (tipo_conta, var) in enumerate(self.contas_fixas.items()):
            tk.Label(frame_contas, text=f"{tipo_conta}:").grid(row=i, column=0, sticky="e", padx=(5,10), pady=2)
            tk.Label(frame_contas, text="R$").grid(row=i, column=1, sticky="e", padx=(0,5))
            entry = tk.Entry(frame_contas, textvariable=var, width=15, validate="key",
                           validatecommand=(validacao_numero, '%P'))
            entry.grid(row=i, column=2, sticky="w")
            entry.insert(0, "0")
            configurar_zero(entry)
            entry.bind('<Return>', lambda e: self.registrar_contas_fixas())
        
        # Botão para registrar contas fixas
        tk.Button(frame_contas, text="Registrar Contas Fixas", 
                 command=self.registrar_contas_fixas).grid(row=len(self.contas_fixas), 
                 column=0, columnspan=3, pady=5, sticky="nsew")

        # Frame separado para contas adicionais
        frame_adicionais = tk.LabelFrame(self.root, text="Gastos Adicionais", padx=5, pady=5)
        frame_adicionais.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame_adicionais, text="Tipo:").grid(row=0, column=0, sticky="e", padx=(5,10))
        self.conta_manual_tipo = tk.Entry(frame_adicionais, width=19)
        self.conta_manual_tipo.grid(row=0, column=1, columnspan=2, sticky="w")
        self.conta_manual_tipo.bind('<Return>', lambda e: self.conta_manual_valor.focus())
        
        tk.Label(frame_adicionais, text="Valor:").grid(row=1, column=0, sticky="e", padx=(5,10))
        tk.Label(frame_adicionais, text="R$").grid(row=1, column=1, sticky="e", padx=(0,5))
        self.conta_manual_valor = tk.Entry(frame_adicionais, width=15, validate="key",
                                         validatecommand=(validacao_numero, '%P'))
        self.conta_manual_valor.grid(row=1, column=2, sticky="w")
        self.conta_manual_valor.insert(0, "0")
        configurar_zero(self.conta_manual_valor)
        self.conta_manual_valor.bind('<Return>', lambda e: self.adicionar_conta_manual())

        # Botão para adicionar conta adicional
        tk.Button(frame_adicionais, text="Adicionar Conta", 
                 command=self.adicionar_conta_manual).grid(row=2, column=0, 
                 columnspan=3, pady=5, sticky="nsew")
        
        # Frame para lista de contas registradas
        frame_lista = tk.LabelFrame(self.root, text="Contas Registradas", padx=5, pady=5)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.lista_contas = tk.Listbox(frame_lista, height=5)
        self.lista_contas.pack(fill="both", expand=True)
        
        # Frame para botões e resultados (corrige o problema de redimensionamento)
        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(fill="x", padx=10, pady=5)
        
        # Botão calcular e resultados no novo frame
        tk.Button(frame_botoes, text="Calcular Finanças", 
                 command=self.calcular_financas).pack(pady=5)
        
        self.resultado_label = tk.Label(frame_botoes, text="")
        self.resultado_label.pack(pady=5)

    def adicionar_conta_manual(self, event=None):
        tipo = self.conta_manual_tipo.get().strip()
        try:
            valor = float(self.conta_manual_valor.get())
            if tipo and valor > 0:
                self.contas.append({'tipo': tipo, 'valor': valor})
                self.lista_contas.insert(tk.END, f"{tipo}: R${valor:,.2f}")
                # Limpar campos
                self.conta_manual_tipo.delete(0, tk.END)
                self.conta_manual_valor.delete(0, tk.END)
                self.conta_manual_valor.insert(0, "0")
            else:
                messagebox.showerror("Erro", "Insira um tipo de conta e um valor maior que zero.")
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido para a conta manual!")

    def registrar_contas_fixas(self, event=None):
        # Guarda as contas manuais existentes
        contas_manuais = [conta for conta in self.contas if conta['tipo'] not in self.contas_fixas.keys()]
        
        self.contas = contas_manuais  # Mantém apenas as contas manuais
        self.lista_contas.delete(0, tk.END)  # Limpa a listbox
        
        # Mostra as contas manuais novamente
        for conta in contas_manuais:
            self.lista_contas.insert(tk.END, f"{conta['tipo']}: R${conta['valor']:,.2f}")
        
        # Registra as contas fixas
        for tipo_conta, var in self.contas_fixas.items():
            try:
                valor = float(var.get() or 0)
                if valor > 0:
                    self.contas.append({'tipo': tipo_conta, 'valor': valor})
                    self.lista_contas.insert(tk.END, f"{tipo_conta}: R${valor:,.2f}")
            except ValueError:
                messagebox.showerror("Erro", f"Valor inválido para {tipo_conta}")
                return
        
        # Zera todos os campos de contas fixas após registrar
        for var in self.contas_fixas.values():
            var.set("0")

    def calcular_economias(self, salario, gasto_comida):
        total_contas = sum(conta['valor'] for conta in self.contas)
        restante_para_economias = salario - total_contas - gasto_comida
        
        if restante_para_economias < 0:
            economias = 0
            gastos_livres = 0
            messagebox.showwarning("Aviso", "Você está gastando mais do que ganha!")
        else:
            # 40% para guardar, 60% para gastos livres
            economias = restante_para_economias * 0.4
            gastos_livres = restante_para_economias * 0.6
            
        return economias, gastos_livres, restante_para_economias

    def calcular_financas(self):
        # Verificar se o usuário preencheu a composição familiar ou valor manual
        total_pessoas = int(self.adultos_entry.get()) + int(self.criancas_entry.get())
        valor_comida = float(self.gasto_comida_entry.get() or 0)
        
        if total_pessoas == 0 and valor_comida == 0:
            messagebox.showwarning("Atenção", 
                "Por favor:\n\n"
                "1. Preencha a quantidade de pessoas na composição familiar e\n"
                "   clique em 'Calcular Gasto com Comida'\n\n"
                "OU\n\n"
                "2. Insira manualmente o valor mensal com alimentação")
            return

        try:
            salario = float(self.salario_entry.get())
            if salario < 0:
                messagebox.showerror("Erro", "O salário não pode ser negativo!")
                return
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido para o salário!")
            return

        economias, gastos_livres, restante = self.calcular_economias(salario, valor_comida)
        total_contas = sum(conta['valor'] for conta in self.contas)

        self.resultado_label.config(
            text=f"Total de Contas: R${total_contas:,.2f}\n"
                f"Gasto com Comida: R${valor_comida:,.2f}\n"
                f"Valor Total Restante: R${restante:,.2f}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Valor para Guardar (40%): R${economias:,.2f}\n"
                f"Valor para Gastos Livres (60%): R${gastos_livres:,.2f}"
        )

    def calcular_media_japonesa(self):
        try:
            num_adultos = int(self.adultos_entry.get())
            num_criancas = int(self.criancas_entry.get())
            
            if num_adultos < 0 or num_criancas < 0:
                messagebox.showerror("Erro", "A quantidade de pessoas não pode ser negativa!")
                return 0
                
            # Valores base por adulto em reais (mensal)
            ALMOCO_TRABALHO = 25.00 * 22     # R$25 por marmita × 22 dias úteis = R$550
            MERCADO_MENSAL = 750.00          # R$750 para compras mensais (cesta básica ampliada)
            
            # Crianças gastam 75% do valor de um adulto (exceto almoço trabalho)
            FATOR_CRIANCA = 0.75
            
            # Cálculo mensal para adultos
            gasto_adultos = num_adultos * (
                ALMOCO_TRABALHO +    # Almoços durante o trabalho
                MERCADO_MENSAL       # Compras do mês (cesta básica ampliada)
            )
            
            # Cálculo mensal para crianças (sem almoço trabalho)
            gasto_criancas = num_criancas * (
                MERCADO_MENSAL * FATOR_CRIANCA  # Apenas mercado mensal para crianças
            )
            
            return gasto_adultos + gasto_criancas
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira números válidos!")
            return 0

    def recalcular_composicao(self, event=None):
        try:
            # Garante que os campos não fiquem vazios
            if not self.adultos_entry.get():
                self.adultos_entry.insert(0, "0")
            if not self.criancas_entry.get():
                self.criancas_entry.insert(0, "0")
            
            # Verifica se há valor manual inserido
            valor_manual = float(self.gasto_comida_entry.get() or 0)
            if valor_manual > 0:
                return  # Se tiver valor manual, mantém e ignora o cálculo automático
                
            num_adultos = int(self.adultos_entry.get())
            num_criancas = int(self.criancas_entry.get())
            
            # Calcula o novo valor mensal se houver pessoas
            if num_adultos > 0 or num_criancas > 0:
                media_mensal = self.calcular_media_japonesa()
                if media_mensal > 0:
                    self.gasto_comida_entry.delete(0, tk.END)
                    self.gasto_comida_entry.insert(0, str(media_mensal))
            # Se não houver pessoas, zera o valor mensal
            elif num_adultos == 0 and num_criancas == 0:
                self.gasto_comida_entry.delete(0, tk.END)
                self.gasto_comida_entry.insert(0, "0")
        except ValueError:
            # Em caso de erro, garante que os campos tenham 0
            self.adultos_entry.delete(0, tk.END)
            self.adultos_entry.insert(0, "0")
            self.criancas_entry.delete(0, tk.END)
            self.criancas_entry.insert(0, "0")

    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GestaoFinanceira()
    app.iniciar()
