import { useEffect, useState } from 'react'
import { ScatterChart, Scatter, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import { api } from '../services/api'

const CLUSTER_COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
const CLUSTER_NAMES = ['Mid-range', 'Affordable', 'Luxury', 'Budget']

export default function Models() {
  const [metrics, setMetrics] = useState<any>(null)
  const [clusters, setClusters] = useState<any>(null)
  const [features, setFeatures] = useState<any>(null)
  const [scatterData, setScatterData] = useState<any>(null)

  useEffect(() => {
    api.get('/models/metrics').then(r => setMetrics(r.data))
    api.get('/models/clusters').then(r => setClusters(r.data))
    api.get('/models/feature-importance').then(r => setFeatures(r.data))
    api.get('/models/clusters/scatter').then(r => setScatterData(r.data))
  }, [])

  if (!metrics || !clusters || !features) {
    return <div className="flex items-center justify-center h-64 text-gray-400">Loading...</div>
  }

  const clusterGroups = [0, 1, 2, 3].map(id =>
    scatterData ? scatterData.points.filter((p: any) => p.cluster === id) : []
  )

  return (
    <div className="max-w-6xl mx-auto px-4 py-10 space-y-10">
      <h1 className="text-3xl font-bold text-gray-800">Model Analytics</h1>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 className="text-lg font-semibold text-gray-700 mb-6">Regression Models - R² Score</h2>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={metrics.regression}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" tick={{ fontSize: 12 }} />
            <YAxis domain={[0.7, 1]} tick={{ fontSize: 12 }} />
            <Tooltip />
            <Bar dataKey="r2" fill="#3b82f6" radius={[4, 4, 0, 0]} name="R² Score" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 className="text-lg font-semibold text-gray-700 mb-6">Classification Models - Accuracy</h2>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={metrics.classification}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" tick={{ fontSize: 12 }} />
            <YAxis domain={[0.7, 1]} tick={{ fontSize: 12 }} />
            <Tooltip />
            <Bar dataKey="accuracy" fill="#8b5cf6" radius={[4, 4, 0, 0]} name="Accuracy" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 className="text-lg font-semibold text-gray-700 mb-6">Top 10 Feature Importance</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={features.features} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" tick={{ fontSize: 11 }} />
            <YAxis dataKey="name" type="category" width={120} tick={{ fontSize: 11 }} />
            <Tooltip />
            <Bar dataKey="importance" fill="#10b981" radius={[0, 4, 4, 0]} name="Importance" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 className="text-lg font-semibold text-gray-700 mb-6">Price Clusters</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {clusters.clusters.map((c: any) => (
            <div key={c.id} className="bg-gray-50 rounded-lg p-4 text-center">
              <div className="text-sm text-gray-400 mb-1">{c.name}</div>
              <div className="text-xl font-bold text-gray-800">${c.avg_price.toLocaleString()}</div>
              <div className="text-xs text-gray-400 mt-1">{c.count} houses</div>
            </div>
          ))}
        </div>
      </div>

      {scatterData && (
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h2 className="text-lg font-semibold text-gray-700 mb-6">Clusters Visualization (PCA)</h2>
          <ResponsiveContainer width="100%" height={400}>
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="x" name="PCA 1" tick={{ fontSize: 11 }} type="number" domain={['auto', 'auto']} />
              <YAxis dataKey="y" name="PCA 2" tick={{ fontSize: 11 }} type="number" domain={['auto', 'auto']} />
              <Tooltip content={({ payload }) => {
                if (payload && payload.length) {
                  const d = payload[0].payload
                  return (
                    <div className="bg-white p-2 border border-gray-200 rounded text-xs shadow">
                      <div className="font-medium">{CLUSTER_NAMES[d.cluster]}</div>
                      <div>Price: ${d.price.toLocaleString()}</div>
                    </div>
                  )
                }
                return null
              }} />
              <Legend />
              {clusterGroups.map((data, i) => (
                <Scatter
                  key={i}
                  name={CLUSTER_NAMES[i]}
                  data={data}
                  fill={CLUSTER_COLORS[i]}
                  opacity={0.6}
                />
              ))}
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}