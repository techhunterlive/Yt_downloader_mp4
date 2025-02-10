from flask import Flask, request, render_template, Response
import yt_dlp

app = Flask(__name__)

def get_video_url(youtube_url):
    """ Extracts the best MP4 download link from YouTube """
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info['url'], info['title']  # Return both URL & Title

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    youtube_url = request.form.get('url')

    if not youtube_url:
        return "Invalid URL"

    video_url, title = get_video_url(youtube_url)

    return render_template('download.html', video_url=video_url, title=title)

@app.route('/force_download')
def force_download():
    video_url = request.args.get('video_url')

    if not video_url:
        return "Invalid video link"

    return Response(
        f'<script>window.location.href="{video_url}";</script>',
        mimetype="text/html"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
