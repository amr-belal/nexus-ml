// import { Home, TrendingUp, MessageCircle } from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'
import { Home, TrendingUp, MessageCircle, BarChart2 } from 'lucide-react'

export default function Navbar() {
  const location = useLocation()

  const links = [
    { to: '/', label: 'Home', icon: Home },
    { to: '/predict', label: 'Predict', icon: TrendingUp },
    { to: '/chat', label: 'ChatBot', icon: MessageCircle },
    { to: '/models', label: 'Models', icon: BarChart2 },
  ]

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <span className="text-xl font-bold text-blue-600">NexusML</span>
        <div className="flex gap-6">
          {links.map(({ to, label, icon: Icon }) => (
            <Link
              key={to}
              to={to}
              className={`flex items-center gap-2 text-sm font-medium transition-colors
                ${location.pathname === to
                  ? 'text-blue-600'
                  : 'text-gray-500 hover:text-blue-600'
                }`}
            >
              <Icon size={16} />
              {label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  )
}