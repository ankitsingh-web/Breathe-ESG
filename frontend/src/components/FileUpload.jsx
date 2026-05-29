import { useState } from 'react'
import {
  Box,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Paper,
  Alert,
} from '@mui/material'
import api from '../api/api'

function FileUpload() {
  const [file, setFile] = useState(null)
  const [sourceType, setSourceType] = useState('SAP')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setMessage('')

    if (!file) {
      setError('Please select a file to upload.')
      return
    }

    const formData = new FormData()
    formData.append('file', file)
    formData.append('source_type', sourceType)

    try {
      await api.post('upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setMessage('File uploaded successfully.')
      setFile(null)
    } catch (uploadError) {
      setError('Upload failed. Please check the file format and try again.')
    }
  }

  return (
    <Paper sx={{ p: 4, maxWidth: 640, mx: 'auto' }}>
      <Typography variant="h5" gutterBottom>
        Upload ESG Data CSV
      </Typography>

      {message && <Alert severity="success">{message}</Alert>}
      {error && <Alert severity="error">{error}</Alert>}

      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3, gap: 2, display: 'grid' }}>
        <FormControl fullWidth>
          <InputLabel id="source-label">Source Type</InputLabel>
          <Select
            labelId="source-label"
            label="Source Type"
            value={sourceType}
            onChange={(e) => setSourceType(e.target.value)}
          >
            <MenuItem value="SAP">SAP</MenuItem>
            <MenuItem value="UTILITY">UTILITY</MenuItem>
            <MenuItem value="TRAVEL">TRAVEL</MenuItem>
          </Select>
        </FormControl>

        <Button variant="contained" component="label">
          Select CSV File
          <input
            type="file"
            hidden
            accept=".csv"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          />
        </Button>

        {file && <Typography>{file.name}</Typography>}

        <Button type="submit" variant="contained" color="primary">
          Upload
        </Button>
      </Box>
    </Paper>
  )
}

export default FileUpload
