export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

async function parseResponse(response) {
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const message =
      typeof payload === "object" && payload?.detail
        ? payload.detail
        : "Não foi possível concluir a requisição.";
    throw new Error(message);
  }

  return payload;
}

export async function generateVideo(imageFile, audioFile, duration, style) {
  const formData = new FormData();
  formData.append("image", imageFile);
  formData.append("audio", audioFile);
  formData.append("duration", String(duration));
  formData.append("style", style);

  const response = await fetch(`${API_BASE}/api/generate`, {
    method: "POST",
    body: formData,
  });

  return parseResponse(response);
}

export async function getJobStatus(jobId) {
  const response = await fetch(`${API_BASE}/api/status/${jobId}`, {
    cache: "no-store",
  });

  return parseResponse(response);
}

export function getDownloadUrl(jobId) {
  return `${API_BASE}/api/download/${jobId}`;
}

export function getVideoStreamUrl(videoUrl) {
  if (!videoUrl) {
    return "";
  }

  if (videoUrl.startsWith("http")) {
    return videoUrl;
  }

  return `${API_BASE}${videoUrl}`;
}
