from flask import Flask, request, jsonify, json
from flask_cors import CORS
from flask_mysqldb import MySQL
from time import sleep
import requests
import jwt
import datetime

app = Flask(__name__)

app.secret_key = "WA#SR#RG(TU/$WQEWREETYTRGFDG3489234720574323#$%/(/&%$#&/"
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS HEADERS"] = "Content-Type"

# Mysql Connection
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_PORT"] = 3306
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "escuela"
mysql = MySQL(app)

def fixStringClient(string):
    fixed = str(string).replace("'", "").replace("*", "").replace('"', "").replace("+", "").replace("|", "").replace("%", "").replace("$", "").replace("&", "").replace("=", "").replace("?", "").replace('¡', "").replace("\a", "").replace("<", "").replace(">", "").replace("/", "").replace("[", "").replace("]", "").replace("(", "").replace("]", "").replace("´", "").replace(",", "").replace("!", "").replace("\n", "")
    return fixed

@app.route('/')
def index():
    return "Hii api :V"

@app.route('/api/v1/curso', methods=['GET', 'POST', 'PUT', 'DELETE'])
def cursoController():
    if request.method == 'GET':
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM cursos")
        data = con.fetchall()
        con.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'profesor_encargado': col[1],
                'grado': col[2]
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'profesor_encargado': -1,
                'grado': -1
            })
        return jsonify(jsonResponse), 200
        
    elif request.method == 'POST':
        datares = request.get_json(force=True)
        profesor_encargado = fixStringClient(datares['profesor_encargado'])
        grado = fixStringClient(datares['grado'])
        con = mysql.connection.cursor()
        con.execute("INSERT INTO cursos(profesor_encargado, grado) VALUES(%s, %s)",(profesor_encargado,grado,))
        mysql.connection.commit()
        con.close()

        con2 = mysql.connection.cursor()
        con2.execute("SELECT * FROM cursos")
        data = con2.fetchall()
        con2.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'profesor_encargado': col[1],
                'grado': col[2]
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'profesor_encargado': -1,
                'grado': -1
            })
        return jsonify(jsonResponse), 200

    elif request.method == 'PUT':
        datares = request.get_json(force=True)
        idC = fixStringClient(datares['id'])
        profesor_encargado = fixStringClient(datares['profesor_encargado'])
        grado = fixStringClient(datares['grado'])
        con = mysql.connection.cursor()
        con.execute("UPDATE cursos SET profesor_encargado = %s, grado = %s WHERE id = %s",(profesor_encargado, grado, idC,))
        mysql.connection.commit()
        con.close()

        con2 = mysql.connection.cursor()
        con2.execute("SELECT * FROM cursos")
        data = con2.fetchall()
        con2.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'profesor_encargado': col[1],
                'grado': col[2]
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'profesor_encargado': -1,
                'grado': -1
            })
        return jsonify(jsonResponse), 200
    elif request.method == 'DELETE':
        datares = request.get_json(force=True)
        idC = fixStringClient(datares['id'])
        con = mysql.connection.cursor()
        con.execute("DELETE FROM cursos WHERE id = %s",(idC,))
        mysql.connection.commit()
        con.close()

        con2 = mysql.connection.cursor()
        con2.execute("SELECT * FROM cursos")
        data = con2.fetchall()
        con2.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'profesor_encargado': col[1],
                'grado': col[2]
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'profesor_encargado': -1,
                'grado': -1
            })
        return jsonify(jsonResponse), 200

@app.route('/api/v1/cursoestudiante/<id>', methods=['GET'])
def cursoEstudiante(id):
    con = mysql.connection.cursor()
    con.execute("SELECT e.nombres AS nombre_estudiante, c.grado, p.nombre AS nombre_profesor FROM cursos c, estudiantes e, profesores p WHERE p.id = c.profesor_encargado AND documento_identidad = %s",(id,))
    data = con.fetchall()
    con.close()
    
    jsonResponse = []
    for col in data:
        jsonResponse.append({
            'nombre_estudiante': col[0],
            'grado': col[1],
            'nombre_profesor': col[2]
        })

    if len(jsonResponse) == 0:
        jsonResponse.append({
            'nombre_estudiante': 'Not found data',
            'grado': -1,
            'nombre_profesor': 'Not found data'
        })

    return jsonify(jsonResponse), 200

