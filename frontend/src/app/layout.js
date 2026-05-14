import "./globals.css";

export const metadata = {
  title: "LipSync Studio",
  description: "Gere vídeos verticais de lip sync a partir de imagem e áudio.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
