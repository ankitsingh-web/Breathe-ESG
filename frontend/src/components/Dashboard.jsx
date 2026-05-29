import { useEffect, useState } from 'react'
import {
  Typography,
  Paper,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Button,
  Chip,
  Box,
  CircularProgress,
} from '@mui/material'
import api from '../api/api'

function Dashboard() {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchRecords = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await api.get('records/')
      setRecords(response.data)
    } catch (fetchError) {
      setError('Unable to load records. Please restart the backend and try again.')
    } finally {
      setLoading(false)
    }
  }

  const approveRecord = async (id) => {
    try {
      await api.patch(`approve/${id}/`)
      fetchRecords()
    } catch (approveError) {
      setError('Unable to approve record, please retry.')
    }
  }

  useEffect(() => {
    fetchRecords()
  }, [])

  return (
    <Paper sx={{ p: 4, maxWidth: '100%', mx: 'auto' }}>
      <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Typography variant="h5">Emission Records</Typography>
        {loading && <CircularProgress size={24} />}
      </Box>

      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}

      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Activity</TableCell>
            <TableCell>Scope</TableCell>
            <TableCell>Emission</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Anomaly</TableCell>
            <TableCell>Action</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {records.map((record) => (
            <TableRow key={record.id}>
              <TableCell>{record.activity_type}</TableCell>
              <TableCell>{record.scope}</TableCell>
              <TableCell>{record.emission_kg_co2e.toFixed(2)}</TableCell>
              <TableCell>
                <Chip
                  label={record.status}
                  color={record.status === 'APPROVED' ? 'success' : 'warning'}
                  size="small"
                />
              </TableCell>
              <TableCell>
                {record.anomaly_flag ? <Chip label="Yes" color="error" size="small" /> : 'No'}
              </TableCell>
              <TableCell>
                <Button
                  variant="contained"
                  size="small"
                  onClick={() => approveRecord(record.id)}
                  disabled={record.status === 'APPROVED'}
                >
                  Approve
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  )
}

export default Dashboard