@app.route('/api/v1/directorginfo/<id>', methods=['GET'])
def directorGInfo(id):
    con = mysql.connection.cursor()
    con.execute("SELECT p.nombre AS nombre_profesor, p.asignatura, c.grado AS grado_encargado FROM profesores p, cursos c WHERE c.profesor_encargado = p.id and p.id = %s",(id,))
    data = con.fetchall()
    con.close()
    
    jsonResponse = []
    for col in data:
        jsonResponse.append({
            'nombre_profesor': col[0],
            'asignatura': col[1],
            'grado_encargado': col[2]
        })

    if len(jsonResponse) == 0:
        jsonResponse.append({
            'nombre_profesor': 'Not found data',
            'asignatura': 'Not found data',
            'grado_encargado': -1
        })

    return jsonify(jsonResponse), 200

@app.route('/api/v1/estudiante', methods=['GET', 'POST', 'PUT', 'DELETE'])
def estudianteController():
    if request.method == 'GET':
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM estudiantes")
        data = con.fetchall()
        con.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'nombres': col[1],
                'curso': col[2],
                'documento_identidad': col[3]
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'nombres': 'Not found data',
                'curso': -1,
                'documento_identidad': -1
            })
        return jsonify(jsonResponse), 200
        
    elif request.method == 'POST':
        datares = request.get_json(force=True)
        nombres = fixStringClient(datares['nombres'])
        curso = fixStringClient(datares['curso'])
        documento_identidad = fixStringClient(datares['documento_identidad'])
        con = mysql.connection.cursor()
        con.execute("INSERT INTO estudiantes(nombres, curso, documento_identidad) VALUES(%s, %s, %s)",(nombres, curso, documento_identidad,))
        mysql.connection.commit()
        con.close()

        con2 = mysql.connection.cursor()
        con2.execute("SELECT * FROM estudiantes")
        data = con2.fetchall()
        con2.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'nombres': col[1],
                'curso': col[2],
                'documento_identidad': col[3]
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'nombres': 'Not found data',
                'curso': -1,
                'documento_identidad': -1
            })
        return jsonify(jsonResponse), 200

    elif request.method == 'PUT':
        datares = request.get_json(force=True)
        nombres = fixStringClient(datares['nombres'])
        id = fixStringClient(datares['id'])
        curso = fixStringClient(datares['curso'])
        documento_identidad = fixStringClient(datares['documento_identidad'])
        con = mysql.connection.cursor()
        con.execute("UPDATE estudiantes SET nombres = %s, curso = %s, documento_identidad = %s WHERE id = %s",(nombres, curso, documento_identidad, id,))
        mysql.connection.commit()
        con.close()

        con2 = mysql.connection.cursor()
        con2.execute("SELECT * FROM estudiantes")
        data = con2.fetchall()
        con2.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'nombres': col[1],
                'curso': col[2],
                'documento_identidad': col[3]
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'nombres': 'Not found data',
                'curso': -1,
                'documento_identidad': -1
            })
        return jsonify(jsonResponse), 200

    elif request.method == 'DELETE':
        datares = request.get_json(force=True)
        idC = fixStringClient(datares['id'])
        con = mysql.connection.cursor()
        con.execute("DELETE FROM estudiantes WHERE id = %s",(idC,))
        mysql.connection.commit()
        con.close()

        con2 = mysql.connection.cursor()
        con2.execute("SELECT * FROM estudiantes")
        data = con2.fetchall()
        con2.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'nombres': col[1],
                'curso': col[2],
                'documento_identidad': col[3]
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'nombres': 'Not found data',
                'curso': -1,
                'documento_identidad': -1
            })
        return jsonify(jsonResponse), 200

