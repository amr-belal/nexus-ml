import { useState } from 'react'
import { predictPrice, type HouseFeatures, type PredictionResponse } from '../services/api'

const defaultFeatures: HouseFeatures = {
  gr_liv_area: 1500,
  total_bsmt_sf: 800,
  garage_area: 400,
  overall_qual: 7,
  overall_cond: 5,
  year_built: 2000,
  year_remod: 2010,
  full_bath: 2,
  half_bath: 1,
  bsmt_full_bath: 1,
  bsmt_half_bath: 0,
  fireplaces: 1,
  pool_area: 0,
  wood_deck_sf: 100,
  open_porch_sf: 50,
  yr_sold: 2025,
}

const fields = [
  { key: 'gr_liv_area', label: 'Living Area (sqft)' },
  { key: 'total_bsmt_sf', label: 'Basement Area (sqft)' },
  { key: 'garage_area', label: 'Garage Area (sqft)' },
  { key: 'overall_qual', label: 'Overall Quality (1-10)' },
  { key: 'overall_cond', label: 'Overall Condition (1-10)' },
  { key: 'year_built', label: 'Year Built' },
  { key: 'year_remod', label: 'Year Remodeled' },
  { key: 'full_bath', label: 'Full Bathrooms' },
  { key: 'half_bath', label: 'Half Bathrooms' },
  { key: 'bsmt_full_bath', label: 'Basement Full Bath' },
  { key: 'bsmt_half_bath', label: 'Basement Half Bath' },
  { key: 'fireplaces', label: 'Fireplaces' },
  { key: 'pool_area', label: 'Pool Area (sqft)' },
  { key: 'wood_deck_sf', label: 'Wood Deck (sqft)' },
  { key: 'open_porch_sf', label: 'Open Porch (sqft)' },
  { key: 'yr_sold', label: 'Year Sold' },
]

const categoryColors: Record<string, string> = {
  Budget: 'text-green-600 bg-green-50',
  Mid: 'text-blue-600 bg-blue-50',
  Luxury: 'text-purple-600 bg-purple-50',
}

export default function Predict() {
  const [features, setFeatures] = useState<HouseFeatures>(defaultFeatures)
  const [result, setResult] = useState<PredictionResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleChange = (key: string, value: string) => {
    setFeatures(prev => ({ ...prev, [key]: parseFloat(value) || 0 }))
  }

  const handleSubmit = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await predictPrice(features)
      setResult(res)
    } catch (e) {
      setError('Prediction failed, make sure the API is running')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Price Predictor</h1>

      <div className="grid md:grid-cols-2 gap-8">
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h2 className="text-lg font-semibold text-gray-700 mb-4">House Features</h2>
          <div className="grid grid-cols-2 gap-4">
            {fields.map(({ key, label }) => (
              <div key={key}>
                <label className="text-xs text-gray-500 mb-1 block">{label}</label>
                <input
                  type="number"
                  value={features[key as keyof HouseFeatures]}
                  onChange={e => handleChange(key, e.target.value)}
                  className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            ))}
          </div>

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="mt-6 w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            {loading ? 'Predicting...' : 'Predict Price'}
          </button>

          {error && <p className="mt-3 text-red-500 text-sm">{error}</p>}
        </div>

        <div>
          {result ? (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <h2 className="text-lg font-semibold text-gray-700 mb-6">Prediction Results</h2>

              <div className="text-4xl font-bold text-blue-600 mb-2">
                ${result.predicted_price.toLocaleString()}
              </div>
              <p className="text-gray-400 text-sm mb-6">Estimated market value</p>

              <div className="grid grid-cols-3 gap-4">
                <div className="bg-gray-50 rounded-lg p-4 text-center">
                  <div className="text-xs text-gray-400 mb-1">Category</div>
                  <span className={`text-sm font-semibold px-2 py-1 rounded-full ${categoryColors[result.price_category]}`}>
                    {result.price_category}
                  </span>
                </div>
                <div className="bg-gray-50 rounded-lg p-4 text-center">
                  <div className="text-xs text-gray-400 mb-1">Cluster</div>
                  <div className="text-lg font-bold text-gray-700">{result.cluster}</div>
                </div>
                <div className="bg-gray-50 rounded-lg p-4 text-center">
                  <div className="text-xs text-gray-400 mb-1">Confidence</div>
                  <div className="text-sm font-semibold text-green-600">{result.confidence}</div>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-gray-50 rounded-xl p-6 border border-dashed border-gray-200 h-full flex items-center justify-center">
              <p className="text-gray-400 text-sm">Fill in the form and click Predict</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}