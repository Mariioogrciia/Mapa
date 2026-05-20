'use client'

import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Search, ChevronDown } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface MatchSelectorProps {
  onSelectMatch: (matchId: number) => void
}

interface Season {
  id: number
  name: string
  matches: number
  type: 'train' | 'test' | 'explore'
}

export default function MatchSelector({ onSelectMatch }: MatchSelectorProps) {
  const [seasons, setSeasons] = useState<Season[]>([])
  const [selectedSeason, setSelectedSeason] = useState<number | null>(null)
  const [matches, setMatches] = useState<number[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchSeasons = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/seasons`)
        setSeasons(response.data.seasons)
        // Seleccionar primera temporada por defecto (explore)
        const exploreSeasons = response.data.seasons.filter((s: Season) => s.type === 'explore')
        if (exploreSeasons.length > 0) {
          setSelectedSeason(exploreSeasons[0].id)
        }
      } catch (error) {
        console.error('Error fetching seasons:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchSeasons()
  }, [])

  useEffect(() => {
    if (selectedSeason) {
      fetchMatches(selectedSeason)
    }
  }, [selectedSeason])

  const fetchMatches = async (seasonId: number) => {
    try {
      const response = await axios.get(`${API_URL}/api/matches`, {
        params: { season_id: seasonId },
      })
      setMatches(response.data.matches)
    } catch (error) {
      console.error('Error fetching matches:', error)
    }
  }

  const filteredMatches = matches.filter((m) =>
    m.toString().includes(searchQuery)
  )

  const getSeasonBadgeColor = (type: string) => {
    switch (type) {
      case 'train':
        return 'bg-blue-900/30 text-blue-300'
      case 'test':
        return 'bg-yellow-900/30 text-yellow-300'
      case 'explore':
        return 'bg-red-900/30 text-red-300'
      default:
        return 'bg-gray-900/30 text-gray-300'
    }
  }

  return (
    <div className="card-dark p-6">
      <h3 className="text-xl font-bold mb-4">Selector de Partido</h3>

      {/* Season Filter */}
      <div className="mb-6">
        <label className="block text-sm font-semibold text-gray-300 mb-2">Temporada</label>
        <select
          value={selectedSeason || ''}
          onChange={(e) => setSelectedSeason(Number(e.target.value))}
          className="w-full px-4 py-2 bg-gray-800 text-white rounded-lg border border-gray-700 hover:border-red-500 focus:border-red-500 outline-none transition-all"
        >
          <option value="">-- Selecciona temporada --</option>
          {seasons.map((season) => (
            <option key={season.id} value={season.id}>
              {season.name} ({season.matches} partidos)
            </option>
          ))}
        </select>
      </div>

      {/* Season Info */}
      {selectedSeason && (
        <div className="mb-4 p-3 bg-black/30 rounded-lg border border-red-900/20">
          {seasons
            .filter((s) => s.id === selectedSeason)
            .map((season) => (
              <div key={season.id}>
                <p className="text-xs text-gray-400 mb-1">Tipo de temporada</p>
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-1 rounded text-xs font-semibold ${getSeasonBadgeColor(season.type)}`}>
                    {season.type === 'train' ? 'ENTRENAMIENTO' : season.type === 'test' ? 'TEST' : 'EXPLORACIÓN'}
                  </span>
                  <span className="text-sm text-gray-300">{season.matches} partidos disponibles</span>
                </div>
              </div>
            ))}
        </div>
      )}

      {/* Match Search */}
      <div className="mb-4">
        <label className="block text-sm font-semibold text-gray-300 mb-2">Buscar Partido</label>
        <div className="relative">
          <Search size={18} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" />
          <input
            type="text"
            placeholder="Ingresa Match ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-gray-800 text-white rounded-lg border border-gray-700 hover:border-red-500 focus:border-red-500 outline-none transition-all"
          />
        </div>
      </div>

      {/* Match List */}
      <div className="border-t border-red-900/20 pt-4">
        <p className="text-xs text-gray-400 mb-3">Partidos disponibles ({filteredMatches.length})</p>
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {loading ? (
            <div className="text-center py-8 text-gray-400">Cargando...</div>
          ) : filteredMatches.length === 0 ? (
            <div className="text-center py-8 text-gray-500">No hay partidos disponibles</div>
          ) : (
            filteredMatches.map((matchId) => (
              <button
                key={matchId}
                onClick={() => onSelectMatch(matchId)}
                className="w-full text-left px-4 py-3 bg-gray-800 hover:bg-red-900/30 border border-gray-700 hover:border-red-500 rounded-lg transition-all font-mono text-sm"
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold">{matchId}</span>
                  <span className="text-gray-500 group-hover:text-red-400">→</span>
                </div>
              </button>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
