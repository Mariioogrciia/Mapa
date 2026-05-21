'use client'

import React, { useEffect, useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface UnusedMatch {
  match_id: number
  season_id: number
}

interface UnusedProps {
  onSelectMatch: (matchId: number) => void
}

export default function UnusedMatches({ onSelectMatch }: UnusedProps) {
  const [matches, setMatches] = useState<UnusedMatch[]>([])
  const [loading, setLoading] = useState(true)
  const [usedInfo, setUsedInfo] = useState<any>(null)
  const [selectedIds, setSelectedIds] = useState<number[]>([])
  const [batchLoading, setBatchLoading] = useState(false)
  const [batchResults, setBatchResults] = useState<any[]>([])

  useEffect(() => {
    const fetch = async () => {
      try {
        const [r1, r2] = await Promise.all([
          axios.get(`${API_URL}/api/unused_matches`),
          axios.get(`${API_URL}/api/used_data`),
        ])
        setMatches(r1.data.matches)
        setUsedInfo(r2.data)
      } catch (e) {
        console.error('Error fetching unused matches or used data', e)
      } finally {
        setLoading(false)
      }
    }

    fetch()
  }, [])

  return (
    <div className="card-dark p-6">
      <h3 className="text-lg font-bold mb-3">Partidos No Usados (Explore)</h3>

      {usedInfo && (
        <div className="mb-4 p-3 bg-black/30 rounded border border-red-900/20 text-sm">
          <p><strong>Temporadas de entrenamiento:</strong> {usedInfo.season_train_ids.join(', ')}</p>
          <p><strong>Temporadas de test:</strong> {usedInfo.season_test_ids.join(', ')}</p>
          <p className="mt-2"><strong>Partidos train:</strong> {usedInfo.train_match_count} — muestra: {usedInfo.train_matches_sample.slice(0,5).join(', ')}</p>
          <p><strong>Partidos test:</strong> {usedInfo.test_match_count} — muestra: {usedInfo.test_matches_sample.slice(0,5).join(', ')}</p>
        </div>
      )}

      <div className="mb-3 text-sm text-gray-400">Selecciona un partido no usado para comprobar la predicción del modelo.</div>

      <div className="max-h-80 overflow-y-auto space-y-2">
        {loading ? (
          <div className="text-gray-400">Cargando...</div>
        ) : matches.length === 0 ? (
          <div className="text-gray-400">No se encontraron partidos no usados.</div>
        ) : (
          matches.map((m) => (
            <div key={m.match_id} className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={selectedIds.includes(m.match_id)}
                onChange={(e) => {
                  if (e.target.checked) setSelectedIds((s) => [...s, m.match_id])
                  else setSelectedIds((s) => s.filter((id) => id !== m.match_id))
                }}
                className="w-4 h-4"
              />
              <button
                onClick={() => onSelectMatch(m.match_id)}
                className="w-full text-left px-3 py-2 bg-gray-800 hover:bg-red-900/30 border border-gray-700 rounded-lg transition-all font-mono text-sm"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-semibold">{m.match_id}</div>
                    <div className="text-xs text-gray-400">Season {m.season_id}</div>
                  </div>
                  <div className="text-gray-500">Ver →</div>
                </div>
              </button>
            </div>
          ))
        )}
      </div>
      {/* Batch predict controls */}
      <div className="mt-4 flex gap-2">
        <button
          disabled={selectedIds.length === 0 || batchLoading}
          onClick={async () => {
            setBatchLoading(true)
            try {
              const resp = await axios.post(`${API_URL}/api/predict_batch`, { match_ids: selectedIds })
              setBatchResults(resp.data.results || [])
            } catch (e) {
              console.error('Batch predict error', e)
            } finally {
              setBatchLoading(false)
            }
          }}
          className="px-3 py-2 bg-red-700 text-white rounded disabled:opacity-50"
        >
          {batchLoading ? 'Procesando...' : `Predecir seleccionados (${selectedIds.length})`}
        </button>

        <button
          onClick={() => {
            setSelectedIds([])
            setBatchResults([])
          }}
          className="px-3 py-2 bg-gray-700 text-white rounded"
        >
          Limpiar
        </button>
      </div>

      {/* Batch results */}
      {batchResults.length > 0 && (
        <div className="mt-4 bg-black/20 p-3 rounded">
          <h4 className="font-semibold mb-2">Resultados por lote</h4>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-400">
                  <th>match_id</th>
                  <th>MSE</th>
                  <th>Anómalo</th>
                  <th>Score</th>
                </tr>
              </thead>
              <tbody>
                {batchResults.map((r: any) => (
                  <tr key={r.match_id} className="border-t border-red-900/10">
                    <td className="py-1">{r.match_id}</td>
                    <td>{r.mse ? r.mse.toFixed(6) : '-'}</td>
                    <td>{r.is_anomalous ? 'Sí' : 'No'}</td>
                    <td>{r.anomaly_score ? r.anomaly_score.toFixed(1) : '0'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="mt-2">
            <button
              onClick={() => {
                // download CSV
                const rows = [['match_id','mse','is_anomalous','anomaly_score'], ...batchResults.map((r: any) => [r.match_id, r.mse, r.is_anomalous, r.anomaly_score])]
                const csv = rows.map((r) => r.join(',')).join('\n')
                const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
                const url = URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = url
                a.download = 'batch_predictions.csv'
                a.click()
                URL.revokeObjectURL(url)
              }}
              className="px-3 py-2 bg-green-700 text-white rounded"
            >
              Descargar CSV
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
