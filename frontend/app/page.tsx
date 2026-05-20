'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import { Zap, TrendingUp, AlertTriangle, BarChart3 } from 'lucide-react'
import MatchSelector from '@/components/MatchSelector'
import HeatmapViewer from '@/components/HeatmapViewer'
import AnomalyScore from '@/components/AnomalyScore'
import TopAnomalies from '@/components/TopAnomalies'
import Header from '@/components/Header'
import Statistics from '@/components/Statistics'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface PredictionResult {
  match_id: number
  season_id: number
  season_name: string
  mse: number
  threshold: number
  is_anomalous: boolean
  anomaly_score: number
  original_image: string
  reconstructed_image: string
  comparison_image: string
  interpretation: {
    mse_level: string
    message: string
  }
}

export default function Home() {
  const [selectedMatchId, setSelectedMatchId] = useState<number | null>(null)
  const [prediction, setPrediction] = useState<PredictionResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'analysis' | 'anomalies' | 'stats'>('analysis')

  const handleMatchSelect = async (matchId: number) => {
    setSelectedMatchId(matchId)
    setLoading(true)
    setError(null)

    try {
      const response = await axios.post(`${API_URL}/api/predict`, null, {
        params: { match_id: matchId },
      })
      setPrediction(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al procesar el partido')
      setPrediction(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#0f1419' }}>
      <Header />

      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Tabs */}
        <div className="flex gap-2 mb-8 border-b border-red-900/30">
          <button
            onClick={() => setActiveTab('analysis')}
            className={`px-6 py-3 font-semibold transition-all ${
              activeTab === 'analysis'
                ? 'text-red-500 border-b-2 border-red-500'
                : 'text-gray-400 hover:text-gray-300'
            }`}
          >
            <div className="flex items-center gap-2">
              <Zap size={18} />
              Análisis de Partido
            </div>
          </button>
          <button
            onClick={() => setActiveTab('anomalies')}
            className={`px-6 py-3 font-semibold transition-all ${
              activeTab === 'anomalies'
                ? 'text-red-500 border-b-2 border-red-500'
                : 'text-gray-400 hover:text-gray-300'
            }`}
          >
            <div className="flex items-center gap-2">
              <AlertTriangle size={18} />
              Top Anomalías
            </div>
          </button>
          <button
            onClick={() => setActiveTab('stats')}
            className={`px-6 py-3 font-semibold transition-all ${
              activeTab === 'stats'
                ? 'text-red-500 border-b-2 border-red-500'
                : 'text-gray-400 hover:text-gray-300'
            }`}
          >
            <div className="flex items-center gap-2">
              <BarChart3 size={18} />
              Estadísticas
            </div>
          </button>
        </div>

        {/* Tab Content */}
        {activeTab === 'analysis' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left: Match Selector */}
            <div className="lg:col-span-1">
              <MatchSelector onSelectMatch={handleMatchSelect} />
            </div>

            {/* Right: Results */}
            <div className="lg:col-span-2">
              {loading && (
                <div className="card-dark p-8 flex items-center justify-center">
                  <div className="text-center">
                    <div className="animate-spin mb-4">
                      <Zap className="text-red-500" size={32} />
                    </div>
                    <p className="text-gray-400">Procesando análisis...</p>
                  </div>
                </div>
              )}

              {error && (
                <div className="card-dark p-6 border-red-500/50 bg-red-500/10">
                  <p className="text-red-400">{error}</p>
                </div>
              )}

              {prediction && !loading && (
                <div className="space-y-6">
                  <AnomalyScore prediction={prediction} />
                  <HeatmapViewer prediction={prediction} />
                </div>
              )}

              {!prediction && !loading && !error && (
                <div className="card-dark p-12 text-center">
                  <TrendingUp className="mx-auto text-gray-600 mb-4" size={48} />
                  <p className="text-gray-400">Selecciona un partido para análisis</p>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'anomalies' && <TopAnomalies />}

        {activeTab === 'stats' && <Statistics />}
      </main>
    </div>
  )
}
