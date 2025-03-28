import axios from 'axios'
import { InstagramClient } from 'instagram-graph-api'

export default async function handler(req, res) {
  try {
    // Initialize Instagram client with credentials from .env
    const client = new InstagramClient({
      username: process.env.INSTAGRAM_USERNAME,
      password: process.env.INSTAGRAM_PASSWORD
    })

    // Fetch profile data
    const profile = await client.getProfile()
    const insights = await client.getInsights()

    // Format response data
    const responseData = {
      followers: profile.followers_count,
      engagement_rate: insights.engagement_rate,
      sentiment_score: insights.sentiment_score,
      age_range: insights.audience_age_range,
      age_percent: insights.audience_age_percent,
      gender: insights.audience_gender,
      gender_percent: insights.audience_gender_percent,
      top_location: insights.audience_top_location,
      location_percent: insights.audience_location_percent
    }

    res.status(200).json(responseData)
  } catch (error) {
    console.error('Error fetching Instagram data:', error)
    res.status(500).json({ 
      error: 'Failed to fetch profile data',
      details: error.message 
    })
  }
}