@app.route('/api/v1/materias', methods=['GET', 'POST', 'PUT', 'DELETE'])
def materiasController():
    if request.method == 'GET':
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM materias")
        data = con.fetchall()
        con.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'nombre_materia': col[1],
                'profesor': col[2]
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'nombre_materia': 'Not found data',
                'profesor': -1
            })
        return jsonify(jsonResponse), 200
        
    elif request.method == 'POST':
        datares = request.get_json(force=True)
        nombre_materia = fixStringClient(datares['nombre_materia'])
        profesor = fixStringClient(datares['profesor'])
        con = mysql.connection.cursor()
        con.execute("INSERT INTO materias(nombre_materia, profesor) VALUES(%s, %s)",(nombre_materia, profesor,))
        mysql.connection.commit()
        con.close()

        con2 = mysql.connection.cursor()
        con2.execute("SELECT * FROM materias")
        data = con2.fetchall()
        con2.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'nombre_materia': col[1],
                'profesor': col[2]
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'nombre_materia': 'Not found data',
                'profesor': -1
            })
        return jsonify(jsonResponse), 200

    elif request.method == 'PUT':
        datares = request.get_json(force=True)
        id = fixStringClient(datares['id'])
        nombre_materia = fixStringClient(datares['nombre_materia'])
        profesor = fixStringClient(datares['profesor'])
        con = mysql.connection.cursor()
        con.execute("UPDATE materias SET nombre_materia = %s, profesor = %s WHERE id = %s",(nombre_materia, profesor, id,))
        mysql.connection.commit()
        con.close()

        con2 = mysql.connection.cursor()
        con2.execute("SELECT * FROM materias")
        data = con2.fetchall()
        con2.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'nombre_materia': col[1],
                'profesor': col[2]
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'nombre_materia': 'Not found data',
                'profesor': -1
            })
        return jsonify(jsonResponse), 200

    elif request.method == 'DELETE':
        datares = request.get_json(force=True)
        id = fixStringClient(datares['id'])
        try:
            con = mysql.connection.cursor()
            con.execute("DELETE FROM materias WHERE id = %s",(id,))
            mysql.connection.commit()
            con.close()

            con2 = mysql.connection.cursor()
            con2.execute("SELECT * FROM materias")
            data = con2.fetchall()
            con2.close()
            jsonResponse = []
            for col in data:
                jsonResponse.append({
                    'id': col[0],
                    'nombre_materia': col[1],
                    'profesor': col[2]
                })
            if len(jsonResponse) == 0:
                jsonResponse.append({
                    'id': -1,
                    'nombre_materia': 'Not found data',
                    'profesor': -1
                })
        except :
            con.close()
            con2 = mysql.connection.cursor()
            con2.execute("SELECT * FROM materias")
            data = con2.fetchall()
            con2.close()
            jsonResponse = []
            for col in data:
                jsonResponse.append({
                    'id': col[0],
                    'nombre_materia': col[1],
                    'profesor': col[2]
                })
            if len(jsonResponse) == 0:
                jsonResponse.append({
                    'id': -1,
                    'nombre_materia': 'Not found data',
                    'profesor': -1
                })
        
            return jsonify(jsonResponse), 200
        return jsonify(jsonResponse), 200

