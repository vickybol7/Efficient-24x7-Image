# Docker Hub - Pull and Run Guide

This guide explains how to pull and run the pre-built Docker image from [Docker Hub](https://hub.docker.com/r/imvickykumar999/youtube-stream).

## Quick Start

### 1. Pull the Image

```bash
docker pull imvickykumar999/youtube-stream:latest
```

### 2. Run with Environment Variables

```bash
docker run -d --name youtube-stream \
  -e STREAM_KEY=your_youtube_stream_key_here \
  -e YouTube_ID=your_youtube_video_id_here \
  imvickykumar999/youtube-stream:latest
```

### 3. Or Use a .env File

Create a `.env` file in your current directory:

```env
STREAM_KEY=your_youtube_stream_key_here
YouTube_ID=your_youtube_video_id_here
```

Then run:

```bash
docker run -d --name youtube-stream \
  --env-file .env \
  imvickykumar999/youtube-stream:latest
```

## Detailed Instructions

### Prerequisites

- Docker installed on your system
- YouTube Live stream key (get it from [YouTube Studio](https://studio.youtube.com/channel/UC/livestreaming))
- YouTube video ID to stream

### Step-by-Step Guide

#### Step 1: Pull the Latest Image

```bash
docker pull imvickykumar999/youtube-stream:latest
```

This will download the pre-built image from Docker Hub. You only need to do this once, or when you want to update to the latest version.

#### Step 2: Get Your YouTube Credentials

1. **YouTube Stream Key**: 
   - Go to [YouTube Studio](https://studio.youtube.com/channel/UC/livestreaming)
   - Navigate to "Stream" settings
   - Copy your stream key

2. **YouTube Video ID**: 
   - Extract the video ID from a YouTube URL
   - Example: For `https://www.youtube.com/watch?v=oY7SfTpyRco`, the ID is `oY7SfTpyRco`

#### Step 3: Run the Container

**Option A: Using Environment Variables (Direct)**

```bash
docker run -d \
  --name youtube-stream \
  -e STREAM_KEY=qvfy-u9ar-1900-63qx-625y \
  -e YouTube_ID=oY7SfTpyRco \
  imvickykumar999/youtube-stream:latest
```

**Option B: Using .env File (Recommended)**

1. Create a `.env` file:
   ```bash
   echo "STREAM_KEY=your_stream_key_here" > .env
   echo "YouTube_ID=your_video_id_here" >> .env
   ```

2. Run the container:
   ```bash
   docker run -d \
     --name youtube-stream \
     --env-file .env \
     imvickykumar999/youtube-stream:latest
   ```

#### Step 4: Monitor the Stream

View the container logs:

```bash
docker logs -f youtube-stream
```

Press `Ctrl+C` to exit the log view (this won't stop the container).

#### Step 5: Check Container Status

```bash
docker ps
```

You should see `youtube-stream` in the list if it's running.

### Managing the Container

#### Stop the Container

```bash
docker stop youtube-stream
```

#### Start a Stopped Container

```bash
docker start youtube-stream
```

#### Remove the Container

```bash
docker stop youtube-stream
docker rm youtube-stream
```

Or force remove (stops and removes in one command):

```bash
docker rm -f youtube-stream
```

#### Restart the Container

```bash
docker restart youtube-stream
```

### Troubleshooting

#### Container Exits Immediately

Check the logs to see what went wrong:

```bash
docker logs youtube-stream
```

Common issues:
- Missing or invalid `STREAM_KEY`
- Missing or invalid `YouTube_ID`
- Network connectivity issues

#### Update to Latest Version

```bash
docker pull imvickykumar999/youtube-stream:latest
docker stop youtube-stream
docker rm youtube-stream
docker run -d --name youtube-stream --env-file .env imvickykumar999/youtube-stream:latest
```

#### View Resource Usage

```bash
docker stats youtube-stream
```

This shows real-time CPU, memory, and network usage.

### Docker Compose (Alternative)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  youtube-stream:
    image: imvickykumar999/youtube-stream:latest
    container_name: youtube-stream
    env_file:
      - .env
    restart: unless-stopped
```

Then run:

```bash
docker-compose up -d
```

View logs:
```bash
docker-compose logs -f
```

Stop:
```bash
docker-compose down
```

## Image Details

- **Image**: `imvickykumar999/youtube-stream:latest`
- **Base Image**: Python 3.11-slim
- **Includes**: FFmpeg, yt-dlp, python-dotenv
- **Size**: ~500-600 MB (compressed)

## Features

- ✅ Optimized for low CPU usage
- ✅ Automatic video download from YouTube
- ✅ 360p streaming support for cost efficiency
- ✅ Infinite video loop
- ✅ Keyframe optimization for YouTube Live compatibility

## Support

For issues or questions:
- Docker Hub: [https://hub.docker.com/r/imvickykumar999/youtube-stream](https://hub.docker.com/r/imvickykumar999/youtube-stream)
- Check container logs: `docker logs youtube-stream`

