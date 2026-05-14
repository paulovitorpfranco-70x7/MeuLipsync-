const STATUS_LABELS = {
  pending: "Na fila",
  processing: "Processando",
  completed: "Concluído",
  failed: "Falhou",
};

export default function ProgressBar({ status, progress }) {
  if (status === "idle") {
    return null;
  }

  return (
    <section className="surface progress-panel" aria-live="polite">
      <div className="progress-panel__meta">
        <span>{STATUS_LABELS[status] || "Processando"}</span>
        <strong>{progress}%</strong>
      </div>
      <div className="progress-track">
        <div className="progress-fill" style={{ width: `${progress}%` }} />
      </div>
    </section>
  );
}
