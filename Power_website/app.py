from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = 'powerlifting.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si la tabla existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lifts'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            cursor.execute('''
                CREATE TABLE lifts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    body_weight REAL NOT NULL,
                    squat REAL NOT NULL,
                    bench REAL NOT NULL,
                    deadlift REAL NOT NULL,
                    weight_category TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Insertar datos de prueba
            test_data = [
                ('Juan', 75.5, 120, 90, 150, '70-80kg', datetime.now().isoformat()),
                ('Ana', 62.3, 95, 65, 120, '60-70kg', datetime.now().isoformat())
            ]
            cursor.executemany('''
                INSERT INTO lifts (name, body_weight, squat, bench, deadlift, weight_category, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', test_data)
            
            conn.commit()
            print("Base de datos inicializada con datos de prueba")
        
        conn.close()
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        raise

def determine_weight_category(body_weight):
    if body_weight < 60: return "-60kg"
    elif body_weight < 70: return "60-70kg"
    elif body_weight < 80: return "70-80kg"
    elif body_weight < 90: return "80-90kg"
    elif body_weight < 100: return "90-100kg"
    else: return "+100kg"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/lifts', methods=['GET'])
def get_lifts():
    category = request.args.get('category', 'all')
    print(f"\n🔍 Filtro solicitado: {category}")  # Debug
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if category == 'all':
            cursor.execute('SELECT * FROM lifts ORDER BY created_at DESC')
        else:
            # Asegúrate que los valores coincidan exactamente con los de tu frontend
            category_mapping = {
                "-60": "-60kg",
                "60-70": "60-70kg",
                "70-80": "70-80kg",
                "80-90": "80-90kg",
                "90-100": "90-100kg",
                "+100": "+100kg"
            }
            actual_category = category_mapping.get(category, category)
            
            cursor.execute('''
                SELECT * FROM lifts 
                WHERE weight_category = ? 
                ORDER BY created_at DESC
            ''', (actual_category,))
        
        lifts = cursor.fetchall()
        print(f"📊 Registros encontrados: {len(lifts)}")  # Debug
        
        lifts_list = [dict(lift) for lift in lifts]
        return jsonify(lifts_list)
        
    except Exception as e:
        print(f"❌ Error en la consulta: {str(e)}")
        return jsonify({"error": str(e)}), 500
        
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')