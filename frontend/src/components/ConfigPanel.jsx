"use client";

const DURATIONS = [8, 15, 30, 60];
const STYLES = [
  { value: "natural", label: "Natural" },
  { value: "emocional", label: "Emocional" },
  { value: "intenso", label: "Intenso" },
];

export default function ConfigPanel({ duration, style, onDurationChange, onStyleChange }) {
  return (
    <section className="surface config-panel" aria-label="Configuração">
      <div className="control-group">
        <span className="control-group__label">Duração</span>
        <div className="segmented-control">
          {DURATIONS.map((item) => (
            <button
              className={item === duration ? "is-active" : ""}
              type="button"
              key={item}
              onClick={() => onDurationChange(item)}
            >
              {item}s
            </button>
          ))}
        </div>
      </div>

      <div className="control-group">
        <span className="control-group__label">Estilo</span>
        <div className="segmented-control">
          {STYLES.map((item) => (
            <button
              className={item.value === style ? "is-active" : ""}
              type="button"
              key={item.value}
              onClick={() => onStyleChange(item.value)}
            >
              {item.label}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
