"""
████████╗████████╗███████╗                                                          
╚══██╔══╝╚══██╔══╝██╔════╝                                                          
   ██║      ██║   ███████╗                                                          
   ██║      ██║   ╚════██║                                                          
   ██║      ██║   ███████║                                                          
   ╚═╝      ╚═╝   ╚══════╝                                                          
██╗███╗   ██╗██████╗  ██████╗ ███╗   ██╗███████╗███████╗██╗ █████╗ ██╗  ██╗██╗   ██╗
██║████╗  ██║██╔══██╗██╔═══██╗████╗  ██║██╔════╝██╔════╝██║██╔══██╗██║ ██╔╝██║   ██║
██║██╔██╗ ██║██║  ██║██║   ██║██╔██╗ ██║█████╗  ███████╗██║███████║█████╔╝ ██║   ██║
██║██║╚██╗██║██║  ██║██║   ██║██║╚██╗██║██╔══╝  ╚════██║██║██╔══██║██╔═██╗ ██║   ██║
██║██║ ╚████║██████╔╝╚██████╔╝██║ ╚████║███████╗███████║██║██║  ██║██║  ██╗╚██████╔╝
╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ 
                                                                                    
Flask API untuk TTS Indonesia - dibuat oleh __drat

API Endpoints:
- POST /api/tts - Generate TTS audio dari teks
- GET /api/speakers - Dapatkan daftar pembicara
- GET /api/languages - Dapatkan daftar bahasa
- GET /health - Health check endpoint
"""

import html
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_restx import Api, Namespace, Resource, fields
from werkzeug.exceptions import BadRequest

sys.path.insert(0, str(Path(__file__).parent / 'g2p-id'))
from g2p import G2P

# Inisialisasi Flask app
app = Flask(__name__)
CORS(app)

# Inisialisasi API dengan Swagger documentation
api = Api(
    app,
    version='1.0',
    title='TTS Indonesia API',
    description='API untuk Text-to-Speech bahasa Indonesia dengan berbagai pilihan suara',
    doc='/swagger/',
    contact='Energi Semesta Digital',
    contact_url='https://github.com/muhammwafa/TTS-Indonesia-Gratis'
)

# Namespace untuk API endpoints
ns = Namespace('api', description='API operations')
api.add_namespace(ns)

# Data models untuk Swagger documentation
tts_model = api.model('TTSRequest', {
    'text': fields.String(required=True, description='Text yang akan diubah menjadi suara', example='Halo, selamat pagi Indonesia!'),
    'speaker': fields.String(required=False, description='Pilihan speaker', default='ardi', enum=['wibowo', 'ardi', 'gadis', 'juminten', 'asep']),
    'speed': fields.Float(required=False, description='Kecepatan bicara (0.1 - 1.99)', default=0.8, example=0.8),
    'language': fields.String(required=False, description='Bahasa', default='Indonesian', example='Indonesian')
})

speaker_model = api.model('Speaker', {
    'id': fields.String(description='ID speaker', example='ardi'),
    'name': fields.String(description='Nama speaker', example='Ardi'),
    'description': fields.String(description='Deskripsi speaker', example='Suara lembut dan hangat')
})

health_model = api.model('Health', {
    'status': fields.String(description='Service status', example='healthy'),
    'service': fields.String(description='Service name', example='TTS Indonesia API')
})

# Inisialisasi G2P (Grapheme to Phoneme)
g2p = G2P()

# Parameter default untuk konfigurasi
params = {
    "activate": True,
    "autoplay": True,
    "show_text": True,
    "remove_trailing_dots": False,
    "voice": "default.wav",
    "language": "Indonesian",
    "model_path": "models/checkpoint_1260000-inference.pth",
    "config_path": "config/config.json",
    "out_path": "output.wav"
}

SAMPLE_RATE = 16000
device = None

# Set nama pembicara default
default_speaker_name = "ardi"

# Speaker mapping
SPEAKER_MAPPING = {
    "wibowo": "wibowo",
    "ardi": "ardi",
    "gadis": "gadis",
    "juminten": "JV-00264",
    "asep": "SU-00060"
}

# Memuat data bahasa
languages = {}
languages_file = Path('config/languages.json')
if languages_file.exists():
    with open(languages_file, encoding='utf8') as f:
        languages = json.load(f)

# Buat direktori outputs jika belum ada
Path('outputs').mkdir(exist_ok=True)


