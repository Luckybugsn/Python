# Overview

This is a Flask-based web service that provides video/audio downloading functionality using yt-dlp. The application exposes a single REST API endpoint that accepts a URL, downloads the media content using yt-dlp, and returns the file to the client. It's designed as a simple, stateless microservice for media downloading.

# Recent Changes

**October 15, 2025**: Initial project setup
- Created Flask application with /download endpoint
- Installed Flask and yt-dlp dependencies
- Installed ffmpeg system dependency for video processing
- Configured Flask Server workflow running on port 5000
- Implemented comprehensive cleanup logic for temporary files on all code paths (success and error)

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Architecture

**Framework**: Flask (Python web framework)
- Chosen for its simplicity and lightweight nature, ideal for single-endpoint microservices
- Runs on port 5000 with debug mode enabled in development

**Request Processing Pattern**: Synchronous request-response
- Each download request is processed synchronously with a 300-second timeout
- Temporary files are created per request and cleaned up after response delivery
- Uses Flask's `after_this_request` decorator to ensure cleanup happens after file transmission

**File Management Strategy**: Temporary directory per request
- Each download creates a unique temporary directory using `tempfile.mkdtemp()`
- Files are stored with template naming: `%(title)s-%(id)s.%(ext)s`
- Automatic cleanup via `shutil.rmtree()` after file is sent or on error
- Rationale: Prevents file accumulation and ensures isolation between concurrent requests

**Media Download Implementation**: yt-dlp subprocess execution
- Uses `subprocess.check_output()` to execute yt-dlp commands
- Command arguments are properly escaped using `shlex.quote()` to prevent injection attacks
- `--no-playlist` flag ensures single video downloads only
- 300-second timeout prevents hung processes

**Error Handling**: Multi-layer approach
- HTTP 400 for missing URL parameter
- HTTP 500 for download failures with error details from yt-dlp output
- HTTP 504 for timeout scenarios
- Exception handling ensures temp directory cleanup in all failure paths

## API Structure

**Endpoint**: `POST /download`
- Accepts JSON payload with `url` field
- Returns downloaded file as attachment or error JSON
- Stateless design with no session management

**Request Format**:
```json
{
  "url": "https://example.com/video"
}
```

**Response Types**:
- Success: Binary file stream with `Content-Disposition: attachment`
- Error: JSON object with `error` and optional `detail` fields

## Security Considerations

**Input Sanitization**: All user inputs are sanitized using `shlex.quote()` before subprocess execution to prevent command injection attacks

**Resource Limits**: 
- 300-second timeout prevents resource exhaustion from long-running downloads
- Temporary file isolation prevents cross-request interference

# External Dependencies

## Core Dependencies

**yt-dlp**: Command-line media downloader
- Purpose: Downloads videos/audio from various platforms
- Integration: Called as subprocess with sanitized arguments
- Must be installed in system PATH

**Flask**: Python web framework (imported)
- Provides HTTP server and request/response handling
- Built-in development server on port 5000

## System Requirements

**Python Standard Library**:
- `tempfile`: Temporary directory creation
- `subprocess`: External process execution
- `shlex`: Safe command-line argument parsing
- `shutil`: Directory cleanup operations
- `os`: File system operations

**Runtime Environment**:
- yt-dlp must be available as system command
- Sufficient disk space for temporary file storage
- Write permissions for temporary directory creation