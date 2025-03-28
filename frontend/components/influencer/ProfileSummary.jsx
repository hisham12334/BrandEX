import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer } from 'recharts'
import axios from 'axios'

export default function ProfileSummary() {
  const [profileData, setProfileData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get('/api/influencer/profile')
        setProfileData(response.data)
      } catch (error) {
        console.error('Error fetching profile:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchProfile()
  }, [])

  if (loading) {
    return <div className="bg-white rounded-lg shadow p-6">Loading profile...</div>
  }

  if (!profileData) {
    return <div className="bg-white rounded-lg shadow p-6">Failed to load profile data</div>
  }

  const chartData = [
    { name: 'Followers', value: profileData.followers },
    { name: 'Engagement', value: profileData.engagement_rate },
    { name: 'Sentiment', value: profileData.sentiment_score },
  ]
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Profile Summary</h2>
      
      <div className="space-y-4">
        <div>
          <h3 className="font-medium">Audience Demographics</h3>
          <p className="text-sm text-gray-600">Age: {profileData.age_range} ({profileData.age_percent}%)</p>
          <p className="text-sm text-gray-600">Gender: {profileData.gender} ({profileData.gender_percent}%)</p>
          <p className="text-sm text-gray-600">Location: {profileData.top_location} ({profileData.location_percent}%)</p>
        </div>

        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <XAxis dataKey="name" />
              <YAxis />
              <Bar dataKey="value" fill="#4F46E5" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
