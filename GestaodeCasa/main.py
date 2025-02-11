from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QFrame, QTreeWidget,
                           QTreeWidgetItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import locale

class GestaoFamiliar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestão Familiar")
        self.setGeometry(100, 100, 800, 600)
        
        # Configurar locale para português brasileiro
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        
        self.data_atual = datetime.now()
        
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # Painel esquerdo (contas)
        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.Shape.StyledPanel)
        left_panel.setFixedWidth(200)  # Largura fixa para o painel esquerdo
        left_layout = QVBoxLayout(left_panel)
        
        # Adicionar contas
        self.criar_painel_contas(left_layout)
        
        # Painel central (transações)
        central_panel = QFrame()
        central_panel.setFrameShape(QFrame.Shape.StyledPanel)
        central_layout = QVBoxLayout(central_panel)
        
        # Adicionar área de transações
        self.criar_painel_transacoes(central_layout)
        
        # Painel direito
        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.Shape.StyledPanel)
        right_panel.setFixedWidth(200)
        right_layout = QVBoxLayout(right_panel)
        
        # Adicionar botões ao painel direito
        self.criar_botoes_direita(right_layout)
        
        # Adicionar painéis ao layout principal
        main_layout.addWidget(left_panel)
        main_layout.addWidget(central_panel)
        main_layout.addWidget(right_panel)

    def criar_painel_contas(self, layout):
        # Container para Banco (Receita)
        container_banco = QFrame()
        container_banco.setFrameShape(QFrame.Shape.StyledPanel)
        container_banco.setFrameShadow(QFrame.Shadow.Raised)
        container_banco_layout = QVBoxLayout(container_banco)
        
        # Banco (Receita)
        banco_frame = QFrame()
        banco_layout = QVBoxLayout(banco_frame)
        banco_label = QLabel("Receita")
        banco_label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        banco_valor = QLabel("R$152.458,37")
        banco_valor.setStyleSheet("font-size: 14pt;")
        banco_layout.addWidget(banco_label)
        banco_layout.addWidget(banco_valor)
        container_banco_layout.addWidget(banco_frame)
        
        # Container para Carteira (Despesas)
        container_carteira = QFrame()
        container_carteira.setFrameShape(QFrame.Shape.StyledPanel)
        container_carteira.setFrameShadow(QFrame.Shadow.Raised)
        container_carteira_layout = QVBoxLayout(container_carteira)
        
        # Carteira (Despesas)
        carteira_frame = QFrame()
        carteira_layout = QVBoxLayout(carteira_frame)
        carteira_label = QLabel("Despesas")
        carteira_label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        carteira_valor = QLabel("R$80,00")
        carteira_valor.setStyleSheet("font-size: 14pt;")
        carteira_layout.addWidget(carteira_label)
        carteira_layout.addWidget(carteira_valor)
        container_carteira_layout.addWidget(carteira_frame)
        
        # Adicionar frames ao layout principal
        layout.addWidget(container_banco)
        layout.addWidget(container_carteira)
        layout.addStretch()

    def criar_painel_transacoes(self, layout):
        # Cabeçalho com mês
        header_layout = QHBoxLayout()
        
        # Criar container para centralização
        btn_prev = QPushButton("<")
        btn_prev.setFixedWidth(30)
        
        self.mes_label = QLabel()
        self.atualizar_label_mes()
        self.mes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_next = QPushButton(">")
        btn_next.setFixedWidth(30)
        
        # Conectar botões aos métodos
        btn_prev.clicked.connect(self.mes_anterior)
        btn_next.clicked.connect(self.mes_seguinte)
        
        # Adicionar stretch antes e depois para centralizar
        header_layout.addStretch()
        header_layout.addWidget(btn_prev)
        header_layout.addWidget(self.mes_label)
        header_layout.addWidget(btn_next)
        header_layout.addStretch()
        
        # Tree widget para transações
        tree = QTreeWidget()
        tree.setHeaderLabels(["Descrição", "Valor", "Data"])
        tree.setStyleSheet("""
            QTreeWidget {
                font-size: 12pt;
            }
            QHeaderView::section {
                font-size: 12pt;
                font-weight: bold;
            }
        """)
        
        # Desabilitar seleção
        tree.setSelectionMode(QTreeWidget.SelectionMode.NoSelection)
        
        # Cores personalizadas
        verde_escuro = QColor(0, 100, 0)  # Verde escuro
        vermelho_escuro = QColor(139, 0, 0)  # Vermelho escuro
        
        # Exemplo de dados
        receitas = QTreeWidgetItem(tree, ["Receitas"])
        receitas.setFlags(receitas.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        # Definir cor verde para receitas
        for coluna in range(3):
            receitas.setBackground(coluna, verde_escuro)
            receitas.setForeground(coluna, Qt.GlobalColor.white)
        
        item_receita = QTreeWidgetItem(receitas, ["Salário", "R$ 5.000,00", "01/10/2008"])
        for coluna in range(3):
            item_receita.setBackground(coluna, verde_escuro)
            item_receita.setForeground(coluna, Qt.GlobalColor.white)
        
        # Expandir Receitas
        receitas.setExpanded(True)
        
        despesas = QTreeWidgetItem(tree, ["Despesas"])
        despesas.setFlags(despesas.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        # Definir cor vermelha para despesas
        for coluna in range(3):
            despesas.setBackground(coluna, vermelho_escuro)
            despesas.setForeground(coluna, Qt.GlobalColor.white)
        
        item_despesa = QTreeWidgetItem(despesas, ["Aluguel", "R$ 1.500,00", "05/10/2008"])
        for coluna in range(3):
            item_despesa.setBackground(coluna, vermelho_escuro)
            item_despesa.setForeground(coluna, Qt.GlobalColor.white)
            
        # Expandir Despesas
        despesas.setExpanded(True)
        
        # Adicionar widgets ao layout
        layout.addLayout(header_layout)
        layout.addWidget(tree)

    def atualizar_label_mes(self):
        mes = self.data_atual.strftime("%B").capitalize()
        ano = self.data_atual.strftime("%Y")
        self.mes_label.setText(f"{mes} {ano}")

    def mes_anterior(self):
        self.data_atual = self.data_atual - relativedelta(months=1)
        self.atualizar_label_mes()
        self.atualizar_transacoes()

    def mes_seguinte(self):
        self.data_atual = self.data_atual + relativedelta(months=1)
        self.atualizar_label_mes()
        self.atualizar_transacoes()

    def atualizar_transacoes(self):
        # Aqui você pode implementar a lógica para atualizar as transações
        # baseado no mês selecionado
        pass

    def criar_botoes_direita(self, layout):
        # Estilo comum para todos os botões
        estilo_botao = """
            QPushButton {
                font-size: 14pt;
                padding: 10px;
                margin: 5px;
                border-radius: 5px;
                background-color: #2c3e50;
                color: white;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """
        
        # Botão Adicionar
        btn_adicionar = QPushButton("Adicionar")
        btn_adicionar.setStyleSheet(estilo_botao)
        
        # Botão Editar
        btn_editar = QPushButton("Editar")
        btn_editar.setStyleSheet(estilo_botao)
        
        # Botão Excluir
        btn_excluir = QPushButton("Excluir")
        btn_excluir.setStyleSheet(estilo_botao + """
            QPushButton {
                background-color: #c0392b;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
        """)
        
        # Adicionar botões ao layout
        layout.addWidget(btn_adicionar)
        layout.addWidget(btn_editar)
        layout.addWidget(btn_excluir)
        layout.addStretch()  # Empurra os botões para o topo

def main():
    app = QApplication(sys.argv)
    window = GestaoFamiliar()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()