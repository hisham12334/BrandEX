import fs from 'fs'
import path from 'path'

export default function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' })
  }

  const { username, password } = req.body

  // Validate credentials
  if (!username || !password) {
    return res.status(400).json({ message: 'Username and password required' })
  }

  // Update .env file
  const envPath = path.join(process.cwd(), '.env')
  const envContent = `INSTAGRAM_USERNAME=${username}\nINSTAGRAM_PASSWORD=${password}`

  try {
    fs.writeFileSync(envPath, envContent)
    return res.status(200).json({ 
      success: true,
      message: 'Instagram credentials saved'
    })
  } catch (error) {
    return res.status(500).json({ 
      success: false,
      message: 'Error saving credentials'
    })
  }
}
