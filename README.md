MTP – Transcrição Musical Automática

Projeto ITA 2026 — Converte áudio (WAV/MP3) em MIDI e partitura.

## Estrutura do projeto

```
mtp-transcricao/
├── app.py                  # Ponto de entrada (Streamlit)
├── transcricao/
│   ├── __init__.py
│   ├── audio.py            # Atividades 2 e 3 — Entrada + Pré-processamento
│   ├── visualizacao.py     # Atividade 4  — Forma de onda + Espectrograma
│   └── transcrever.py      # Atividade 5  — Transcrição (Fase 1: basic-pitch)
├── exports/                # Arquivos .mid e .csv gerados (ignorado pelo git)
├── requirements.txt
└── .gitignore
```

## Setup (fazer uma vez por integrante)

### 1. Clonar o repositório
```bash
git clone https://github.com/<seu-usuario>/mtp-transcricao.git
cd mtp-transcricao
```

### 2. Criar ambiente virtual
```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

> ⚠️ O `basic-pitch` instala TensorFlow como dependência.
> Se você tiver GPU e quiser usá-la, instale o `tensorflow-gpu` manualmente depois.

### 4. Rodar o app
```bash
streamlit run app.py
```

O browser abre automaticamente em `http://localhost:8501`.

---

## Fluxo atual (Fase 1 – MVP)

```
Upload WAV/MP3
     ↓
Pré-processamento (normalização + remoção de silêncio)
     ↓
Visualização (forma de onda + espectrograma)
     ↓
Transcrição com basic-pitch  →  PrettyMIDI
     ↓
Download do arquivo .mid
```

## Fase 2 – Pipeline DSP próprio (planejado)

A função `transcrever()` em `transcricao/transcrever.py` será substituída por um
pipeline interno usando `librosa` (CQT → pYIN → onset detection → quantização rítmica).
O resto do sistema não muda.

---

## Integrantes

| Nome            | Responsabilidade principal          |
|-----------------|-------------------------------------|
| Rafael / Pedro  | Setup, integração e testes          |
| Victor          | Entrada de áudio e exportação       |
| Henrique D.     | Pré-processamento                   |
| João Pedro      | Visualização do áudio               |
| Artur / Gabriel | Transcrição (basic-pitch → DSP)     |
| Henrique P.     | Pós-processamento MIDI              |
| Paulo           | Piano roll e apresentação           |
