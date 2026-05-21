"use client"

import React, { useEffect, useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Explanation() {
  const [debug, setDebug] = useState<any | null>(null)
  const [loadingDebug, setLoadingDebug] = useState(false)
  const [errorDebug, setErrorDebug] = useState<string | null>(null)

  const [matchId, setMatchId] = useState<number | ''>('')
  const [prediction, setPrediction] = useState<any | null>(null)
  const [loadingPred, setLoadingPred] = useState(false)
  const [errorPred, setErrorPred] = useState<string | null>(null)

  useEffect(() => {
    const fetchDebug = async () => {
      setLoadingDebug(true)
      try {
        const res = await axios.get(`${API_URL}/api/debug_model`)
        setDebug(res.data)
      } catch (err: any) {
        setErrorDebug(err?.response?.data?.detail || 'No se pudo obtener debug_model')
      } finally {
        setLoadingDebug(false)
      }
    }
    fetchDebug()
  }, [])

  const runPredict = async () => {
    if (!matchId) return
    setLoadingPred(true)
    setErrorPred(null)
    setPrediction(null)
    try {
      const res = await axios.post(`${API_URL}/api/predict`, null, { params: { match_id: matchId } })
      setPrediction(res.data)
    } catch (err: any) {
      setErrorPred(err?.response?.data?.detail || 'Error en predict')
    } finally {
      setLoadingPred(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="card-dark p-6 rounded-lg">
        <h2 className="text-2xl font-semibold text-red-100 mb-2">Información del modelo</h2>

        {loadingDebug && <p className="text-gray-400">Cargando datos del modelo...</p>}
        {errorDebug && <p className="text-red-400">{errorDebug}</p>}

        {debug && (
          <div className="text-gray-300">
            <p><strong>p99 usado:</strong> {String(debug.p99_used ?? debug.p99 ?? 'desconocido')}</p>
            <p><strong>Umbral (95% train):</strong> {String(debug.anomaly_threshold_used ?? debug.threshold ?? 'desconocido')}</p>
            <p><strong>Modelo:</strong> {debug.model_name || debug.model_path || 'desconocido'}</p>
          </div>
        )}
      </div>

      <div className="card-dark p-6 rounded-lg">
        <h3 className="text-lg font-medium text-red-100 mb-3">Probar predicción por partido</h3>

        <div className="flex gap-2 items-center mb-4">
          <input
            type="number"
            placeholder="match_id"
            value={matchId}
            onChange={(e) => setMatchId(e.target.value === '' ? '' : Number(e.target.value))}
            className="px-3 py-2 bg-gray-800 text-gray-200 rounded w-40"
          />
          <button onClick={runPredict} className="px-4 py-2 bg-red-600 rounded" disabled={loadingPred || !matchId}>
            {loadingPred ? 'Procesando...' : 'Ejecutar'}
          </button>
        </div>

        {errorPred && <p className="text-red-400">{errorPred}</p>}

        {prediction && (
          <div className="space-y-3 text-gray-300">
            <p><strong>mse:</strong> {prediction.mse}</p>
            <p><strong>anomaly_score:</strong> {prediction.anomaly_score}</p>
            <p><strong>z_score:</strong> {prediction.z_score}</p>
            <p><strong>mse_percentile:</strong> {prediction.mse_percentile}</p>
            <p><strong>is_anomalous:</strong> {String(prediction.is_anomalous)}</p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
              {prediction.original_image && (
                <div className="text-center">
                  <p className="text-sm text-gray-400 mb-1">Original</p>
                  <img src={prediction.original_image} alt="original" />
                </div>
              )}
              {prediction.reconstructed_image && (
                <div className="text-center">
                  <p className="text-sm text-gray-400 mb-1">Reconstruida</p>
                  <img src={prediction.reconstructed_image} alt="recon" />
                </div>
              )}
              {prediction.comparison_image && (
                <div className="text-center">
                  <p className="text-sm text-gray-400 mb-1">Diferencia</p>
                  <img src={prediction.comparison_image} alt="diff" />
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      <div className="card-dark p-6 rounded-lg">
        <h3 className="text-lg font-medium text-red-100">Resumen</h3>
        <p className="text-gray-300">Resumen: histograma → sqrt → dividir por p99 → clip → autoencoder → MSE. Usa <code>/api/debug_model</code> para alinear preprocesado y umbral en cliente.</p>
        <div className="mt-3 text-sm text-gray-400">
          <details>
            <summary className="cursor-pointer">Ver JSON de debug (para diagnóstico)</summary>
            <pre className="text-xs whitespace-pre-wrap mt-2">{JSON.stringify(debug, null, 2)}</pre>
          </details>
        </div>
      </div>
    </div>
  )
}
