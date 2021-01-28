from App.MainAbstract.index import db,Entity_list_user
from App.MainAbstract.CLS_MainAbstractModule import CLS
from werkzeug.security import generate_password_hash
from flask import jsonify,request

class CLS_CRUD(CLS):
    def create(self):
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = Entity_list_user(NationalID=data['nationalid'],
                                    FirstName=data['firstname'],
                                    LastName=data['lastname'],
                                    Password=hashed_password,
                                    Email=data['email'],
                                    FacultyID=data['facultyid'],
                                    Faculty=data['faculty'],
                                    Dept=data['dept'],
                                    UserType=data['usertype'])
        db.session.add(new_user)
        db.session.commit()
        return data

    def read(self):
        users = Entity_list_user.query.all()
        output = []
        for user in users:
            user_data = {}
            user_data['nationalid'] = user.NationalID
            user_data['firstname'] = user.FirstName
            user_data['lastname'] = user.LastName
            user_data['password'] = user.Password
            user_data['email'] = user.Email
            user_data['facultyid'] = user.FacultyID
            user_data['faculty'] = user.Faculty
            user_data['dept'] = user.Dept
            user_data['usertype'] = user.UserType
            output.append(user_data)
        return jsonify({'users': output})


    def readOne(self,id):
        user = Entity_list_user.query.filter_by(NationalID=id).first()
        if not user:
                return jsonify({'message': 'no user found!'})
        else:
                user_data = {}
                user_data['nationalid'] = user.NationalID
                user_data['firstname'] = user.FirstName
                user_data['lastname'] = user.LastName
                user_data['password'] = user.Password
                user_data['email'] = user.Email
                user_data['facultyid'] = user.FacultyID
                user_data['faculty'] = user.Faculty
                user_data['dept'] = user.Dept
                user_data['usertype'] =user.UserType
                return user_data


    def update(self,id):
        uuser = Entity_list_user.query.filter_by(NationalID=id).first()
        if not uuser:
            return jsonify({'message': 'User not found!'})
        else:
            user = request.get_json()
            hashed_password = generate_password_hash(user['password'], method='sha256')
            uuser.NationalID=user['nationalid']
            uuser.FirstName=user['firstname']
            uuser.LastName=user['lastname']
            uuser.Password=hashed_password
            uuser.Email=user['email']
            uuser.FacultyID=user['facultyid']
            uuser.Faculty=user['faculty']
            uuser.Dept=user['dept']
            uuser.UserType=user['usertype']
            db.session.commit()
            return jsonify({'message': 'The user'+ uuser.NationalID+ 'has been updated '})


    def delete(self,id):
        user = Entity_list_user.query.filter_by(NationalID=id).first()
        if not user:
            return jsonify({'message': 'User not found!'})
        else:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'Delete done'})
