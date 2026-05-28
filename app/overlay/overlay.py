from PyQt5 import QtWidgets, QtCore, QtGui      # Importando as bibliotecas so PyQt5 
                                                #   QtWidgets → janelas, botões, interface
                                                #   QtWidgets → janelas, botões, interface
                                                #   QtGui → desenho (cores, pincéis, etc)
from .zone_config import ZoneConfig  # Importa a configuração da zona de interesse

class Overlay(QtWidgets.QWidget):   #   Criando a classe Overlay que herda de QWidget
    def __init__(self, monitor_area=None):   # Método construtor da classe
        super().__init__()   # Chamando o construtor da classe pai

        self.setWindowFlags(        # Definindo as flags da janela para que ela seja transparente e fique sempre no topo
            QtCore.Qt.FramelessWindowHint |     # Remove a borda da janela
            QtCore.Qt.WindowStaysOnTopHint |    # Mantém a janela sempre no topo
            QtCore.Qt.Tool                      # Permite que a janela seja usada como uma ferramenta, evitando que apareça na barra de tarefas
        )

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)   # Define o fundo da janela como transparente
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)   # Permite que os eventos de mouse passem através da janela, tornando-a clicável

        if monitor_area:
            # Alinha o overlay com a mesma região capturada pelo mss (monitor correto).
            self.setGeometry(
                monitor_area["left"],
                monitor_area["top"],
                monitor_area["width"],
                monitor_area["height"],
            )
        else:
            screen = QtWidgets.QApplication.primaryScreen()  # Obtém a tela principal
            size = screen.size()   # Obtém o tamanho da tela
            self.setGeometry(0, 0, size.width(), size.height())   # Define a geometria da janela para cobrir toda a tela

        self.boxes = []   # Lista para armazenar os retângulos desenhados
        self.zone = ZoneConfig()  # Carrega a configuração da zona de interesse

        self.show()    # Exibe a janela

    def paintEvent(self, event):   # Método para desenhar os retângulos na janela
        painter = QtGui.QPainter(self)   # Criando um objeto QPainter para desenhar na janela
        
        # Desenha a zona de interesse (retângulo fixo) primeiro
        self.zone.draw_zone(painter)
        
        pen = QtGui.QPen(QtGui.QColor(0, 255, 0))  # Criando um objeto QPen para definir a cor e a largura da borda dos retângulos
        pen.setWidth(3)    # definindo a largura da borda dos retângulos
        painter.setPen(pen)    # Definindo o pen para o painter

        for (x1, y1, x2, y2) in self.boxes:   # Iterando sobre a lista de retângulos e desenhando cada um deles
            painter.drawRect(x1, y1, x2 - x1, y2 - y1)    # Desenhando um retângulo com as coordenadas fornecidas