# LipSync Studio

Ferramenta local para gerar vídeos verticais de lip sync a partir de uma imagem estática e um arquivo de áudio. A primeira versão usa um placeholder com FFmpeg: imagem + áudio, chunking, concatenação e exportação final em MP4 1080x1920.

## Pré-requisitos

- Node.js 18+
- Python 3.10+
- FFmpeg e FFprobe instalados e disponíveis no `PATH`

## Instalação

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

No PowerShell do Windows, se `npm` estiver bloqueado por política de execução, use:

```bash
npm.cmd install
```

## Execução

### Terminal 1 - Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

No PowerShell do Windows:

```bash
npm.cmd run dev
```

Acesse `http://localhost:3000`.

## API

- `GET /api/health` - health check
- `POST /api/generate` - recebe `image`, `audio`, `duration` e `style`
- `GET /api/status/{job_id}` - retorna progresso do job
- `GET /api/download/{job_id}` - baixa o MP4 final

## Fluxo

1. O frontend envia imagem, áudio, duração e estilo.
2. O backend salva os arquivos em `uploads/`.
3. O áudio é cortado na duração escolhida.
4. Áudios maiores que 10s são divididos em chunks.
5. Cada chunk gera um clipe com imagem estática e áudio.
6. Os clipes são concatenados.
7. O vídeo final é convertido para 1080x1920, H.264 e AAC.
8. O resultado fica em `outputs/`.

## Integração futura com SadTalker

O ponto de troca fica em `backend/services/lipsync_engine.py`, na função `generate_lipsync_clip()`. Hoje ela chama FFmpeg para criar o placeholder. Para integrar SadTalker, substitua o corpo da função por uma chamada ao script de inferência, mantendo a assinatura.

## Estrutura

```text
lipsync/
├── backend/
│   ├── main.py
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── utils/
├── frontend/
│   └── src/
│       ├── app/
│       ├── components/
│       └── lib/
├── uploads/
├── outputs/
└── temp/
```

## Observações

- O status dos jobs fica em memória. Reiniciar o backend apaga o registro dos jobs.
- `uploads/`, `outputs/` e `temp/` são artefatos locais e não devem ser versionados.
- Se FFmpeg ou FFprobe não estiverem no `PATH`, a geração falhará com mensagem no frontend.

## Licença

MIT