@app.route('/api/v1/notas', methods=['GET', 'POST', 'PUT', 'DELETE'])
def notasController():
    if request.method == 'GET':
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM notas")
        data = con.fetchall()
        con.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'nota1': col[1],
                'nota2': col[2],
                'nota3': col[3],
                'nota4': col[4],
                'estudiante': col[5],
                'materia': col[6],
                'promedio': (col[1] + col[2] + col[3] + col[4]) / 4
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'nota1': -1,
                'nota2': -1,
                'nota3': -1,
                'nota4': -1,
                'estudiante': -1,
                'materia': -1,
                'promedio': -1
            })
        return jsonify(jsonResponse), 200
        
    elif request.method == 'POST':
        datares = request.get_json(force=True)
        nota1 = fixStringClient(datares['nota1'])
        nota2 = fixStringClient(datares['nota2'])
        nota3 = fixStringClient(datares['nota3'])
        nota4 = fixStringClient(datares['nota4'])
        estudiante = fixStringClient(datares['estudiante'])
        materia = fixStringClient(datares['materia'])
        con = mysql.connection.cursor()
        con.execute("INSERT INTO notas(nota1, nota2, nota3, nota4, estudiante, materia) VALUES(%s,%s,%s,%s, %s, %s)",(nota1, nota2, nota3, nota4, estudiante, materia,))
        mysql.connection.commit()
        con.close()

        con2 = mysql.connection.cursor()
        con2.execute("SELECT * FROM notas")
        data = con2.fetchall()
        con2.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'nota1': col[1],
                'nota2': col[2],
                'nota3': col[3],
                'nota4': col[4],
                'estudiante': col[5],
                'materia': col[6],
                'promedio': (col[1] + col[2] + col[3] + col[4]) / 4
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'nota1': -1,
                'nota2': -1,
                'nota3': -1,
                'nota3': -1,
                'estudiante': -1,
                'materia': -1,
                'promedio': -1
            })
        return jsonify(jsonResponse), 200

    elif request.method == 'PUT':
        datares = request.get_json(force=True)
        id = fixStringClient(datares['id'])
        nota1 = fixStringClient(datares['nota1'])
        nota2 = fixStringClient(datares['nota2'])
        nota3 = fixStringClient(datares['nota3'])
        nota4 = fixStringClient(datares['nota4'])
        estudiante = fixStringClient(datares['estudiante'])
        materia = fixStringClient(datares['materia'])
        con = mysql.connection.cursor()
        con.execute("UPDATE notas SET nota1 = %s, nota2 = %s, nota3 = %s, nota4 = %s, estudiante = %s, materia = %s WHERE id = %s",(nota1, nota2, nota3, nota4, estudiante, materia, id,))
        mysql.connection.commit()
        con.close()

        con2 = mysql.connection.cursor()
        con2.execute("SELECT * FROM notas")
        data = con2.fetchall()
        con2.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'nota1': col[1],
                'nota2': col[2],
                'nota3': col[3],
                'nota4': col[4],
                'estudiante': col[5],
                'materia': col[6],
                'promedio': (col[1] + col[2] + col[3] + col[4]) / 4
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'nota1': -1,
                'nota2': -1,
                'nota3': -1,
                'nota3': -1,
                'estudiante': -1,
                'materia': -1,
                'promedio': -1
            })
        return jsonify(jsonResponse), 200

    elif request.method == 'DELETE':
        datares = request.get_json(force=True)
        id = fixStringClient(datares['id'])
        try:
            con = mysql.connection.cursor()
            con.execute("DELETE FROM notas WHERE id = %s",(id,))
            mysql.connection.commit()
            con.close()
            
            con2 = mysql.connection.cursor()
            con2.execute("SELECT * FROM notas")
            data = con2.fetchall()
            con2.close()
            jsonResponse = []
            for col in data:
                jsonResponse.append({
                    'id': col[0],
                    'nota1': col[1],
                    'nota2': col[2],
                    'nota3': col[3],
                    'nota4': col[4],
                    'estudiante': col[5],
                    'materia': col[6],
                    'promedio': (col[1] + col[2] + col[3] + col[4]) / 4
                })
            if len(jsonResponse) == 0:
                jsonResponse.append({
                    'id': -1,
                    'nota1': -1,
                    'nota2': -1,
                    'nota3': -1,
                    'nota3': -1,
                    'estudiante': -1,
                    'materia': -1,
                    'promedio': -1
                })
        except :
            con.close()
            con2 = mysql.connection.cursor()
            con2.execute("SELECT * FROM notas")
            data = con2.fetchall()
            con2.close()
            jsonResponse = []
            for col in data:
                jsonResponse.append({
                    'id': col[0],
                    'nota1': col[1],
                    'nota2': col[2],
                    'nota3': col[3],
                    'nota4': col[4],
                    'estudiante': col[5],
                    'materia': col[6],
                    'promedio': (col[1] + col[2] + col[3] + col[4]) / 4
                })
            if len(jsonResponse) == 0:
                jsonResponse.append({
                    'id': -1,
                    'nota1': -1,
                    'nota2': -1,
                    'nota3': -1,
                    'nota3': -1,
                    'estudiante': -1,
                    'materia': -1,
                    'promedio': -1
                })
        
            return jsonify(jsonResponse), 200
        return jsonify(jsonResponse), 200

