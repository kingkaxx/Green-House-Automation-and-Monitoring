
from flask import Flask,render_template,url_for,request,session,redirect,json,jsonify,flash
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson import ObjectId
import socket,json,time
import sys
#import receive




app=Flask(__name__,template_folder='templates')  #give name of folder where templates are saved

app.config['MONGO_DBNAME']='GreenHouse'
app.config['MONGO_URI']='mongodb://localhost:27017/GreenHouse'

mongo = PyMongo(app)
"""
@app.route('/')
def loginf():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('loginf.html')
    
"""

@app.route('/',methods=['GET','POST'])
def index():

    return render_template('home.html')


@app.route('/overview',methods=['GET'])
def overview():
	return render_template('cc.html')

@app.route('/logout',methods=['GET'])
def logout():
	return render_template('home.html')

#loads for decoding and dumps for encoding

@app.route('/delete',methods=['GET','POST'])
def delete():
    
    users = mongo.db.users
    usersnew = users.find().sort('name')
    data =[]
    delete_user = request.form['deleteuser']
    op=users.remove({"name":delete_user})
    

    for one in usersnew:
        
        data.append(one)
        newdata = JSONEncoder().encode(data)
    
    return render_template('CustomerAdded.html',data=data)

   


@app.route('/Update',methods=['GET','POST'])
def updatecustomer():
    users = mongo.db.users
    usersnew = users.find().sort('name')

    data=[];
    updatedval = request.form['Update']
    name = users.find({"name":updatedval})
    session['updatedval']=updatedval;

    #print('iid',name)
    dt =[];

    for i in name:
        dt.append(i)
    print(dt)
    
       
        
    for one in usersnew:
        
        data.append(one)
        newdata = JSONEncoder().encode(data)
   
        
    return render_template('updatecustomer.html',users=users,updatedval=updatedval)

@app.route('/realupdate',methods=['GET','POST'])
def realupdate():
    users = mongo.db.users
    usersnew = users.find().sort('name')
    updatedval=session.get('updatedval')
    up=users.update_one({"name":updatedval},{'$set':{'name':request.form['edit-username'],'email':request.form['edit-email'],'Address':request.form['edit-Address']}})
    data=[];
    for one in usersnew:
        
        data.append(one)
        newdata = JSONEncoder().encode(data)
   
        
    return render_template('CustomerAdded.html',data=data)





@app.route('/login', methods=['POST'])   
def login():
    if 'username' in session:
        
        print( 'You are logged in as ' + session['username'])
    users = mongo.db.users
    tests=mongo.db.tests
    login_user = users.find_one({'name' : request.form['username']})
    avauser = users.count();
    count1=tests.find({}).count();
    pune = users.find({"Address":"Pune"});
    mumbai = users.find({"Address":"Mumbai"});
    punecount = pune.count();
    mumbaicount = mumbai.count();
    temp = tests.find()
    fielddata1 = tests.find_one({"Name":"pict"});
    fielddata = tests.find_one({"Name":"PICT"});
    straw = tests.find_one({"name":"straw"});
    spin = tests.find_one({"name":"spin"});
    gerb = tests.find_one({"name":"gerb"});
    if (request.form['username']=='admin'):
        if ((request.form['password'])== 'admin'):
            flash('You were successfully logged in')

            return render_template('admin.html',avauser=avauser,punecount=punecount,mumbaicount=mumbaicount)
    
    elif ((request.form['username'])== login_user['name']):


        if((request.form['password'])== login_user['password']):
            
            return render_template('test.html',fielddata=fielddata,straw=straw,spin=spin,gerb=gerb,fielddata1=fielddata1,count1=count1)
           
    elif ((request.form['username'])!= login_user['name']):
        return render_template('invalidlog.html')


    return render_template('invalidlog.html')



    




@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if(request.form['username']=='admin'):
            return render_template('cantbe.html')


        elif existing_user is None:
            hashpass = (request.form['password'])    
            users.insert({'name' : request.form['username'], 'password' : hashpass,'email':request.form['email']})
           
            return render_template('regsu.html')
        
        return render_template('already.html')

    return render_template('signup.html')




@app.route('/customadd', methods=['POST','GET'])
def customadd():
    return render_template('addcustom_admin.html')


