import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Barcelona Tactical Audit',
  description: 'Advanced tactical analysis with autoencoder anomaly detection',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  )
}
