from PyQt5 import QtWidgets, QtCore, QtGui      # Importando as bibliotecas so PyQt5 
                                                #   QtWidgets → janelas, botões, interface
                                                #   QtWidgets → janelas, botões, interface
                                                #   QtGui → desenho (cores, pincéis, etc)
from .zone_config import ZoneConfig  # Importa a configuração da zona de interesse
from core.action_command import run_action  # Importa a função para executar a ação quando a zona for cruzada

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
                monitor_area["left"],   # Define a posição horizontal da janela (distância da borda esquerda da tela)
                monitor_area["top"],    # Define a posição vertical da janela (distância da borda superior da tela)
                monitor_area["width"],  # Define a largura da janela
                monitor_area["height"], # Define a altura da janela
            )
        else:
            screen = QtWidgets.QApplication.primaryScreen()  # Obtém a tela principal
            size = screen.size()   # Obtém o tamanho da tela
            self.setGeometry(0, 0, size.width(), size.height())   # Define a geometria da janela para cobrir toda a tela

        self.boxes = []   # Lista para armazenar os retângulos desenhados
        self.zone = ZoneConfig()  # Carrega a configuração da zona de interesse
        self.zone_crossed = False  # Controla se a zona já foi cruzada no estado atual

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

    def _rects_intersect(self, a, b):                               # Método para verificar se dois retângulos se intersectam
        """Retorna True se os retângulos a e b se intersectam.

        Args:
            a: tupla (x1, y1, x2, y2)
            b: tupla (x1, y1, x2, y2)
        """
        ax1, ay1, ax2, ay2 = a                                      # Desempacotando as coordenadas do retângulo a
        bx1, by1, bx2, by2 = b                                      # Desempacotando as coordenadas do retângulo b
        return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)   # Verificando se os retângulos não se intersectam (um está completamente à esquerda, direita, acima ou abaixo do outro)

    def set_boxes(self, boxes):                                         # Método para atualizar as caixas a serem desenhadas e verificar se alguma delas cruza a zona configurada
        """Atualiza as caixas a serem desenhadas e emite mensagem
        no terminal se alguma delas cruzar a zona configurada."""
        self.boxes = boxes                                    # Atualizando a lista de retângulos com as novas coordenadas fornecidas       
        if not self.zone.has_zone():                            # Verificando se a zona de interesse está configurada, se não estiver, não há necessidade de verificar interseção, apenas desenhar os retângulos
            return      # Se a zona de interesse não estiver configurada, apenas desenha os retângulos sem verificar interseção

        zone = self.zone.get_zone()                            # Obtendo as coordenadas da zona de interesse para verificar a interseção com os retângulos fornecidos   
        if zone is None:                                        # Se a zona de interesse não estiver configurada corretamente, não há necessidade de verificar interseção, apenas desenhar os retângulos
            return                                              # Se a zona de interesse não estiver configurada corretamente, apenas desenha os retângulos sem verificar interseção

        current_intersect = any(self._rects_intersect(b, zone) for b in boxes)  # Verificando se algum dos retângulos fornecidos cruza a zona de interesse, usando o método _rects_intersect para verificar a interseção entre cada retângulo e a zona

        if current_intersect and not self.zone_crossed:                             # Se algum retângulo cruza a zona de interesse e a zona ainda não foi marcada como cruzada, emite um alerta e executa a ação definida
            print("ALERTA: detecção cruzou a zona de limite!")                      # Imprime uma mensagem de alerta no terminal indicando que a zona de interesse foi cruzada
            run_action()  # Executa a ação definida quando a zona for cruzada
            self.zone_crossed = True                    # Marca a zona como cruzada para evitar múltiplos alertas enquanto a zona estiver sendo cruzada                         
        elif not current_intersect and self.zone_crossed:                      # Se nenhum retângulo cruza a zona de interesse e a zona estava marcada como cruzada, reseta o estado para permitir futuros alertas                  
            self.zone_crossed = False                   # Reseta o estado de cruzamento da zona para permitir futuros alertas quando a zona for cruzada novamente