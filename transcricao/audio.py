"""
transcricao/audio.py
Atividades 2 e 3 – Entrada de Áudio + Pré-processamento

Responsabilidades:
  - Carregar WAV ou MP3 como array numpy (+ sample rate)
  - Normalizar o volume
  - Remover silêncio das extremidades
  - Salvar o áudio processado em WAV temporário para o pipeline usar
"""

import os
import tempfile

import librosa
import numpy as np
import soundfile as sf


# ── Constantes ──────────────────────────────────────────────────────────────

SAMPLE_RATE_PADRAO = 22050   # Hz — padrão do librosa e do basic-pitch
SILENCIO_DB        = 20      # limiar de silêncio em dB para librosa.effects.trim
TAMANHO_MAX_MB     = 30      # limite de tamanho de arquivo aceito


# ── Funções públicas ─────────────────────────────────────────────────────────

def validar_arquivo(nome: str, tamanho_bytes: int) -> str | None:
    """
    Verifica se o arquivo é válido antes de processar.
    Retorna uma mensagem de erro (str) ou None se tudo estiver ok.
    """
    extensao = os.path.splitext(nome)[1].lower()
    if extensao not in (".wav", ".mp3"):
        return f"Formato '{extensao}' não suportado. Envie WAV ou MP3."

    tamanho_mb = tamanho_bytes / (1024 ** 2)
    if tamanho_mb > TAMANHO_MAX_MB:
        return f"Arquivo muito grande ({tamanho_mb:.1f} MB). Limite: {TAMANHO_MAX_MB} MB."

    return None


def carregar_audio(caminho: str, sr_alvo: int = SAMPLE_RATE_PADRAO) -> tuple[np.ndarray, int]:
    """
    Lê WAV ou MP3 e retorna (sinal, sample_rate).
    - Converte para mono automaticamente
    - Reamostra para sr_alvo se necessário
    """
    y, sr = librosa.load(caminho, sr=sr_alvo, mono=True)
    return y, sr


def normalizar(y: np.ndarray) -> np.ndarray:
    """
    Escala o sinal para que o pico seja exatamente 1.0.
    Evita clipping sem alterar a dinâmica relativa.
    """
    pico = np.max(np.abs(y))
    if pico > 0:
        y = y / pico
    return y


def remover_silencio(y: np.ndarray, sr: int, top_db: int = SILENCIO_DB) -> np.ndarray:
    """
    Corta silêncio no início e no fim do áudio.
    top_db: quanto (em dB) abaixo do pico é considerado silêncio.
    """
    y_trimmed, _ = librosa.effects.trim(y, top_db=top_db)
    return y_trimmed


def preprocessar(caminho_entrada: str) -> tuple[np.ndarray, int, str]:
    """
    Pipeline completo de pré-processamento.
    Retorna (sinal_processado, sample_rate, caminho_wav_temporario).

    O arquivo WAV temporário é necessário porque o basic-pitch (Passo 5)
    recebe um caminho de arquivo, não um array numpy.
    """
    y, sr = carregar_audio(caminho_entrada)
    y     = normalizar(y)
    y     = remover_silencio(y, sr)

    # Salva em WAV temporário para o resto do pipeline
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(tmp.name, y, sr)

    return y, sr, tmp.name
