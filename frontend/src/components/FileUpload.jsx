"use client";

const ACCEPTED_EXTENSIONS = {
  "image/*": ["png", "jpg", "jpeg"],
  "audio/*": ["mp3", "wav"],
};

function getAllowedExtensions(accept) {
  return ACCEPTED_EXTENSIONS[accept] || accept.replaceAll(".", "").split(",");
}

function isAllowed(file, accept) {
  const extension = file.name.split(".").pop()?.toLowerCase();
  return getAllowedExtensions(accept).includes(extension);
}

export default function FileUpload({ accept, label, marker, onFileSelect, file }) {
  function handleFile(nextFile) {
    if (!nextFile) {
      return;
    }

    if (!isAllowed(nextFile, accept)) {
      window.alert(`Arquivo inválido para ${label}.`);
      return;
    }

    onFileSelect(nextFile);
  }

  function handleDrop(event) {
    event.preventDefault();
    handleFile(event.dataTransfer.files?.[0]);
  }

  return (
    <label
      className={`upload-zone ${file ? "upload-zone--filled" : ""}`}
      onDragOver={(event) => event.preventDefault()}
      onDrop={handleDrop}
    >
      <input
        type="file"
        accept={accept}
        onChange={(event) => handleFile(event.target.files?.[0])}
      />
      <span className="upload-zone__marker">{marker}</span>
      <span className="upload-zone__label">{label}</span>
      <span className="upload-zone__hint">
        {file ? file.name : "Arraste ou selecione um arquivo"}
      </span>
    </label>
  );
}
