"""
transcricao/transcrever.py
Atividade 5 – Transcrição (Fase 1: basic-pitch)

Interface única e estável:

    def transcrever(caminho_audio: str) -> pretty_midi.PrettyMIDI

O resto do sistema chama só esta função. Na Fase 2, o interior será
substituído pelo pipeline DSP próprio (pYIN + CQT + onset + BPM) sem
que nenhum outro arquivo precise mudar.
"""

import pretty_midi
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH


# ── Parâmetros de transcrição (ajustáveis) ───────────────────────────────────

ONSET_THRESHOLD    = 0.5   # sensibilidade para detectar início de notas (0–1)
FRAME_THRESHOLD    = 0.3   # sensibilidade para sustentar notas (0–1)
MIN_NOTE_LENGTH    = 58    # duração mínima de nota em milissegundos


# ── Interface pública ────────────────────────────────────────────────────────

def transcrever(caminho_audio: str) -> pretty_midi.PrettyMIDI:
    """
    Recebe o caminho de um arquivo WAV e retorna um objeto PrettyMIDI
    com as notas detectadas pelo basic-pitch.

    Parâmetros usados:
      onset_threshold  – mais alto → menos notas falsas, mas pode perder notas reais
      frame_threshold  – mais baixo → notas mais longas
      minimum_note_length – filtra ruídos muito curtos
    """
    _, midi_data, _ = predict(
        audio_path            = caminho_audio,
        model_or_model_path   = ICASSP_2022_MODEL_PATH,
        onset_threshold       = ONSET_THRESHOLD,
        frame_threshold       = FRAME_THRESHOLD,
        minimum_note_length   = MIN_NOTE_LENGTH,
    )
    return midi_data


def contar_notas(midi: pretty_midi.PrettyMIDI) -> int:
    """Retorna o total de notas em todos os instrumentos."""
    return sum(len(inst.notes) for inst in midi.instruments)


def salvar_midi(midi: pretty_midi.PrettyMIDI, caminho_saida: str) -> None:
    """Salva o objeto PrettyMIDI em disco como arquivo .mid."""
    midi.write(caminho_saida)