@app.route('/Addcustomer',methods=['POST','GET'])
def Addcustomer():
    users = mongo.db.users
    avauser = users.count();
    pune = users.find({"Address":"Pune"});
    mumbai = users.find({"Address":"Mumbai"});
    punecount = pune.count();
    mumbaicount = mumbai.count();
    tests=mongo.db.tests
    temp = tests.find()
    
    existing_user = users.find_one({'name' : request.form['username']})

    if request.method == 'POST':
        
        if existing_user is None :
            
            passw = (request.form['password'])    
            users.insert({'name' : request.form['username'], 'email' : request.form['email'],'password' : passw,'Address' : request.form['Address']})
            return render_template('admin.html',avauser=avauser,punecount=punecount,mumbaicount=mumbaicount)
        return render_template('existing_user.html')    
    
    return json.dumps({'status':'OK','Username':request.form['username'],'password':passw,'Email':request.form['email'],'Address' : request.form['Address']});

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)




@app.route('/CustomerAdded',methods=['GET'])
def completeAdd():
    users = mongo.db.users
    usersnew = users.find().sort('name')
    data=[];
    
        
    for one in usersnew:
        eachitem={
        'name':users['name'],
        'email':users['email'],
        'password':users['password'],
        }
        data.append(one)
        newdata = JSONEncoder().encode(data)

    return render_template('CustomerAdded.html',data=data,users=users)   



 
@app.route('/straw',methods=['GET','POST'])
def straw():
    tests=mongo.db.tests
    users=mongo.db.users
    straw = tests.find_one({"name":"straw"});
    fielddata = tests.find_one({"Name":"PICT"});
    fielddata1 = tests.find_one({"Name":"pict"});
    count1=tests.find({}).count();

    
    TCP_IP = '192.168.43.89'
    TCP_PORT = 12397
    saw = bytes( "1".encode())
    s = socket.socket()
    s.connect((TCP_IP, TCP_PORT))
    s.send(saw)
    s.close()
    
    return render_template('straw.html',straw=straw,fielddata=fielddata,fielddata1=fielddata1,count1=count1)


@app.route('/spin',methods=['GET','POST'])
def spin():
    tests=mongo.db.tests
    spin = tests.find_one({"name":"spin"});
    fielddata = tests.find_one({"Name":"PICT"});
    fielddata1 = tests.find_one({"Name":"pict"});
    count1=tests.find({}).count();

    
    TCP_IP = '192.168.43.89'
    TCP_PORT = 12397
    pop = bytes( "2".encode())
    s = socket.socket()
    s.connect((TCP_IP, TCP_PORT))
    s.send(pop)
    s.close()
    
    
    return render_template('spin.html',spin=spin,fielddata=fielddata,fielddata1=fielddata1,count1=count1)


@app.route('/gerb',methods=['GET','POST'])
def gerb():
    tests=mongo.db.tests
    gerb = tests.find_one({"name":"gerb"});
    fielddata = tests.find_one({"Name":"PICT"});
    fielddata1 = tests.find_one({"Name":"pict"});
    count1=tests.find({}).count();



    TCP_IP = '192.168.43.89'
    TCP_PORT = 12397
    gerba = bytes( "3".encode())
    s = socket.socket()
    s.connect((TCP_IP, TCP_PORT))
    s.send(gerba)
    s.close()
    
    return render_template('gerb.html',gerb=gerb,fielddata=fielddata,fielddata1=fielddata1,count1=count1)











@app.route('/login')
def loginform():
	return render_template('loginf.html')
"""
"""
""" changes done in Dashb tab """
@app.route('/Dashb')
def home():
   
    tests=mongo.db.tests
   
    fielddata = tests.find_one({"Name":"PICT"});
    fielddata1 = tests.find_one({"Name":"pict"});
    count1=tests.find({}).count();

   
    return render_template('test.html',fielddata=fielddata,fielddata1=fielddata1,count1=count1);

        


"""Make changes according to condition """



@app.route('/dashy',methods=['GET','POST'])
def dashy():
    users = mongo.db.users
    avauser = users.count();
    pune = users.find({"Address":"Pune"});
    mumbai = users.find({"Address":"Mumbai"});
    punecount = pune.count();
    mumbaicount = mumbai.count();
    tests=mongo.db.tests
    temp = tests.find()

    
    return render_template('admin.html',avauser=avauser,punecount=punecount,mumbaicount=mumbaicount)


    

"""
"""

if __name__ == '__main__':
		app.secret_key = 'mysecret'	

		app.run(debug=True)





