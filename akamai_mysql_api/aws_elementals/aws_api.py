from flask import Flask, jsonify, request,Response
import xmltodict
from bs4 import BeautifulSoup
import xml.dom.minidom

app = Flask(__name__)
  
@app.route("/testapp", methods = ['POST', 'GET'], strict_slashes=False)
def parseRequest():
    content = xmltodict.parse(request.get_data())
    # header("Content-type: text/xml","accept:application/xml")
    print (content)
    # return content
    return jsonify({'data': content})
    # return Response(content, mimetype='text/xml')

@app.route("/live_event", methods = ['POST', 'GET'])
def xml_file_reading():
   domtree = xml.dom.minidom.parse('live_event_341_c.xml')
   live_event = domtree.documentElement
   network_input = live_event.getElementsByTagName('network_input')
   output_group = live_event.getElementsByTagName('output_group')
   uri = network_input[0].getElementsByTagName('uri')[0].childNodes[0].nodeValue
   output_uri = output_group[0].getElementsByTagName('uri')[0].childNodes[0].nodeValue
   output_uri1 = output_group[1].getElementsByTagName('uri')[0].childNodes[0].nodeValue
#    start fetching uri of network_input
# rtmp://173.16.16.24/live/Roopsibnbghgugkhih
   split_uri = uri.rsplit('/',1)
   uri_index_one = split_uri[1]
   uri_index_one = 'Roopsibnbghgugkhih'
   end_point_uri = uri_index_one
   uri_assign = f"{split_uri[0]}/{end_point_uri}"
   network_input[0].getElementsByTagName('uri')[0].childNodes[0].nodeValue = uri_assign


   #    output uri fetch
#    http://p-ep2101752.i.akamaientrypoint.net/2101752/outputkeyassign/master

   split_output_uri = output_uri.rsplit('/',2)
   ouput_uri_key = split_output_uri[-2]
   ouput_uri_key = 'outputkeyassign'
   output_key_assign = f"{split_output_uri[0]}/{ouput_uri_key}/{split_output_uri[2]}"
   output_group[0].getElementsByTagName('uri')[0].childNodes[0].nodeValue = output_key_assign


   #output_uri_fetch 2
#    /data/mnt/storage/FTP/PW/$d$/keychabge-$t$
   split_output_uri1 = output_uri1.rsplit('/',1)
   split_output_uri1_key = split_output_uri1[1].split('-')
   split_output_uri1_key_get = split_output_uri1_key[0]
   split_output_uri1_key_get ='keychabge'
   output_1_uri = f"{split_output_uri1[0]}/{split_output_uri1_key_get}-{split_output_uri1_key[1]}"
   output_group[1].getElementsByTagName('uri')[0].childNodes[0].nodeValue = output_1_uri


   domtree.writexml(open('live_event_341_c.xml','w'))
   return jsonify({'data': "hello world"})
    
if __name__ == '__main__':
  
    app.run(debug = True)
    xml_file_reading()