from flask import Flask, render_template, request, jsonify, render_template
from flask import request

app = Flask(__name__)

# List of stores. Here we are using dictionary as later we will save them in json.
# Each store has 2 key-value pairs: name and items. Then items (also like a store has a list of features).
# Items have 2 key-value pairs: name and price.

#json uses only double quotes
stores = [
             {'name': 'My Apple store',
              'items' : [
                  {
                      'name': 'Phone',
                      'price': 15
                  }
              ]
              }
]
@app.route('/')
def home():
    return render_template('index.html')
#Post comes from users. when they want to post smth. i.e post(item)
#Get store, users use to get information.

#POST /store data:{name:} By default method is GET
@app.route('/store', methods = ['POST']) # http//127.0.0.1:5000/store/store_name
def create_store():
    #request is data which was made through /store endpoint, name of the store. It is json file
    request_data = request.get_json() # translates to python dictionary
    new_store = {
        'name': request_data['name'], #already translated to dict so can access it via the this
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


#GET /store/<string:name>
@app.route('/store/<string:name>') # http//127.0.0.1:5000/store/store_name
def get_store(name):
    #Iterate through stores, if name matches, return it,
    # if none matches return an error
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message' : 'No such store'})

#GET /store/
@app.route('/store')
def get_stores():
    return jsonify({'stores' : stores})

#POST /store/<string:name>/item
#User posts name and item. We know the name of the store, iterate trough stores, find suitable,
#Put there our item, which is also sent to us with post request.
#That post request has item's name and price (or may not if error)
@app.route('/store/<string:name>/item', methods = ['POST'])
def create_item_in_store(name):
    request_data = request.get_json()  #here we will have item['name'] and item['price']
    #We loop through all store and if not find existing we print: store not found message.
    for store in stores:
        if store['name'] == name:
            new_item = {
             'name': request_data['name'],  # already translated to dict so can access it via the this
             'price': request_data['price']
            }
            store['items'].append(new_item) #appending to 'items' : [name, price]
            return jsonify(new_item) # or return jsonify(store)
    return jsonify({'message': 'No such store'})


# GET ('/store/<string:name>/item')
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    # Iterate through stores, if name matches, return it,
    # if none matches return an error
    for store in stores:
        if store['name'] == name:
            return jsonify({'items' : store['items']})
    return jsonify({'message': 'No such items'})



if __name__ == '__main__':
    app.run(port = 5000) #debug=True