def gen_voice(text, speaker, speed=0.8, language="Indonesian"):
    """
    Fungsi untuk menghasilkan suara dari teks
    """
    try:
        # Validasi speaker
        if speaker not in SPEAKER_MAPPING:
            speaker = default_speaker_name

        speaker_id = SPEAKER_MAPPING[speaker]

        # Konversi teks
        text = html.unescape(text)
        text_to_tts = g2p(text)

        # Generate unique filename
        short_uuid = str(uuid.uuid4())[:8]
        output_file = Path(f'outputs/{speaker}-{short_uuid}.wav')

        # Perintah untuk menjalankan TTS
        command = [
            "tts",
            "--text", text_to_tts,
            "--model_path", params["model_path"],
            "--config_path", params["config_path"],
            "--speaker_idx", speaker_id,
            "--out_path", str(output_file)
        ]

        # Jalankan TTS
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None, f"TTS Error: {result.stderr}"

        return str(output_file), None

    except Exception as e:
        return None, str(e)


@api.route('/health')
class HealthCheck(Resource):
    @api.doc('health_check')
    @api.marshal_with(health_model)
    def get(self):
        """Health check endpoint"""
        return {
            'status': 'healthy',
            'service': 'TTS Indonesia API'
        }


@ns.route('/speakers')
class SpeakersList(Resource):
    @api.doc('get_speakers')
    @api.marshal_list_with(speaker_model)
    def get(self):
        """Mendapatkan daftar pembicara yang tersedia"""
        speakers = [
            {
                "id": "wibowo",
                "name": "Wibowo",
                "description": "Suara jantan berwibawa"
            },
            {
                "id": "ardi",
                "name": "Ardi",
                "description": "Suara lembut dan hangat"
            },
            {
                "id": "gadis",
                "name": "Gadis",
                "description": "Suara perempuan yang merdu"
            },
            {
                "id": "juminten",
                "name": "Juminten",
                "description": "Suara perempuan jawa (bahasa jawa)"
            },
            {
                "id": "asep",
                "name": "Asep",
                "description": "Suara lelaki sunda (bahasa sunda)"
            }
        ]
        return {
            'speakers': speakers,
            'default': default_speaker_name
        }


@ns.route('/languages')
class LanguagesList(Resource):
    @api.doc('get_languages')
    def get(self):
        """Mendapatkan daftar bahasa yang tersedia"""
        return {
            'languages': list(languages.keys()) if languages else ["Indonesian"]
        }


@ns.route('/tts')
class TTSGenerate(Resource):
    @api.doc('generate_tts')
    @api.expect(tts_model)
    @api.produces(['audio/wav'])
    def post(self):
        """
        Generate TTS audio dari teks

        Menghasilkan file audio dari teks dalam bahasa Indonesia menggunakan speaker yang dipilih.
        """
        try:
            data = request.get_json()

            if not data:
                raise BadRequest("Request body harus berisi JSON")

            text = data.get('text')
            if not text:
                raise BadRequest("Parameter 'text' wajib diisi")

            speaker = data.get('speaker', default_speaker_name)
            speed = data.get('speed', 0.8)
            language = data.get('language', 'Indonesian')

            # Validasi speed
            try:
                speed = float(speed)
                if speed < 0.1 or speed > 1.99:
                    speed = 0.8
            except:
                speed = 0.8

            # Generate audio
            audio_file, error = gen_voice(text, speaker, speed, language)

            if error:
                return {
                    'success': False,
                    'error': error
                }, 500

            if not audio_file or not Path(audio_file).exists():
                return {
                    'success': False,
                    'error': 'Gagal menghasilkan audio'
                }, 500

            # Return audio file
            return send_file(
                audio_file,
                mimetype='audio/wav',
                as_attachment=True,
                download_name=Path(audio_file).name
            )

        except BadRequest as e:
            return {
                'success': False,
                'error': str(e)
            }, 400
        except Exception as e:
            return {
                'success': False,
                'error': f'Internal server error: {str(e)}'
            }, 500


@app.route('/', methods=['GET'])
def index():
    """Root endpoint dengan informasi API"""
    return jsonify({
        'service': 'TTS Indonesia API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'speakers': '/api/speakers',
            'languages': '/api/languages',
            'tts': '/api/tts (POST)'
        },
        'author': '__drat',
        'message': 'Energi Semesta Digital © 2024 | 🇮🇩 Untuk Indonesia Jaya!'
    })


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
