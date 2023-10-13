from flask import Flask, request, Response
from PIL import Image
import io

app = Flask(__name__)
app.debug=True

@app.route('/altb-thumb', methods=['GET'])
def altbThumb():
	if(request.method == 'GET'): pass
	fn=request.args.get('fn')
	width=int(request.args.get('w'))
	height=int(request.args.get('h'))
	left,top,right,bottom=request.args.get('crop').split(',')
	quality=request.args.get('q')
	format=request.args.get('format')
	area=(int(left),int(top),int(right),int(bottom))
	img=Image.open(fn)
	img=img.crop(area)
	img=img.resize((width,height))
	buf = io.BytesIO()
	img.save(buf, format=format,quality=quality)
	byte_im = buf.getvalue()
	resp = Response(response=byte_im, status=200,  mimetype="image/jpg")
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=88)