# ===== IMPORTS PRINCIPAIS =====
import sys                          # Permite interagir com o sistema (argumentos e saída do programa)
import os
from PyQt5 import QtWidgets        # Módulo do PyQt responsável pela interface gráfica
from dotenv import load_dotenv         # Permite carregar variáveis de ambiente de um arquivo .env



# ===== IMPORTS DOS MÓDULOS DO PROJETO =====
from core.capture import ScreenCapture          # Classe responsável por capturar a tela
from core.detector import Detector              # Classe responsável por detectar objetos (YOLO)
from overlay.overlay import Overlay             # Classe responsável por desenhar na tela (overlay)
from workers.detection_worker import DetectionWorker  # Thread que executa captura + detecção


def main():
    load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

    # Inicializa a aplicação PyQt (obrigatório para qualquer interface gráfica)
    app = QtWidgets.QApplication(sys.argv)


    # ===== INSTÂNCIAS DOS COMPONENTES =====

    # Defina MONITOR_INDEX=1,2,3... para escolher qual monitor capturar/desenhar.
    monitor_index = int(os.getenv("MONITOR_INDEX", "1"))

    capture = ScreenCapture(monitor_index=monitor_index)   # Responsável por capturar frames da tela
    detector = Detector()       # Responsável por detectar objetos nos frames
    overlay = Overlay(monitor_area=capture.monitor)         # Janela transparente que desenha os retângulos na tela


    # ===== THREAD DE PROCESSAMENTO =====

    worker = DetectionWorker(capture, detector)
    # Cria a thread que irá rodar continuamente:
    # captura → detecta → envia resultados


    # ===== CONEXÃO DOS SINAIS =====

    worker.update_boxes.connect(
        overlay.set_boxes
    )
    # Sempre que a thread enviar novas caixas:
    # atualiza a lista de boxes do overlay

    worker.update_boxes.connect(overlay.update)
    # Após atualizar os dados:
    # força o redesenho da tela (paintEvent)


    # ===== INICIA A THREAD =====

    worker.start()
    # Começa a execução paralela (chama o método run() da thread)


    # ===== LOOP PRINCIPAL DA INTERFACE =====

    sys.exit(app.exec_())
    # Inicia o loop da interface gráfica (mantém a aplicação rodando)


# ===== PONTO DE ENTRADA =====
if __name__ == "__main__":      
    main()
    # Garante que o código só execute quando o arquivo for rodado diretamente
