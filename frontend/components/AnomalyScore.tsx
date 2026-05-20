import React from 'react'
import { Flame, Shield } from 'lucide-react'

interface AnomalyScoreProps {
  prediction: {
    match_id: number
    season_name: string
    mse: number
    threshold: number
    is_anomalous: boolean
    anomaly_score: number
    interpretation: {
      mse_level: string
      message: string
    }
  }
}

export default function AnomalyScore({ prediction }: AnomalyScoreProps) {
  const scorePercentage = Math.min(100, prediction.anomaly_score)
  const isAnomalous = prediction.is_anomalous

  return (
    <div className="card-dark p-8">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold">Anomaly Score</h3>
        {isAnomalous ? (
          <Flame className="text-red-500 pulse-red" size={24} />
        ) : (
          <Shield className="text-green-500" size={24} />
        )}
      </div>

      {/* Match Info */}
      <div className="mb-6 p-4 bg-black/30 rounded-lg border border-red-900/20">
        <p className="text-sm text-gray-400 mb-1">Match ID</p>
        <p className="text-lg font-mono">{prediction.match_id}</p>
        <p className="text-sm text-gray-400 mt-2">Temporada</p>
        <p className="text-gray-200">{prediction.season_name}</p>
      </div>

      {/* Score Visualization */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-semibold text-gray-300">MSE Score</span>
          <span className="text-sm font-mono text-gray-400">
            {prediction.mse.toFixed(6)} / {prediction.threshold.toFixed(6)}
          </span>
        </div>
        <div className="w-full bg-gray-800 rounded-full h-3 overflow-hidden">
          <div
            className={`h-full transition-all duration-500 ${
              isAnomalous
                ? 'bg-gradient-to-r from-red-600 to-red-500'
                : 'bg-gradient-to-r from-green-600 to-green-500'
            }`}
            style={{ width: `${Math.min(scorePercentage, 100)}%` }}
          />
        </div>
      </div>

      {/* Anomaly Indicator */}
      <div className="p-4 rounded-lg bg-gradient-to-r from-red-900/20 to-orange-900/20 border border-red-500/30">
        <div className="flex items-center gap-2 mb-2">
          <div
            className={`w-3 h-3 rounded-full ${
              isAnomalous ? 'bg-red-500 pulse-red' : 'bg-green-500'
            }`}
          />
          <span className={isAnomalous ? 'anomaly-high' : 'anomaly-normal'}>
            {isAnomalous ? 'ANÓMALO' : 'NORMAL'}
          </span>
        </div>
        <p className="text-gray-300 text-sm">{prediction.interpretation.message}</p>
      </div>

      {/* Details */}
      <div className="mt-6 pt-6 border-t border-red-900/20">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-gray-400 mb-1">MSE Level</p>
            <p className="text-gray-100 font-semibold">{prediction.interpretation.mse_level}</p>
          </div>
          <div>
            <p className="text-gray-400 mb-1">Anomaly Probability</p>
            <p className="text-gray-100 font-semibold">{scorePercentage.toFixed(1)}%</p>
          </div>
        </div>
      </div>
    </div>
  )
}
