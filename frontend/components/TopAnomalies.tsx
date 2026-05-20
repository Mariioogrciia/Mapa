'use client'

import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { TrendingUp, Flame } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Anomaly {
  match_id: number
  season_id: number
  season_name: string
  mse: number
  is_anomalous: boolean
  anomaly_score: number
}

export default function TopAnomalies() {
  const [anomalies, setAnomalies] = useState<Anomaly[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchAnomalies = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/top-anomalies?limit=15`)
        setAnomalies(response.data.anomalies)
      } catch (error) {
        console.error('Error fetching anomalies:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchAnomalies()
  }, [])

  return (
    <div className="space-y-6">
      <div className="card-dark p-6">
        <h2 className="text-2xl font-bold flex items-center gap-2 mb-6">
          <Flame className="text-red-500" size={28} />
          Top 15 Anomalías Detectadas
        </h2>

        {loading ? (
          <div className="text-center py-8 text-gray-400">Cargando datos...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-red-900/30">
                  <th className="text-left px-4 py-3 text-sm font-semibold text-gray-300">Ranking</th>
                  <th className="text-left px-4 py-3 text-sm font-semibold text-gray-300">Match ID</th>
                  <th className="text-left px-4 py-3 text-sm font-semibold text-gray-300">Temporada</th>
                  <th className="text-left px-4 py-3 text-sm font-semibold text-gray-300">MSE</th>
                  <th className="text-center px-4 py-3 text-sm font-semibold text-gray-300">Score</th>
                  <th className="text-center px-4 py-3 text-sm font-semibold text-gray-300">Estado</th>
                </tr>
              </thead>
              <tbody>
                {anomalies.map((anomaly, index) => (
                  <tr
                    key={anomaly.match_id}
                    className="border-b border-gray-800/30 hover:bg-red-900/10 transition-all"
                  >
                    <td className="px-4 py-3">
                      <span className="inline-flex items-center justify-center w-6 h-6 bg-red-600 text-white rounded-full text-xs font-bold">
                        {index + 1}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-mono text-sm text-gray-200">{anomaly.match_id}</td>
                    <td className="px-4 py-3 text-sm text-gray-300">{anomaly.season_name}</td>
                    <td className="px-4 py-3 font-mono text-sm text-gray-300">{anomaly.mse.toFixed(6)}</td>
                    <td className="px-4 py-3 text-center">
                      <div className="flex items-center justify-center">
                        <div className="text-right">
                          <p className="font-bold text-red-400">{anomaly.anomaly_score.toFixed(0)}%</p>
                          <div className="w-24 h-2 bg-gray-700 rounded-full overflow-hidden mt-1">
                            <div
                              className="h-full bg-red-500"
                              style={{ width: `${Math.min(anomaly.anomaly_score, 100)}%` }}
                            />
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-center">
                      {anomaly.is_anomalous ? (
                        <span className="inline-block px-2 py-1 bg-red-900/50 text-red-300 rounded text-xs font-semibold animate-pulse">
                          ⚠️ ANÓMALO
                        </span>
                      ) : (
                        <span className="inline-block px-2 py-1 bg-green-900/50 text-green-300 rounded text-xs font-semibold">
                          ✓ Normal
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Legend */}
      <div className="card-dark p-6">
        <h3 className="font-bold mb-3">Interpretación</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <p className="text-gray-400 mb-1">📊 MSE</p>
            <p className="text-gray-300">Error de reconstrucción del autoencoder</p>
          </div>
          <div>
            <p className="text-gray-400 mb-1">🔴 Score</p>
            <p className="text-gray-300">Probabilidad normalizada de anomalía (0-100%)</p>
          </div>
          <div>
            <p className="text-gray-400 mb-1">⚙️ Estado</p>
            <p className="text-gray-300">Clasificación respecto al umbral 95%</p>
          </div>
        </div>
      </div>
    </div>
  )
}
