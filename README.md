# Pandoc Text Converter API

This is a Flask-based API that uses pandoc to convert text to various formats.

## Prerequisites

- Python 3.x
- pandoc (must be installed on your system)
- pip (Python package manager)
- Docker (optional, for containerized deployment)

## Installation

### Local Installation

1. Install pandoc on your system:
   - macOS: `brew install pandoc`
   - Ubuntu/Debian: `sudo apt-get install pandoc`
   - Windows: Download from [pandoc.org](https://pandoc.org/installing.html)

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Docker Installation

1. Build the Docker image:
```bash
docker build -t pandoc-converter .
```

2. Run the container:
```bash
docker run -p 5000:5000 pandoc-converter
```
如果要挂载出来就文件夹/app/uploads映射即可

## Usage

1. Start the server:
```bash
# For local installation
python app.py

# For Docker installation
docker run -p 5000:5000 pandoc-converter
```

2. The API will be available at `http://localhost:5000`

### API Endpoints

#### Convert Text
- **URL**: `/convert`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
```json
{
    "text": "Your text content here",
    "output_format": "pdf"  // or any other format supported by pandoc
}
```

#### Download Converted File
- **URL**: `/download/<filename>`
- **Method**: `GET`

### Example Usage

```bash
curl -X POST http://localhost:5000/convert \
  -H "Content-Type: application/json" \
  -d '{"text": "# Hello World\nThis is a test", "output_format": "pdf"}'
```

The response will include a download URL for the converted file.

## Supported Formats

The API supports all formats that pandoc can convert to, including:
- PDF
- HTML
- DOCX
- EPUB
- And many more

## Security Notes

- The API includes basic security measures to prevent directory traversal attacks
- Files are stored with unique UUIDs to prevent naming conflicts
- Input validation is performed on all requests

## Docker Notes

- The Docker image is based on Debian 11.11
- Includes all necessary dependencies for pandoc and PDF generation
- Exposes port 5000 for API access
- Creates a persistent uploads directory for converted files 
