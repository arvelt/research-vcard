# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask import make_response
import vobject

app = Flask(__name__)
app.config.update({'DEBUG': True })

SAMPLE_VCF4 = u"""
BEGIN:VCARD
VERSION:4.0
UID:urn:uuid:4fbe8971-0bc3-424c-9c26-36c3e1eff6b1
N:太郎４;管理４;;;
FN:管理４太郎４
EMAIL;PID=1.1:admin@example.com
EMAIL;PID=2.1:admin@example.com
TEL;PID=1.1;VALUE=uri:tel:+1-555-555-5555
TEL;PID=2.1;VALUE=uri:tel:+1-666-666-6666
CLIENTPIDMAP:1;urn:uuid:53e374d9-337e-4727-8803-a1e9c14e0556
END:VCARD
""".strip()

SAMPLE_VCF3 = u"""
BEGIN:VCARD
VERSION:3.0
PRODID:-//Apple Inc.//iPhone OS 10.2//EN
N:管理３;太郎３;;;
FN: 太郎３  管理３
X-PHONETIC-FIRST-NAME:たろう
X-PHONETIC-LAST-NAME:かんり
ORG:会社名;
X-PHONETIC-ORG:かいしゃめい
EMAIL;type=INTERNET;type=WORK;type=pref:admin@example.com
item1.URL;type=pref:https://example.com
item1.X-ABLabel:_$!<HomePage>!$_
END:VCARD
""".strip()

SAMPLE_VCF3_multi = u"""
BEGIN:VCARD
VERSION:3.0
PRODID:-//Apple Inc.//iPhone OS 10.2//EN
N:管理1-1;太郎;;;
FN: 太郎1-1 管理
ORG:会社名;
EMAIL;type=WORK:admin@example.com
END:VCARD
BEGIN:VCARD
VERSION:3.0
PRODID:-//Apple Inc.//iPhone OS 10.2//EN
N:管理1-2;太郎;;;
FN: 太郎1-2 管理
ORG:会社名;
EMAIL;type=WORK:admin@example.com
END:VCARD
""".strip()

def get_vcard_from_code():
	v = vobject.vCard()
	v.add('n').value = vobject.vcard.Name(family=u'管理', given=u'太郎')
	v.add('fn').value = '太郎 管理'
	v.add('org').value = [u'株式会社', u'第一営業部', u'部長']
	v.add("bday").value = u'19801201'

	def add_item(v, label, value, _type):
		item = v.add(label)
		item.value = value
		item.type_param = _type
		return item

	def add_address(v):
		adr = v.add("adr")
		adr.value = vobject.vcard.Address(country=u'日本', code=u'111-000', region=u'東京都', city=u'新宿区', street=u'1-1')
		adr.type_param = 'work'
		return v

	add_item(v, 'email', 'admin@example.com', 'work')
	add_item(v, 'tel', '000-000-000', 'cell')
	add_item(v, 'tel', '03-111-111', 'work')
	add_item(v, 'tel', '001-222-222', 'fax')
	add_address(v)

	return v.serialize()

def get_response(vcf):
	response = make_response(vcf)
	response.headers['Content-Type'] = 'text/x-vcard charaset=utf-8'
	response.headers['Content-Disposition'] = 'attachment; filename=sample.vcf'
	#response.headers['Content-length'] = len(vcf)
	return response	

@app.route("/downloads4")
def downloads4():
	return get_response(SAMPLE_VCF4)

@app.route("/downloads3")
def downloads3():
	return get_response(SAMPLE_VCF3)

@app.route("/downloads_code")
def downloads_code():
	return get_response(get_vcard_from_code())

@app.route("/downloads_multiple")
def downloads_multiple():
	return get_response(SAMPLE_VCF3_multi)

@app.route("/")
def vcard_index():
	template = u"""
	<!DOCTYPE html>
	<html>
	<body>
		<form method="GET" action="/downloads3">
			<input type="submit" value="Download a vcard v3"></input>
		</form>
		<form method="GET" action="/downloads4">
			<input type="submit" value="Download a vcard v4"></input>
		</form>
		<form method="GET" action="/downloads_code">
			<input type="submit" value="Download a vcard from code"></input>
		</form>
		<form method="GET" action="/downloads_multiple">
			<input type="submit" value="Download multiple vcards"></input>
		</form>
	</body>
	</html>
	""".strip()
	response = make_response(template)
	return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')
