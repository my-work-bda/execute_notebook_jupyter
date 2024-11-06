from flask import Flask, request, jsonify, send_file
import paramiko
import base64
import io
from datetime import datetime

app = Flask(__name__)

# Base64-encoded username and password
encoded_pass = 'c3Bhcms='  

# Decode the Base64-encoded credentials
username = base64.b64decode(encoded_pass).decode('utf-8')
password = base64.b64decode(encoded_pass).decode('utf-8')

def filter_error_message(output):
    error_start = "raise_for_execution_errors\n    raise error\npapermill.exceptions.PapermillExecutionError: \n---------------------------------------------------------------------------\n"
    if error_start in output:
        return output.split(error_start, 1)[1]
    return output

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'status': 'success',
        'message': 'API for executing Jupyter notebook v1'
    })

@app.route('/run_job', methods=['POST'])
def run_job():
    # Mengambil data JSON dari request
    data = request.get_json()

    # Validasi input
    if not data:
        return jsonify({'status': 'error', 'message': 'Data JSON tidak ditemukan.'}), 400

    hostname = data.get('hostname', '').strip()
    port = data.get('port', 0)
    notebook_path = data.get('notebook_path', '/home/jupyter/project_api/note.ipynb').strip()

    if not hostname:
        return jsonify({'status': 'error', 'message': 'Hostname harus diisi.'}), 400
    if not port:
        return jsonify({'status': 'error', 'message': 'Port harus diisi.'}), 400
    if not notebook_path:
        return jsonify({'status': 'error', 'message': 'Notebook path harus diisi.'}), 400

    output_path = data.get('output_path', f'/home/jupyter/tmp/{notebook_path.split("/")[-1]}')
    output_path = output_path.split('.ipynb')[0] + f'_{datetime.now().strftime("%Y%m%d_%H%M%S")}.ipynb'
    
    parameter = data.get('parameter', '').strip()

    try:
        # Membuat objek SSHClient
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=port, username=username, password=password)

        # Perintah yang akan dieksekusi dengan tambahan opsi --log-output
        command = f'papermill {notebook_path} {output_path} {parameter}'
        app.logger.info(f"Eksekusi perintah: {command}")

        # Eksekusi perintah di server remote dengan get_pty=True untuk interaksi
        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)

        # Tunggu hingga perintah selesai dan dapatkan exit status
        exit_status = stdout.channel.recv_exit_status()
        
        # Membaca output dan error
        output_stdout = stdout.read().decode()
        output_stderr = stderr.read().decode()

        # Response
        if exit_status == 0:
            app.logger.info('Perintah berhasil dijalankan.')
            return jsonify({
                'status': 'success',
                'output': output_path,
                'message': 'Notebook berhasil dieksekusi.'
            }), 200
        else:
            app.logger.error(f'Perintah gagal dengan exit status {exit_status}')
            filtered_output = filter_error_message(output_stderr)
            return jsonify({
                'status': 'error ',
                'output': filtered_output
            }), 400
    
    except Exception as e:
        app.logger.error(f'Terjadi kesalahan: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500

    finally:
        # Tutup koneksi SSH
        ssh.close()
        app.logger.info("Koneksi SSH ditutup.")

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
