from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Verileri yükle
def load_data():
    tc_to_gsm = {}
    gsm_to_tc = {}
    
    try:
        # Render'da dosya yolu
        file_path = 'initial.txt'
        
        # Eğer dosya yoksa, örnek veri oluştur
        if not os.path.exists(file_path):
            print("initial.txt dosyası bulunamadı, örnek veri oluşturuluyor...")
            sample_data = """25343514434  5386146644
27773396666  5062647224
23812923336  5053781592
22201408492  5067827064
64762152070  5064370202
33679287892  5364646843
45562507420  5445476709
17798006794  5063567957
12074451510  5059256986
24668539306  5064801657"""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(sample_data)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) >= 2:
                        tc = parts[0].strip()
                        gsm = parts[1].strip()
                        tc_to_gsm[tc] = gsm
                        gsm_to_tc[gsm] = tc
                        
        print(f"Toplam {len(tc_to_gsm)} kayıt yüklendi")
                        
    except Exception as e:
        print(f"Dosya yükleme hatası: {e}")
    
    return tc_to_gsm, gsm_to_tc

# Verileri yükle
TC_TO_GSM, GSM_TO_TC = load_data()

@app.route('/api/innial.php', methods=['GET'])
def innial_api():
    """Ana API endpoint - GET parametreleri ile sorgulama"""
    
    # GET parametrelerini al
    tc = request.args.get('tc', '').strip()
    gsm = request.args.get('gsm', '').strip()
    phone = request.args.get('phone', '').strip()
    numara = request.args.get('numara', '').strip()  # Türkçe parametre
    
    # Önce tc kontrol et
    if tc:
        if tc in TC_TO_GSM:
            return jsonify({
                'success': True,
                'tc': tc,
                'gsm': TC_TO_GSM[tc],
                'message': 'GSM numarası başarıyla bulundu'
            }), 200
        else:
            return jsonify({
                'success': False,
                'tc': tc,
                'message': 'Bu TC numarasına ait GSM bulunamadı'
            }), 404
    
    # Sonra gsm kontrol et
    if gsm:
        if gsm in GSM_TO_TC:
            return jsonify({
                'success': True,
                'gsm': gsm,
                'tc': GSM_TO_TC[gsm],
                'message': 'TC numarası başarıyla bulundu'
            }), 200
        else:
            return jsonify({
                'success': False,
                'gsm': gsm,
                'message': 'Bu GSM numarasına ait TC bulunamadı'
            }), 404
    
    # Phone parametresi ile kontrol et
    if phone:
        if phone in GSM_TO_TC:
            return jsonify({
                'success': True,
                'gsm': phone,
                'tc': GSM_TO_TC[phone],
                'message': 'TC numarası başarıyla bulundu'
            }), 200
        elif phone in TC_TO_GSM:
            return jsonify({
                'success': True,
                'tc': phone,
                'gsm': TC_TO_GSM[phone],
                'message': 'GSM numarası başarıyla bulundu'
            }), 200
        else:
            return jsonify({
                'success': False,
                'phone': phone,
                'message': 'Bu numaraya ait kayıt bulunamadı'
            }), 404
    
    # Numara parametresi ile kontrol et
    if numara:
        if numara in GSM_TO_TC:
            return jsonify({
                'success': True,
                'gsm': numara,
                'tc': GSM_TO_TC[numara],
                'message': 'TC numarası başarıyla bulundu'
            }), 200
        elif numara in TC_TO_GSM:
            return jsonify({
                'success': True,
                'tc': numara,
                'gsm': TC_TO_GSM[numara],
                'message': 'GSM numarası başarıyla bulundu'
            }), 200
        else:
            return jsonify({
                'success': False,
                'numara': numara,
                'message': 'Bu numaraya ait kayıt bulunamadı'
            }), 404
    
    # Hiç parametre yoksa hata döndür
    return jsonify({
        'success': False,
        'message': 'Lütfen tc veya gsm parametresi gönderin',
        'usage': '/api/innial.php?tc=TC_NUMARASI veya /api/innial.php?gsm=GSM_NUMARASI',
        'example_tc': '/api/innial.php?tc=25343514434',
        'example_gsm': '/api/innial.php?gsm=5386146644'
    }), 400

@app.route('/')
def home():
    """Ana sayfa - API bilgileri"""
    return jsonify({
        'api': 'Innial TC-GSM Sorgulama API',
        'version': '1.0',
        'endpoints': {
            '/api/innial.php': {
                'description': 'TC ve GSM sorgulama',
                'params': {
                    'tc': 'TC kimlik numarası',
                    'gsm': 'GSM numarası',
                    'phone': 'Alternatif parametre',
                    'numara': 'Alternatif parametre (Türkçe)'
                },
                'examples': [
                    '/api/innial.php?tc=25343514434',
                    '/api/innial.php?gsm=5386146644'
                ]
            }
        },
        'total_records': len(TC_TO_GSM)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint bulunamadı'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Sunucu hatası oluştu'
    }), 500

if __name__ == '__main__':
    # Render için port ayarı
    port = int(os.environ.get('PORT', 5000))
    print("=" * 50)
    print("Innial API başlatılıyor...")
    print(f"Toplam {len(TC_TO_GSM)} kayıt yüklendi")
    print("=" * 50)
    print("\nKullanım Örnekleri:")
    print(f"  TC sorgula: http://localhost:{port}/api/innial.php?tc=25343514434")
    print(f"  GSM sorgula: http://localhost:{port}/api/innial.php?gsm=5386146644")
    print(f"  Alternatif: http://localhost:{port}/api/innial.php?phone=5386146644")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=False)
