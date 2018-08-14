import base64
import hashlib
import random
import string
import time

from flask import Flask, session, render_template, jsonify, request

app = Flask(__name__)

suffix_lengths = [16, 4, 1]
thresholds = [102, 140, 199]  # these numbers are carefully chosen, please don't modify
flags = ['flag{md5_7cfa0da2c09776ae}',
         'flag{sha1_21d0e7b1be5a3cae}',
         'flag{sha256_02938baf7abc9cd3}']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getjob', methods=['POST'])
def getjob():
    suffix = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(max(suffix_lengths))])
    expire = time.time() + 60
    session['suffix'] = suffix
    session['expire'] = expire
    app.logger.info('suffix=%s, expire=%s', suffix, expire)
    return jsonify({
        'suffix': suffix,
        'expire': expire
    })


def difficulty(nonce1, nonce2, algo):
    hash_func = [hashlib.md5, hashlib.sha1, hashlib.sha256][algo]
    hash_digit = [128, 160, 256]
    hash1 = int(hash_func(nonce1).hexdigest(), 16)
    hash2 = int(hash_func(nonce2).hexdigest(), 16)
    hash_xor = hash1 ^ hash2
    d = 0
    for i in range(hash_digit[algo]):
        if (hash_xor >> i) & 1 == 0:
            d += 1
    return d


@app.route('/submitjob', methods=['POST'])
def submitjob():
    try:
        nonce1 = base64.b64decode(request.form['nonce1'])
        nonce2 = base64.b64decode(request.form['nonce2'])
        coin = int(request.form['coin'])
    except:
        return jsonify({
            'success': False,
            'info': 'input is not valid'
        })
    if 'expire' not in session or session['expire'] < time.time():
        return jsonify({
            'success': False,
            'info': 'job expired or does not exist'
        })
    elif nonce1 == nonce2:
        return jsonify({
            'success': False,
            'info': 'nonce should not be the same'
        })
    elif coin not in [0, 1, 2]:
        return jsonify({
            'success': False,
            'info': 'coin variant does not exist'
        })
    else:
        suffix = session['suffix'].encode()[:suffix_lengths[coin]]
        diff = difficulty(nonce1 + suffix, nonce2 + suffix, coin)
        if coin == 0 and diff == 128:
            return jsonify({
                'success': False,
                'info': "Don't trick me by MD5 collisions!"
            })
        if diff >= thresholds[coin]:
            return jsonify({
                'success': True,
                'info': flags[coin]
            })
        else:
            return jsonify({
                'success': True,
                'info': format(
                    'Your difficulty = %s, target difficulty = %s. Please reach target difficulty to get the flag!'
                    % (diff, thresholds[coin]))
            })


if __name__ == '__main__':
    app.secret_key = '7ed1886a19c920239f3230487573ae94'
    app.run(threaded=True)
