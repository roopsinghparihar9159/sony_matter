from flask import Flask, jsonify, request,Response
import xmltodict
from bs4 import BeautifulSoup
# from flask import Flask, request
import xml.dom.minidom

app = Flask(__name__)

@app.route("/xml", methods = ['POST', 'GET'])
def xml_file_reading():

   domtree = xml.dom.minidom.parse('people.xml')
   group = domtree.documentElement
   people = group.getElementsByTagName('person')
   for person in people:
        print(f"-- Person {person.getAttribute('id')} --")
        name = person.getElementsByTagName('name')[0].childNodes[0].nodeValue
        age = person.getElementsByTagName('age')[0].childNodes[0].nodeValue
        weight = person.getElementsByTagName('weight')[0].childNodes[0].nodeValue
        height = person.getElementsByTagName('height')[0].childNodes[0].nodeValue

        print(f"Name: {name}")
        print(f"Age: {age}")
        print(f"Weight: {weight}")
        print(f"Height: {height}")
   people[0].getElementsByTagName('name')[0].childNodes[0].nodeValue = "Roopsingh"
   people[0].setAttribute("id","200")
   people[0].setAttribute("newattr","Hello")
   domtree.writexml(open('people.xml','w'))
   return jsonify({'data': "hello world"})
   
@app.route("/live_event", methods = ['POST', 'GET'])
def read_live_event_file():
    domtree = xml.dom.minidom.parse('live_event_341_c.xml')
    live_event = domtree.documentElement
    # input1 = live_event.getElementsByTagName('input')
    network_input = live_event.getElementsByTagName('network_input')
    # for network in network_input:
    #     check_server_certificate = network.getElementsByTagName('check_server_certificate')[0].childNodes[0].nodeValue
    #     enable_fec_rx = network.getElementsByTagName('enable_fec_rx')[0].childNodes[0].nodeValue
    #     quad = network.getElementsByTagName('quad')[0].childNodes[0].nodeValue
    #     uri = network.getElementsByTagName('uri')[0].childNodes[0].nodeValue
        
    #     print(f"check_server_certificate: {check_server_certificate}")
    #     print(f"enable_fec_rx: {enable_fec_rx}")
    #     print(f"quad: {quad}")
    #     print(f"uri: {uri}")
    uri = network_input[0].getElementsByTagName('uri')[0].childNodes[0].nodeValue
    split_uri = uri.rsplit('/',1)
    # print('split_uri',split_uri[0])
    # print('split_uri',split_uri[1])
    uri_index_one = split_uri[1]
    uri_index_one = 'Roopsibnbghgugkhih'
    end_point_uri = uri_index_one
    uri_assign = f"{split_uri[0]}/{end_point_uri}"
    print('uri_assign',uri_assign)
    network_input[0].getElementsByTagName('uri')[0].childNodes[0].nodeValue = uri_assign
    domtree.writexml(open('live_event_341_c.xml','w'))
    return jsonify({'data': "hello world"})

    
if __name__ == '__main__':
    app.run(debug = True)