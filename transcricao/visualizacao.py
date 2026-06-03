"""
transcricao/visualizacao.py
Atividade 4 – Visualização do Áudio

Gera duas figuras matplotlib:
  - Forma de onda  (amplitude × tempo)
  - Espectrograma  (frequência × tempo, escala dB)

Ambas são retornadas como objetos Figure para o Streamlit exibir com st.pyplot().
"""

import librosa
import librosa.display
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


# Paleta de cores consistente com o visual do app
COR_ONDA      = "#2E75B6"
COR_ESPECTRO  = "magma"   # colormap perceptualmente uniforme


def plotar_forma_de_onda(y: np.ndarray, sr: int) -> plt.Figure:
    """
    Plota amplitude do sinal ao longo do tempo.
    """
    fig, ax = plt.subplots(figsize=(9, 2.5))
    fig.patch.set_facecolor("#0E1117")   # fundo escuro (tema Streamlit)
    ax.set_facecolor("#0E1117")

    librosa.display.waveshow(y, sr=sr, ax=ax, color=COR_ONDA, alpha=0.85)

    ax.set_title("Forma de onda", color="white", fontsize=11, pad=8)
    ax.set_xlabel("Tempo (s)", color="#AAAAAA", fontsize=9)
    ax.set_ylabel("Amplitude", color="#AAAAAA", fontsize=9)
    ax.tick_params(colors="#AAAAAA")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333333")

    fig.tight_layout()
    return fig


def plotar_espectrograma(y: np.ndarray, sr: int) -> plt.Figure:
    """
    Plota espectrograma de curto prazo (STFT) em escala logarítmica de dB.
    """
    fig, ax = plt.subplots(figsize=(9, 3))
    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    img = librosa.display.specshow(
        D, sr=sr,
        x_axis="time", y_axis="hz",
        ax=ax, cmap=COR_ESPECTRO
    )

    cbar = fig.colorbar(img, ax=ax, format="%+2.0f dB", pad=0.01)
    cbar.ax.yaxis.set_tick_params(color="#AAAAAA")
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="#AAAAAA", fontsize=8)

    ax.set_title("Espectrograma", color="white", fontsize=11, pad=8)
    ax.set_xlabel("Tempo (s)", color="#AAAAAA", fontsize=9)
    ax.set_ylabel("Frequência (Hz)", color="#AAAAAA", fontsize=9)
    ax.tick_params(colors="#AAAAAA")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    for spine in ax.spines.values():
        spine.set_edgecolor("#333333")

    fig.tight_layout()
    return fig
