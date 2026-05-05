import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface HouseFeatures {
  gr_liv_area: number
  total_bsmt_sf: number
  garage_area: number
  overall_qual: number
  overall_cond: number
  year_built: number
  year_remod: number
  full_bath: number
  half_bath: number
  bsmt_full_bath: number
  bsmt_half_bath: number
  fireplaces: number
  pool_area: number
  wood_deck_sf: number
  open_porch_sf: number
  yr_sold: number
}

export interface PredictionResponse {
  predicted_price: number
  price_category: string
  cluster: number
  confidence: string
}

export const predictPrice = async (features: HouseFeatures): Promise<PredictionResponse> => {
  const response = await api.post('/predictions/predict', features)
  return response.data
}