import { Typography } from '@mui/material'
import Dashboard from '../components/Dashboard'

function DashboardPage() {
  return (
    <div>
      <Typography variant="h4" sx={{ mb: 2 }}>
        Dashboard
      </Typography>
      <Dashboard />
    </div>
  )
}

export default DashboardPage
