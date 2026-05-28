import os
from PyQt5 import QtGui


class ZoneConfig:
    """Gerencia a configuração da zona de interesse (retângulo fixo de limite)"""
    
    def __init__(self):
        self.zone_coordinates = self._parse_zone_from_env()
        self.zone_color = QtGui.QColor(255, 165, 0)  # Laranja
        self.zone_pen_width = 2
    
    def _parse_zone_from_env(self):
        """Lê a zona de interesse das variáveis de ambiente
        
        Formato esperado: ZONE_OF_INTEREST="x1,y1,x2,y2"
        Exemplo: ZONE_OF_INTEREST="100,100,1820,1080"
        """
        zone_str = os.getenv("ZONE_OF_INTEREST", None)
        if zone_str:
            try:
                coords = list(map(int, zone_str.split(",")))
                if len(coords) == 4:
                    return tuple(coords)
                else:
                    print(f"⚠️  Aviso: ZONE_OF_INTEREST deve ter 4 coordenadas, recebeu {len(coords)}")
            except ValueError:
                print(f"⚠️  Aviso: ZONE_OF_INTEREST com formato inválido: {zone_str}. Use: x1,y1,x2,y2")
        return None
    
    def has_zone(self):
        """Verifica se uma zona foi configurada"""
        return self.zone_coordinates is not None
    
    def get_zone(self):
        """Retorna as coordenadas da zona (x1, y1, x2, y2)"""
        return self.zone_coordinates
    
    def draw_zone(self, painter):
        """Desenha a zona de interesse no painter
        
        Args:
            painter: QtGui.QPainter object para desenhar
        """
        if not self.has_zone():
            return
        
        x1, y1, x2, y2 = self.zone_coordinates
        pen = QtGui.QPen(self.zone_color)
        pen.setWidth(self.zone_pen_width)
        painter.setPen(pen)
        painter.drawRect(x1, y1, x2 - x1, y2 - y1)
