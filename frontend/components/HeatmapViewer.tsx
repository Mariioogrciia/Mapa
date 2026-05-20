import React from 'react'
import { Eye, Copy } from 'lucide-react'

interface HeatmapViewerProps {
  prediction: {
    original_image: string
    reconstructed_image: string
    comparison_image: string
  }
}

export default function HeatmapViewer({ prediction }: HeatmapViewerProps) {
  const [activeView, setActiveView] = React.useState<'comparison' | 'original' | 'reconstructed'>('comparison')

  const handleCopy = (imageSrc: string) => {
    const link = document.createElement('a')
    link.href = imageSrc
    link.download = `heatmap-${Date.now()}.png`
    link.click()
  }

  return (
    <div className="card-dark p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold flex items-center gap-2">
          <Eye size={20} />
          Heatmap Analysis
        </h3>
        <div className="flex gap-2">
          <button
            onClick={() => setActiveView('comparison')}
            className={`px-3 py-1 rounded text-sm font-semibold transition-all ${
              activeView === 'comparison'
                ? 'bg-red-600 text-white'
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
            }`}
          >
            Comparación
          </button>
          <button
            onClick={() => setActiveView('original')}
            className={`px-3 py-1 rounded text-sm font-semibold transition-all ${
              activeView === 'original'
                ? 'bg-red-600 text-white'
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
            }`}
          >
            Original
          </button>
          <button
            onClick={() => setActiveView('reconstructed')}
            className={`px-3 py-1 rounded text-sm font-semibold transition-all ${
              activeView === 'reconstructed'
                ? 'bg-red-600 text-white'
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
            }`}
          >
            Reconstruido
          </button>
        </div>
      </div>

      {/* Image Display */}
      <div className="relative bg-black/50 rounded-lg overflow-hidden aspect-video flex items-center justify-center mb-4">
        <img
          src={
            activeView === 'comparison'
              ? prediction.comparison_image
              : activeView === 'original'
              ? prediction.original_image
              : prediction.reconstructed_image
          }
          alt={activeView}
          className="w-full h-full object-contain"
        />
      </div>

      {/* Download Button */}
      <div className="flex justify-end gap-2">
        <button
          onClick={() =>
            handleCopy(
              activeView === 'comparison'
                ? prediction.comparison_image
                : activeView === 'original'
                ? prediction.original_image
                : prediction.reconstructed_image
            )
          }
          className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-semibold transition-all"
        >
          <Copy size={16} />
          Descargar
        </button>
      </div>

      {/* Info */}
      <div className="mt-4 p-4 bg-black/30 rounded-lg border border-red-900/20">
        <p className="text-sm text-gray-400 mb-2">
          {activeView === 'comparison'
            ? 'Comparación lado a lado: Original vs Reconstruido'
            : activeView === 'original'
            ? 'Mapa de calor original de pases del partido'
            : 'Reconstrucción del autoencoder basada en el patrón histórico'}
        </p>
        <p className="text-xs text-gray-500">
          Los píxeles más brillantes indican mayor concentración de pases en esa zona del campo
        </p>
      </div>
    </div>
  )
}
