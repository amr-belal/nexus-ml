import { BarChart2, Home as HomeIcon, TrendingUp, Brain } from 'lucide-react'

const stats = [
  { label: 'Model Accuracy', value: '92.5%', icon: TrendingUp, color: 'text-blue-600' },
  { label: 'Training Samples', value: '2,344', icon: BarChart2, color: 'text-green-600' },
  { label: 'Features Used', value: '284', icon: Brain, color: 'text-purple-600' },
  { label: 'Price Clusters', value: '4', icon: HomeIcon, color: 'text-orange-600' },
]

export default function Home() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="mb-10">
        <h1 className="text-4xl font-bold text-gray-800 mb-3">
          Real Estate Price Predictor
        </h1>
        <p className="text-gray-500 text-lg">
          Predict house prices using Machine Learning trained on Ames Housing Dataset
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
        {stats.map(({ label, value, icon: Icon, color }) => (
          <div key={label} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <Icon className={`${color} mb-3`} size={24} />
            <div className="text-2xl font-bold text-gray-800">{value}</div>
            <div className="text-sm text-gray-500 mt-1">{label}</div>
          </div>
        ))}
      </div>

      <div className="bg-blue-50 rounded-xl p-8 border border-blue-100">
        <h2 className="text-xl font-semibold text-blue-800 mb-2">How it works</h2>
        <div className="grid md:grid-cols-3 gap-6 mt-4">
          {[
            { step: '1', title: 'Enter Details', desc: 'Fill in your house features' },
            { step: '2', title: 'AI Predicts', desc: 'Our ML model analyzes the data' },
            { step: '3', title: 'Get Results', desc: 'Receive price prediction instantly' },
          ].map(({ step, title, desc }) => (
            <div key={step} className="flex items-start gap-4">
              <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm flex-shrink-0">
                {step}
              </div>
              <div>
                <div className="font-medium text-gray-800">{title}</div>
                <div className="text-sm text-gray-500">{desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}