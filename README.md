# Detecção de Cachorro com Overlay de Monitor

Aplicativo de detecção de objetos em tempo real que captura a imagem do monitor, identifica cães usando YOLO e desenha um overlay transparente na tela.

## O que este projeto faz

Este projeto captura o conteúdo de um monitor e aplica um modelo de detecção YOLO para identificar cães no vídeo da tela. Quando o modelo detecta um cachorro, o sistema desenha uma caixa verde ao redor da área detectada diretamente sobre a tela em uma janela transparente.

### Principais recursos

- Captura de tela em tempo real sem usar webcam
- Detecção de objetos com modelo YOLO (`yolov8n.pt`)
- Overlay transparente que desenha bounding boxes no monitor
- Processamento em thread separada para manter a interface responsiva

## Como ele faz

O projeto usa uma arquitetura simples, modular e orientada a eventos:

1. `ScreenCapture` captura frames do monitor usando `mss`
2. `Detector` processa cada frame com `ultralytics.YOLO`
3. `DetectionWorker` roda um loop contínuo em uma thread separada
4. `Overlay` recebe as caixas detectadas e desenha retângulos na tela com `PyQt5`

## Quem faz

Este projeto foi desenvolvido para demonstrar detecção de cães em imagens de tela usando machine learning e uma interface gráfica leve. A arquitetura foi pensada para separar captura, detecção e exibição, permitindo melhorias futuras sem modificar toda a aplicação.

## Estrutura do projeto

```text
.
├── app
│   ├── main.py
│   ├── core
│   │   ├── capture.py
│   │   └── detector.py
│   ├── overlay
│   │   └── overlay.py
│   └── workers
│       └── detection_worker.py
├── models
│   └── yolov8n.pt
├── requirements-cpu.txt
├── requirements-gpu.txt
└── README.md
```

### Arquivos principais

- `app/main.py`: inicializa a aplicação e conecta todos os componentes
- `app/core/capture.py`: captura a tela do monitor
- `app/core/detector.py`: carrega o modelo YOLO e detecta cães
- `app/overlay/overlay.py`: desenha as caixas no monitor em modo transparente
- `app/workers/detection_worker.py`: roda captura e detecção em uma thread
- `models/yolov8n.pt`: modelo YOLO pré-treinado usado para detecção

## Instalação passo a passo

Estas instruções estão focadas em Windows e consideram que você está começando do zero.

### 1. Baixar o repositório

- Clonar via Git:

```powershell
git clone https://github.com/tenaltmann/deteccao_de_cachorro_com_overlay_de_monitor.git
```

- Ou baixar o ZIP no GitHub e descompactar em uma pasta local.

### 2. Abrir a pasta do projeto

- No Explorador de Arquivos, entre na pasta onde o projeto foi baixado.
- Abra o terminal do Windows (PowerShell) dentro dessa pasta.

### 3. Criar e ativar ambiente virtual Python

Se você ainda não tem ambiente virtual criado, execute:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a execução, execute primeiro:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

### 4. Instalar dependências

Escolha o arquivo certo de acordo com seu hardware:

- Para CPUs sem GPU NVIDIA: `requirements-cpu.txt`
- Para máquinas com GPU NVIDIA compatível: `requirements-gpu.txt`

Exemplo para CPU:

```powershell
pip install -r requirements-cpu.txt
```

Exemplo para GPU:

```powershell
pip install -r requirements-gpu.txt
```

### 5. Verificar dependências instaladas

Confirme que o Python e as dependências foram instalados corretamente:

```powershell
python --version  (É necessário a versão 3.12.x ou versão anterior devido inconsistencias nas bibliotecas em versões recentes python)
pip show pyqt5 mss numpy opencv-python ultralytics
```

### 6. Executar o aplicativo

No terminal já com o ambiente ativado, execute:

```powershell
python app\main.py
```

Se tudo estiver funcionando, o aplicativo começará a detectar cães que aparecerem na tela do monitor.

## Configuração de monitor

Por padrão, o aplicativo captura o monitor `1`. Para usar outro monitor, defina a variável de ambiente `MONITOR_INDEX` antes de iniciar:

```powershell
$env:MONITOR_INDEX = 2
python app\main.py
```

## Como funciona internamente

### Captura de tela

`app/core/capture.py` usa `mss` para tirar uma screenshot do monitor selecionado e converte a imagem para um array NumPy.

### Detecção de objetos

`app/core/detector.py` carrega `models/yolov8n.pt` com `ultralytics.YOLO`. Ele converte o frame para RGB e executa a inferência. Só as detecções de classe `16` (cachorro) com confiança acima de `0.1` são retornadas.

### Overlay transparente

`app/overlay/overlay.py` cria uma janela transparente e sem bordas usando `PyQt5`. O overlay permite que o mouse passe através dele e desenha retângulos verdes ao redor dos cães detectados.

### Thread de detecção

`app/workers/detection_worker.py` roda em paralelo ao PyQt, capturando frames, detectando objetos e emitindo os resultados para o overlay.

## Observações importantes

- O projeto funciona melhor com a tela do monitor ajustada para o monitor principal ou para o monitor correto definido em `MONITOR_INDEX`.
- O modelo `yolov8n.pt` deve estar presente em `models/yolov8n.pt`.
- Se houver problema com dependências do PyQt5 ou do PyTorch, confira a versão do Python e instale a versão correta de acordo com seu sistema.

## Problemas comuns e soluções

- `ModuleNotFoundError`: verifique se o ambiente virtual está ativado e se as dependências foram instaladas.
- `OSError` ao carregar o modelo: confirme se `models/yolov8n.pt` existe e está no caminho correto.
- Tela em branco ou sem overlays: confirme se o monitor correto foi selecionado e se a janela do overlay está aparecendo em modo transparente.

## Próximos passos sugeridos

- Adicionar suporte para outras classes de objeto além de cachorro
- Melhorar o filtro de confiança e ajuste de classes
- Adicionar logging e interface de configuração para seleção de monitor
- Implementar alertas ou ações baseadas na detecção
* Sistema de alertas (log, som, API)
* Otimização de performance (GPU / batch)
* Suporte a múltiplos monitores

---

##  Conceitos Utilizados

* Computer Vision
* Object Detection (YOLO)
* Multithreading
* Overlay gráfico em tempo real
* Arquitetura modular

---

##  Autor

Projeto desenvolvido para fins de estudo e evolução em visão computacional e engenharia de software.
