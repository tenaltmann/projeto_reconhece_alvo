
import cv2
from ultralytics import YOLO        # Usado para detectar o item / individuo na imagem

class Detector :
    def __init__(self, model_path="models/yolov8n.pt"):     # Carrega o modelo pré-treinado do YOLO
        self.model = YOLO(model_path)          # Carrega a versão leve do modelo pré-treinado

    def detect(self, frame):                   # Método para detectar objetos em um frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ##################################
        cv2.imwrite("debug_frame.png", frame)

        results = self.model(frame, verbose=False)   # Envia o frame para o YOLO e detecta os objetos
        
        boxes = []      # Lista para armazenar as caixas de detecção


        for r in results:                   # Percorre os resultados encontrados
            for box in r.boxes:             # Percorre todas as caixas (objetos encontrados)

                cls = int(box.cls[0])       # Obtém a classe (tipo de) do objeto encontrado
                conf = float(box.conf[0])   # Obtém a confiança da detecção (0 a 1)

                print(f"Classe: {cls}, Conf: {conf:.2f}")

                if cls == 16 and conf > 0.1:    # Se cls for igual a 16 (código de cachorro) e conf (confiabilidade da detecção) maior que 0.3 (30% de certeza)
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Armazena as coordenadas da caixa após a detecção
                    boxes.append((x1, y1, x2, y2))  # Adiciona as coordenadas da caixa à lista de boxes
        return boxes