#Imports
from App.MachineLearning.CLS_Trainning import CLS_Trainning
from App.MachineLearning.CLS_Attendence import CLS_Attendance
from App.MachineLearning.CLS_VideoToImages import CLS_VideoToImages
from App.BusinessLayer.CLS_TokenRequired import token_required
from App.MachineLearning.CLS_RecordingVideo import record
from App.DataBaseLayer.CLS_CRUD import CLS_CRUD
from flask import request,jsonify,make_response,redirect
from MainAbstract.index import app,db,Entity_list_Attendance,Entity_list_user
from uuid import uuid4
from werkzeug.security import generate_password_hash,check_password_hash
import datetime
import base64
import jwt
from werkzeug.exceptions import HTTPException


########################################################################################################################


#just for test record and base64 encode
@app.route('/justfortestrecordvideo/<id>')
def recordsss(name,id):
    user = Entity_list_user.query.filter_by(FacultyID=id).first()
    Name=user.FirstName+'_'+user.LastName
    i=record(Name,id)
    return i


#just for test
@app.route('/record',methods=["POST"])
def record():
    image = open('D:\\171011youssef samy.avi', 'rb')
    image_read = image.read()
    image_64_encode = base64.encodebytes(image_read)
    return jsonify({"video":image_64_encode.decode('UTF-8')})
########################################################################################################################

#image_proccessing
#recieve video string Done
@app.route('/savevide/<id>',methods=["POST"])
def save(id):
    videojson=request.get_json()
    user = Entity_list_user.query.filter_by(FacultyID=id).first()
    Name = user.FirstName + '_' + user.LastName
    videoObj=videojson['video'].encode('UTF-8')
    image_64_decode = base64.decodebytes(videoObj)
    videoName=Name+'_'+facultyid
    image_result = open('Assets\\videos\\'+videoName+'.avi', 'wb')
    image_result.write(image_64_decode)
    return jsonify({'message':'done'})

#Spliter Done
@app.route('/Spliter/<facultyid>',methods=["POST"])
def Spliter(facultyid):
    if not facultyid:
        return jsonify({'message':'Not found NationalID'})
    user = Entity_list_user.query.filter_by(FacultyID=facultyid).first()
    if not user :
        return jsonify({'message':'Not found user'})
    Id=user.FacultyID
    Name=user.FirstName+'_'+user.LastName
    NUser=CLS_VideoToImages(Id,Name)
    NUser.SpliterVideo()
    return jsonify({'message':'Video upload and divided into frames for user: '+Name +' '})

#Train Done
@app.route('/Trainning',methods=["POST"])
def Trainning():
    Nuser=CLS_Trainning()
    Nuser.TrainImages()
    return jsonify({'message':'Trainning Done !!!'})

#problem in time out
@app.route('/Attendance',methods=["POST"])
def Attendance():
    obj1=CLS_Attendance()
    output=obj1.Attendence()
    return jsonify({'students_attended_today':output})
########################################################################################################################


#READ All Data
@app.route('/user', methods=['GET'])
@token_required
def getAllUsers(current_user):
        if not current_user.UserType=='admin':
            return make_response('Only Admin can perform this Function !!!', 401, {'WWW-Authenticate': 'Basic realm="Only Admin can perform this Function !!!"'})
        else:
            users=CLS_CRUD()
            output=users.read()
            return output


#Read one User
@app.route('/user/<nationalid>', methods=['GET'])
@token_required
def getOneUser(current_user, nationalid):
        if not current_user.UserType=='admin':
            return make_response('Only Admin can perform this Function !!!', 401,
                                 {'WWW-Authenticate': 'Basic realm="Only Admin can perform this Function !!!"'})
        else:
            user=CLS_CRUD()
            user_data=user.readOne(nationalid)
            return jsonify({'user': user_data})




@app.route('/user/<nationalid>', methods=['PUT'])
@token_required
def PromotUser(current_user, nationalid):
        if not current_user.UserType=='admin':
            return make_response('Only Admin can perform this Function !!!', 401,
                                 {'WWW-Authenticate': 'Basic realm="Only Admin can perform this Function !!!"'})
        else:
             UpdatedUser=CLS_CRUD()
             user=UpdatedUser.update(nationalid)
             return user



@app.route('/user/<nationalid>', methods=['DELETE'])
@token_required
def DeleteUser(current_user, nationalid):
        if not current_user.UserType=='admin':
            return make_response('Only Admin can perform this Function !!!', 401,
                                 {'WWW-Authenticate': 'Basic realm="Only Admin can perform this Function !!!"'})
        else:
            deleteuser=CLS_CRUD()
            us=deleteuser.delete(nationalid)
            return us


########################################################################################################################


#login for all users
@app.route('/login')
def login():
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!!!"'})
        user = Entity_list_user.query.filter_by(Email=auth.username).first()
        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!!!"'})
        if check_password_hash(user.Password, auth.password):
            token =jwt.encode({'nationalid': user.NationalID, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)},
                app.config['SECRET_KEY'])
            return jsonify({'token':token.decode('UTF-8')})
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!!!"'})



@app.route('/Registration', methods=['POST'])
def create_User():
        newUser=CLS_CRUD()
        data=newUser.create()
        return jsonify({'message': 'the new user added'+data['nationalid'] })



########################################################################################################################


#Handle Exception
#404,not found
@app.errorhandler(404)
def handle_exception(e):
    return redirect('/notfound')

@app.route('/notfound')
def NotFound():
    return jsonify({'error':'404,not found 404 !'})

#400 , bad request
@app.errorhandler(400 )
def handle_exception(e):
    return redirect('/badrequest')

@app.route('/badrequest')
def badrequest():
    return jsonify({'error':'400 , bad request !'})

#401  , unauthoraized
@app.errorhandler(401)
def handle_exception(e):
    return redirect('/unauthoraized'),401


@app.route('/unauthoraized')
def unauthoraized():
    return jsonify({'error':'401 ,unauthoraized !'})


#403 , forbiden
@app.errorhandler(403 )
def handle_exception(e):
    return redirect('/forbiden')


@app.route('/forbiden')
def forbiden():
    return jsonify({'error':'403 , forbiden !'})


#500 , internal server error
@app.errorhandler(500)
def handle_exception(e):
    return redirect('/internalservererror')

@app.route('/internalservererror')
def internalservererror():
    return jsonify({'error':'500 , internal server error !'})


#502  , bad gatway
@app.errorhandler(502)
def handle_exception(e):
    return redirect('/badgatway')

@app.route('/badgatway')
def badgatway():
    return jsonify({'error':'502  , bad gatway !'})


#504 , gatway timout
@app.errorhandler(504)
def handle_exception(e):
    return redirect('/gatwaytimout')


@app.route('/gatwaytimout')
def gatwaytimout():
    return jsonify({'error':'504 , gatway timout !'})


########################################################################################################################
#Run Web Service
if __name__ == '__main__':
   app.run()
