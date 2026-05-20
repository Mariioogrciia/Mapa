import React from 'react'
import { AlertTriangle } from 'lucide-react'

export default function Header() {
  return (
    <div className="bg-gradient-to-r from-red-950/80 via-red-900/60 to-red-950/80 border-b border-red-800/50 backdrop-blur-sm">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="flex items-center gap-4 mb-2">
          <AlertTriangle className="text-red-400" size={32} />
          <div>
            <h1 className="text-4xl font-black text-red-50">Barcelona Tactical Audit</h1>
            <p className="text-red-200 text-sm mt-1">Advanced Autoencoder Anomaly Detection System</p>
          </div>
        </div>
        <div className="mt-4 p-3 bg-red-900/30 border border-red-500/30 rounded-lg">
          <p className="text-red-100 text-sm">
            🔴 Detección automática de desviaciones tácticas usando autoencoder convolucional
          </p>
        </div>
      </div>
    </div>
  )
}
