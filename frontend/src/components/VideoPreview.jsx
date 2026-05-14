import { getDownloadUrl, getVideoStreamUrl } from "@/lib/api";

export default function VideoPreview({ jobId, videoUrl }) {
  if (!jobId || !videoUrl) {
    return null;
  }

  return (
    <section className="surface preview-panel">
      <div className="preview-frame">
        <video src={getVideoStreamUrl(videoUrl)} controls playsInline />
      </div>
      <a className="download-button" href={getDownloadUrl(jobId)}>
        Baixar MP4
      </a>
    </section>
  );
}
