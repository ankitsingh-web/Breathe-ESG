import { Typography } from '@mui/material'
import FileUpload from '../components/FileUpload'

function UploadPage() {
  return (
    <div>
      <Typography variant="h4" sx={{ mb: 2 }}>
        Data Upload
      </Typography>
      <FileUpload />
    </div>
  )
}

export default UploadPage
