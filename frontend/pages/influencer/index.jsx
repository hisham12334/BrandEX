import { useState, useEffect } from 'react'
import Layout from '../../components/Layout'
import InstagramLogin from '../../components/InstagramLogin'
import ProfileSummary from '../../components/influencer/ProfileSummary'
import RecommendedBrands from '../../components/influencer/RecommendedBrands'
import PricingEstimate from '../../components/influencer/PricingEstimate'

export default function InfluencerDashboard() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  useEffect(() => {
    // Check for existing login in local storage
    const loggedIn = localStorage.getItem('instagramLoggedIn') === 'true'
    setIsLoggedIn(loggedIn)
  }, [])

  const handleLoginSuccess = () => {
    localStorage.setItem('instagramLoggedIn', 'true')
    setIsLoggedIn(true)
  }

  if (!isLoggedIn) {
    return (
      <Layout>
        <div className="flex justify-center py-12">
          <InstagramLogin onLogin={handleLoginSuccess} />
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="space-y-8">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Influencer Dashboard</h1>
          <button 
            onClick={() => {
              localStorage.removeItem('instagramLoggedIn')
              setIsLoggedIn(false)
            }}
            className="text-sm text-red-600 hover:text-red-800"
          >
            Logout
          </button>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1">
            <ProfileSummary />
          </div>
          <div className="lg:col-span-2 space-y-6">
            <RecommendedBrands />
            <PricingEstimate />
          </div>
        </div>
      </div>
    </Layout>
  )
}
