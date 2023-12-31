from flask import Flask, make_response, jsonify
import ssl
import socket

SUCCESSFUL_RESPONSE = 200
HOSTNAME = socket.gethostname()

total_requests_served_since_startup = 0

app = Flask(__name__)

@app.route('/health')
def health():
    global total_requests_served_since_startup
    total_requests_served_since_startup += 1
    ret = {}
    ret['response'] = 'healthy'
    ret['hostname'] = HOSTNAME
    ret['inside_function'] = f"{__file__}['{health.__name__}']"
    return make_response(jsonify(ret), SUCCESSFUL_RESPONSE)

@app.route('/count')
def count():
    global total_requests_served_since_startup
    total_requests_served_since_startup += 1
    ret = {}
    ret['hostname'] = HOSTNAME
    ret['total_requests_count'] = total_requests_served_since_startup
    ret['inside_function'] = f"{__file__}['{count.__name__}']"
    return make_response(jsonify(ret), SUCCESSFUL_RESPONSE)


if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('venus-srv.com.crt', 'venus-srv.com.key')
    app.run('0.0.0.0', {{TGW_COUNTING_TLS_PORT}}, ssl_context=context)