@app.route('/api/v1/notasestudiantes/<id>', methods=['GET'])
def notasEstudiantes(id):
    con = mysql.connection.cursor()
    con.execute("SELECT e.nombres AS nombre_estudiante, n.nota1, n.nota2, n.nota3, n.nota4, m.nombre_materia, p.nombre AS profesor_encargado FROM estudiantes e, notas n, profesores p, materias m WHERE e.id = n.estudiante AND p.id = m.profesor AND n.materia = m.id AND e.documento_identidad = %s",(id,))
    data = con.fetchall()
    con.close()
    
    jsonResponse = []
    for col in data:
        jsonResponse.append({
            'nombre_estudiante': col[0],
            'nota1': col[1],
            'nota2': col[2],
            'nota3': col[3],
            'nota4': col[4],
            'nombre_materia': col[5],
            'profesor_encargado': col[6]
        })

    if len(jsonResponse) == 0:
        jsonResponse.append({
            'nombre_estudiante': 'Not found data',
            'nota1': -1,
            'nota2': -1,
            'nota3': -1,
            'nota4': -1,
            'nombre_materia': 'Not found data',
            'profesor_encargado': 'Not found data'
        })

    return jsonify(jsonResponse), 200

@app.route('/api/v1/profesor', methods=['GET', 'POST', 'PUT', 'DELETE'])
def profesorController():
    if request.method == 'GET':
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM profesores")
        data = con.fetchall()
        con.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'nombre': col[1],
                'asignatura': col[2]
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'nombre': 'Not found data',
                'asignatura': 'Not found data'
            })
        return jsonify(jsonResponse), 200
        
    elif request.method == 'POST':
        datares = request.get_json(force=True)
        nombre = fixStringClient(datares['nombre'])
        asignatura = fixStringClient(datares['asignatura'])
        con = mysql.connection.cursor()
        con.execute("INSERT INTO profesores(nombre, asignatura) VALUES(%s,%s)",(nombre, asignatura,))
        mysql.connection.commit()
        con.close()

        con2 = mysql.connection.cursor()
        con2.execute("SELECT * FROM profesores")
        data = con2.fetchall()
        con2.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'nombre': col[1],
                'asignatura': col[2]
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'nombre': 'Not found data',
                'asignatura': 'Not found data'
            })
        return jsonify(jsonResponse), 200

    elif request.method == 'PUT':
        datares = request.get_json(force=True)
        id = fixStringClient(datares['id'])
        nombre = fixStringClient(datares['nombre'])
        asignatura = fixStringClient(datares['asignatura'])
        con = mysql.connection.cursor()
        con.execute("UPDATE profesores SET nombre = %s, asignatura = %s WHERE id = %s",(nombre, asignatura, id,))
        mysql.connection.commit()
        con.close()

        con2 = mysql.connection.cursor()
        con2.execute("SELECT * FROM profesores")
        data = con2.fetchall()
        con2.close()
        jsonResponse = []
        for col in data:
            jsonResponse.append({
                'id': col[0],
                'nombre': col[1],
                'asignatura': col[2]
            })
        if len(jsonResponse) == 0:
            jsonResponse.append({
                'id': -1,
                'nombre': 'Not found data',
                'asignatura': 'Not found data'
            })
        return jsonify(jsonResponse), 200

    elif request.method == 'DELETE':
        datares = request.get_json(force=True)
        id = fixStringClient(datares['id'])
        try:
            con = mysql.connection.cursor()
            con.execute("DELETE FROM profesores WHERE id = %s",(id,))
            mysql.connection.commit()
            con.close()
            
            con2 = mysql.connection.cursor()
            con2.execute("SELECT * FROM profesores")
            data = con2.fetchall()
            con2.close()
            jsonResponse = []
            for col in data:
                jsonResponse.append({
                    'id': col[0],
                    'nombre': col[1],
                    'asignatura': col[2]
                })
            if len(jsonResponse) == 0:
                jsonResponse.append({
                    'id': -1,
                    'nombre': 'Not found data',
                    'asignatura': 'Not found data'
                })
        except :
            con.close()
            con2 = mysql.connection.cursor()
            con2.execute("SELECT * FROM profesores")
            data = con2.fetchall()
            con2.close()
            jsonResponse = []
            for col in data:
                jsonResponse.append({
                    'id': col[0],
                    'nombre': col[1],
                    'asignatura': col[2]
                })
            if len(jsonResponse) == 0:
                jsonResponse.append({
                    'id': -1,
                    'nombre': 'Not found data',
                    'asignatura': 'Not found data'
                })
        
            return jsonify(jsonResponse), 200
        return jsonify(jsonResponse), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='localhost')