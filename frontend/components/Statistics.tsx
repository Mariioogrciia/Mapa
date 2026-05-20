'use client'

import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { BarChart3, Zap, Users, Flame } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface StatsData {
  total_matches: number
  total_seasons: number
  training_matches: number
  test_matches: number
  explore_matches: number
  anomaly_threshold: number
  model_info: {
    name: string
    input_shape: number[]
    encoder_filters: number[]
    decoder_filters: number[]
    loss_function: string
    optimizer: string
  }
}

export default function Statistics() {
  const [stats, setStats] = useState<StatsData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/statistics`)
        setStats(response.data)
      } catch (error) {
        console.error('Error fetching statistics:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  if (loading) {
    return <div className="card-dark p-8 text-center text-gray-400">Cargando estadísticas...</div>
  }

  if (!stats) {
    return <div className="card-dark p-8 text-center text-red-400">Error al cargar estadísticas</div>
  }

  return (
    <div className="space-y-6">
      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card-dark p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm mb-2">Total de Partidos</p>
              <p className="text-3xl font-bold text-red-400">{stats.total_matches}</p>
            </div>
            <Zap className="text-red-500/50" size={32} />
          </div>
        </div>

        <div className="card-dark p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm mb-2">Temporadas</p>
              <p className="text-3xl font-bold text-yellow-400">{stats.total_seasons}</p>
            </div>
            <BarChart3 className="text-yellow-500/50" size={32} />
          </div>
        </div>

        <div className="card-dark p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm mb-2">Entrenamiento</p>
              <p className="text-3xl font-bold text-blue-400">{stats.training_matches}</p>
              <p className="text-xs text-gray-500 mt-1">2007-2017</p>
            </div>
            <Users className="text-blue-500/50" size={32} />
          </div>
        </div>

        <div className="card-dark p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm mb-2">Exploración</p>
              <p className="text-3xl font-bold text-red-400">{stats.explore_matches}</p>
              <p className="text-xs text-gray-500 mt-1">2019-2021</p>
            </div>
            <Flame className="text-red-500/50" size={32} />
          </div>
        </div>
      </div>

      {/* Dataset Split */}
      <div className="card-dark p-6">
        <h3 className="text-xl font-bold mb-4">Distribución del Dataset</h3>
        <div className="space-y-4">
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm font-semibold text-gray-300">Entrenamiento</span>
              <span className="text-sm text-gray-400">{stats.training_matches} partidos</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
              <div
                className="h-full bg-blue-500"
                style={{
                  width: `${(stats.training_matches / stats.total_matches) * 100}%`,
                }}
              />
            </div>
          </div>

          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm font-semibold text-gray-300">Test</span>
              <span className="text-sm text-gray-400">{stats.test_matches} partidos</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
              <div
                className="h-full bg-yellow-500"
                style={{
                  width: `${(stats.test_matches / stats.total_matches) * 100}%`,
                }}
              />
            </div>
          </div>

          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm font-semibold text-gray-300">Exploración</span>
              <span className="text-sm text-gray-400">{stats.explore_matches} partidos</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
              <div
                className="h-full bg-red-500"
                style={{
                  width: `${(stats.explore_matches / stats.total_matches) * 100}%`,
                }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Model Architecture */}
      <div className="card-dark p-6">
        <h3 className="text-xl font-bold mb-4">Arquitectura del Modelo</h3>
        <div className="space-y-3 text-sm">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-gray-400 mb-1">Nombre</p>
              <p className="text-gray-100 font-semibold">{stats.model_info.name}</p>
            </div>
            <div>
              <p className="text-gray-400 mb-1">Entrada</p>
              <p className="font-mono text-gray-100">{stats.model_info.input_shape.join(' × ')}</p>
            </div>
            <div>
              <p className="text-gray-400 mb-1">Encoder Filters</p>
              <p className="font-mono text-gray-100">{stats.model_info.encoder_filters.join(' → ')}</p>
            </div>
            <div>
              <p className="text-gray-400 mb-1">Decoder Filters</p>
              <p className="font-mono text-gray-100">{stats.model_info.decoder_filters.join(' → ')}</p>
            </div>
            <div>
              <p className="text-gray-400 mb-1">Loss Function</p>
              <p className="text-gray-100 font-semibold">{stats.model_info.loss_function}</p>
            </div>
            <div>
              <p className="text-gray-400 mb-1">Optimizer</p>
              <p className="text-gray-100 font-semibold">{stats.model_info.optimizer}</p>
            </div>
          </div>

          <div className="pt-4 border-t border-gray-700 mt-4">
            <p className="text-gray-400 mb-2">Umbral de Anomalía (Percentil 95%)</p>
            <p className="text-lg font-mono text-red-400">{stats.anomaly_threshold.toFixed(6)}</p>
            <p className="text-xs text-gray-500 mt-1">
              Partidos con MSE por encima de este valor se consideran anómalos
            </p>
          </div>
        </div>
      </div>

      {/* How it Works */}
      <div className="card-dark p-6">
        <h3 className="text-xl font-bold mb-4">¿Cómo funciona?</h3>
        <div className="space-y-3 text-sm text-gray-300">
          <div className="flex gap-3">
            <div className="text-red-500 font-bold flex-shrink-0">1.</div>
            <p>Se construyen mapas de calor 64×64 con np.histogram2d desde las coordenadas de pases (x_inicio, y_inicio)</p>
          </div>
          <div className="flex gap-3">
            <div className="text-red-500 font-bold flex-shrink-0">2.</div>
            <p>Los mapas se normalizan con raíz cuadrada y percentil 99 del entrenamiento (p99 = 1.414)</p>
          </div>
          <div className="flex gap-3">
            <div className="text-red-500 font-bold flex-shrink-0">3.</div>
            <p>El autoencoder convolucional aprende a reconstruir la estructura táctica histórica</p>
          </div>
          <div className="flex gap-3">
            <div className="text-red-500 font-bold flex-shrink-0">4.</div>
            <p>Se calcula el MSE (error cuadrático medio) de reconstrucción por partido</p>
          </div>
          <div className="flex gap-3">
            <div className="text-red-500 font-bold flex-shrink-0">5.</div>
            <p>Partidos con MSE por encima del umbral 95% se marcan como anómalos</p>
          </div>
        </div>
      </div>
    </div>
  )
}
