# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask import make_response
app = Flask(__name__)


@app.route("/vcard/downloads")
def vrad_download():
    SAMPLE_VCF = u"""
    BEGIN:VCARD
    VERSION:3.0
    PRODID:-//Apple Inc.//iPhone OS 10.2//EN
    N:管理;太郎;;;
    FN: 太郎  管理
    X-PHONETIC-FIRST-NAME:たろう
    X-PHONETIC-LAST-NAME:かんり
    ORG:会社名;
    X-PHONETIC-ORG:会社
    EMAIL;type=INTERNET;type=WORK;type=pref:admin@example.com
    item1.URL;type=pref:https://example.com
    item1.X-ABLabel:_$!<HomePage>!$_
    END:VCARD
    """.strip()
    response = make_response(SAMPLE_VCF)
    response.headers['Content-Type'] = 'text/x-vcard'
    response.headers['Content-Disposition'] = 'attachment; filename=sample.vcf'
    return response    
    

@app.route("/vcard")
def vcard_index():
    template = u"""
    <!DOCTYPE html>
    <html>
    <body>
        <form method="GET" action="/vcard/downloads">
            <input type="submit" value="Download vcards"></input>
        </form>
    </body>
    </html>
    """.strip()
    response = make_response(template)
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')
