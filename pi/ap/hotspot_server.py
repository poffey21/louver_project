"""
This will serve as a hotspot that receives traffic, and
requests
- SSID (list only ones available)
    sudo iwlist wlan0 scanning | egrep 'Cell |Encryption|Quality|Last beacon|ESSID'
- Password
"""
import urllib

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect

from wireless import Wireless


"""
Example.  http://na1r.services.adobe.com:5000/blah?query=value#hash
"""

app = Flask(__name__)
wireless = Wireless()

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    next_url = request.values.get('next', request.referrer)
    if request.method == 'POST':
        # Store ssid & password in file
        # queue wireless connection
        #
        wireless.connect(
            ssid=request.form['ssid'],
            password=request.form['ssid'],
        )
        return redirect(next_url)
    return render_template('hotspot.html', next=next)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    path = urllib.quote('{}'.format(request.url))
    return redirect('http://beta.ten08.local:5000/setup?next=' + path)
    # return 'You want path: %s' % (path)

if __name__ == '__main__':
    app.run()
