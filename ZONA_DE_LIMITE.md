# 🎯 Zona de Limite (Zone of Interest)

## 📋 Visão Geral

Agora você pode desenhar um retângulo fixo na tela que marca uma **zona de limite** para a detecção de cachorros. Este retângulo permanece fixo enquanto as detecções são mostradas dinamicamente.

## 🎨 Cores Utilizadas

- 🟠 **Laranja**: Zona de limite (retângulo fixo) - configurado em `zone_config.py`
- 🟢 **Verde**: Detecções de cachorros (retângulos dinâmicos)

## 📦 Estrutura de Arquivos

A zona de interesse foi implementada em um arquivo separado para manter o projeto organizado:

```
app/
├── overlay/
│   ├── __init__.py
│   ├── overlay.py          (modificado minimamente - apenas importa zone_config)
│   └── zone_config.py      ✨ NOVO - Gerencia a zona de interesse
├── main.py                 (sem alterações)
└── ...
```

## 🚀 Como Usar

### Opção 1: Variável de Ambiente (PowerShell)

```powershell
$env:ZONE_OF_INTEREST = "100,100,1820,1080"
python app/main.py
```

### Opção 2: Arquivo `.env`

1. Copie o arquivo `.env.example`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edite o arquivo `.env` e descomente a linha de `ZONE_OF_INTEREST`:
   ```
   ZONE_OF_INTEREST=100,100,1820,1080
   ```

3. Execute normalmente:
   ```powershell
   python app/main.py
   ```

## 📐 Coordenadas

O formato é: `x1,y1,x2,y2` onde:
- **x1, y1** = canto superior esquerdo (em pixels)
- **x2, y2** = canto inferior direito (em pixels)

### Exemplos

**Tela 1920x1080 com margens:**
```
ZONE_OF_INTEREST=100,100,1820,1000
```
- Começa em (100px, 100px)
- Termina em (1820px, 1000px)
- Deixa ~100px de margem nas laterais e ~80px no topo/rodapé

**Tela inteira:**
```
ZONE_OF_INTEREST=0,0,1920,1080
```

## 💡 Dicas

1. **Para encontrar as coordenadas:**
   - Use uma ferramenta de screenshot (Print Screen + Paint)
   - Ou use o inspetor de pixel do seu SO
   - Anote (x1, y1) no canto superior esquerdo desejado
   - Anote (x2, y2) no canto inferior direito desejado

2. **Desabilitar a zona:**
   - Deixe a variável vazia ou comente-a
   - Assim usará toda a tela sem retângulo fixo

3. **Ajustes finos:**
   - Inicie com um retângulo grande
   - Vá reduzindo até ajustar a zona desejada
   - Deixe margem para os retângulos de detecção terem espaço

## 🔧 Modificar as Cores

Se quiser mudar a cor do retângulo fixo, edite `zone_config.py`:

```python
self.zone_color = QtGui.QColor(255, 165, 0)  # Altere estes valores
```

**Exemplos de cores (RGB):**
- Vermelho: `(255, 0, 0)`
- Verde: `(0, 255, 0)`
- Azul: `(0, 0, 255)`
- Amarelo: `(255, 255, 0)`
- Ciano: `(0, 255, 255)`

## 📝 Avisos

- Se o formato de `ZONE_OF_INTEREST` estiver inválido, você verá um aviso no console
- A zona é desenhada **atrás** das detecções, então não interfere na visibilidade dos retângulos de cachorros
