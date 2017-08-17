# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask import make_response
app = Flask(__name__)


SAMPLE_VCF = u"""
BEGIN:VCARD
VERSION:3.0
PRODID:-//Apple Inc.//iPhone OS 10.2//EN
N:管理;太郎５;;;
FN: 太郎５  管理
X-PHONETIC-FIRST-NAME:たろう
X-PHONETIC-LAST-NAME:かんり
ORG:会社名;
X-PHONETIC-ORG:かいしゃめい
EMAIL;type=INTERNET;type=WORK;type=pref:admin@example.com
item1.URL;type=pref:https://example.com
item1.X-ABLabel:_$!<HomePage>!$_
UID:5743e92e-8a6a-4d6d-a095-6dfdd51543d4
END:VCARD
""".strip()

@app.route("/downloads")
def vrad_download():
	response = make_response(SAMPLE_VCF)
	response.headers['Content-Type'] = 'text/x-vcard'
	response.headers['Content-Disposition'] = 'attachment; filename=sample.vcf'
#	response.headers['Content-length'] = len(SAMPLE_VCF)
	return response


@app.route("/")
def vcard_index():
	template = u"""
	<!DOCTYPE html>
	<html>
	<body>
		<form method="GET" action="/downloads">
			<input type="submit" value="Download vcards"></input>
		</form>
	</body>
	</html>
	""".strip()
	response = make_response(template)
	return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')
