"use client";

import { useEffect, useMemo, useState } from "react";

import ConfigPanel from "@/components/ConfigPanel";
import FileUpload from "@/components/FileUpload";
import ProgressBar from "@/components/ProgressBar";
import VideoPreview from "@/components/VideoPreview";
import { generateVideo, getJobStatus } from "@/lib/api";

export default function Home() {
  const [imageFile, setImageFile] = useState(null);
  const [audioFile, setAudioFile] = useState(null);
  const [duration, setDuration] = useState(15);
  const [style, setStyle] = useState("natural");
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState("idle");
  const [progress, setProgress] = useState(0);
  const [videoUrl, setVideoUrl] = useState(null);
  const [error, setError] = useState(null);

  const canGenerate = useMemo(
    () => imageFile && audioFile && !["pending", "processing"].includes(status),
    [audioFile, imageFile, status],
  );

  useEffect(() => {
    if (!jobId || !["pending", "processing"].includes(status)) {
      return undefined;
    }

    const interval = window.setInterval(async () => {
      try {
        const nextStatus = await getJobStatus(jobId);
        setStatus(nextStatus.status);
        setProgress(nextStatus.progress);
        setVideoUrl(nextStatus.video_url);
        setError(nextStatus.error);
      } catch (nextError) {
        setStatus("failed");
        setError(nextError.message);
      }
    }, 2000);

    return () => window.clearInterval(interval);
  }, [jobId, status]);

  async function handleGenerate() {
    if (!imageFile || !audioFile) {
      return;
    }

    setError(null);
    setVideoUrl(null);
    setProgress(0);
    setStatus("pending");

    try {
      const response = await generateVideo(imageFile, audioFile, duration, style);
      setJobId(response.job_id);
      setStatus(response.status);
    } catch (nextError) {
      setStatus("failed");
      setError(nextError.message);
    }
  }

  return (
    <main className="app-shell">
      <header className="app-header">
        <p className="eyebrow">Local video workflow</p>
        <h1>LipSync Studio</h1>
        <p className="app-header__copy">
          Gere um MP4 vertical a partir de uma imagem e um áudio.
        </p>
      </header>

      <section className="workspace">
        <div className="upload-grid">
          <FileUpload
            accept="image/*"
            label="Imagem"
            marker="IMG"
            file={imageFile}
            onFileSelect={setImageFile}
          />
          <FileUpload
            accept="audio/*"
            label="Áudio"
            marker="AUD"
            file={audioFile}
            onFileSelect={setAudioFile}
          />
        </div>

        <ConfigPanel
          duration={duration}
          style={style}
          onDurationChange={setDuration}
          onStyleChange={setStyle}
        />

        <button
          className="generate-button"
          type="button"
          disabled={!canGenerate}
          onClick={handleGenerate}
        >
          {["pending", "processing"].includes(status) ? "Gerando..." : "Gerar vídeo"}
        </button>

        <ProgressBar status={status} progress={progress} />

        {error && <p className="error-message">{error}</p>}

        <VideoPreview jobId={jobId} videoUrl={videoUrl} />
      </section>
    </main>
  );
}
