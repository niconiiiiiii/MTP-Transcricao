"""
app.py – Ponto de entrada do MTP
Transcrição Musical Automática: Áudio → MIDI

Execução:
    streamlit run app.py
"""

import os
import tempfile

import streamlit as st

from transcricao.audio import validar_arquivo, preprocessar
from transcricao.visualizacao import plotar_forma_de_onda, plotar_espectrograma
from transcricao.transcrever import transcrever, contar_notas, salvar_midi


# ── Configuração da página ───────────────────────────────────────────────────

st.set_page_config(
    page_title="MTP – Transcrição Musical",
    page_icon="🎵",
    layout="wide",
)

st.title("🎵 MTP – Transcrição Musical Automática")
st.caption("Áudio → MIDI  |  Fase 1 — MVP com basic-pitch (Spotify)")
st.divider()


# ── Passo 2: Entrada de Áudio ────────────────────────────────────────────────

st.subheader("① Envie seu áudio")
arquivo = st.file_uploader(
    "Arquivo WAV ou MP3 (máx. 30 MB)",
    type=["wav", "mp3"],
    help="Funciona melhor com áudio monofônico e instrumentos melódicos.",
)

if arquivo is None:
    st.info("Aguardando upload de um arquivo de áudio para começar.")
    st.stop()

# Validação
erro = validar_arquivo(arquivo.name, arquivo.size)
if erro:
    st.error(erro)
    st.stop()

st.audio(arquivo)

# Salva o arquivo original em disco temporariamente
extensao = os.path.splitext(arquivo.name)[1].lower()
with tempfile.NamedTemporaryFile(delete=False, suffix=extensao) as tmp_original:
    tmp_original.write(arquivo.read())
    caminho_original = tmp_original.name


# ── Passo 3: Pré-processamento ───────────────────────────────────────────────

st.divider()
st.subheader("② Pré-processamento")

with st.spinner("Carregando, normalizando e removendo silêncio..."):
    y, sr, caminho_processado = preprocessar(caminho_original)

duracao   = len(y) / sr
col1, col2, col3 = st.columns(3)
col1.metric("Sample Rate",  f"{sr:,} Hz")
col2.metric("Duração",      f"{duracao:.2f} s")
col3.metric("Amostras",     f"{len(y):,}")

st.success("✅ Áudio normalizado e silêncio removido.")


# ── Passo 4: Visualização ────────────────────────────────────────────────────

st.divider()
st.subheader("③ Visualização do Áudio")

col_onda, col_spec = st.columns(2)

with col_onda:
    st.caption("Forma de onda")
    with st.spinner("Gerando forma de onda..."):
        fig_onda = plotar_forma_de_onda(y, sr)
    st.pyplot(fig_onda, use_container_width=True)

with col_spec:
    st.caption("Espectrograma")
    with st.spinner("Gerando espectrograma..."):
        fig_spec = plotar_espectrograma(y, sr)
    st.pyplot(fig_spec, use_container_width=True)


# ── Passo 5: Transcrição ─────────────────────────────────────────────────────

st.divider()
st.subheader("④ Transcrição para MIDI")

st.markdown(
    "O **basic-pitch** (Spotify) detecta as notas do áudio e gera um arquivo `.mid`. "
    "Funciona melhor com instrumentos melódicos (violão, piano, flauta, voz…)."
)

if st.button("🎼 Transcrever para MIDI", type="primary", use_container_width=True):
    with st.spinner("Transcrevendo... (pode levar alguns segundos na primeira vez)"):
        midi = transcrever(caminho_processado)

    n_notas = contar_notas(midi)

    # Salva o MIDI em exports/
    os.makedirs("exports", exist_ok=True)
    nome_base   = os.path.splitext(arquivo.name)[0]
    caminho_mid = os.path.join("exports", f"{nome_base}.mid")
    salvar_midi(midi, caminho_mid)

    st.success(f"✅ Transcrição concluída! **{n_notas} notas** detectadas.")

    col_dl1, col_dl2 = st.columns(2)

    with open(caminho_mid, "rb") as f:
        col_dl1.download_button(
            label     = "⬇️ Baixar arquivo .mid",
            data      = f,
            file_name = f"{nome_base}.mid",
            mime      = "audio/midi",
        )

    # Resumo por instrumento
    with st.expander("Ver detalhes da transcrição"):
        for i, inst in enumerate(midi.instruments):
            nome_inst = inst.name if inst.name else f"Instrumento {i+1}"
            st.write(f"**{nome_inst}**: {len(inst.notes)} notas")

    st.caption(
        "💡 Próximos passos: pós-processamento MIDI (filtrar notas curtas), "
        "visualização no piano roll e exportação CSV."
    )


# ── Rodapé ───────────────────────────────────────────────────────────────────

st.divider()
st.caption("MTP – Projeto ITA 2026  |  Fase 1 (basic-pitch)  →  Fase 2 (pipeline DSP próprio)")
