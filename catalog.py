#!/usr/bin/env python
import random
import string
import httplib2
import json
import requests
from flask import Flask, render_template, request, redirect,\
    jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response

app = Flask(__name__)

# FIrst we create a database session
engine = create_engine('sqlite:///vgcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Now we read in the google info from the local file
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "ItemCatalog"


# Show all categories
@app.route('/')
@app.route('/category')
@app.route('/category/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('categories.html', categories=categories)


# Create new category
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    # print("In newCategory")
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCat = Category(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCat)
        flash('Category %s Successfully Created' % newCat.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('NewCatagory.html')


# Delete category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    # print("In deleteCategory")
    deleteCat = session.query(
        Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if deleteCat.user_id != login_session['user_id']:
        flash('You are not authorized to delete this category.')
        return redirect(url_for('showCategories'))
    if request.method == 'POST':
        session.delete(deleteCat)
        flash('%s Successfully Deleted' % deleteCat.name)
        session.commit()
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('delCategory.html',
                               category=deleteCat)


# Edit Category
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    # print("In editCategory")
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedCategory.user_id != login_session['user_id']:
        flash('You are not permitted to edit this category.')
        return redirect(url_for('showCategories'))
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showCategories'))
    else:
        return render_template('editCatagory.html', category=editedCategory)


# Show items for a category
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/item/')
def showItem(category_id):
    # print("In showItem")
    category = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(category.user_id)
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('items.html', items=items,
                           category=category, creator=creator)


# Create new item
@app.route('/category/<int:category_id>/item/new/', methods=['GET', 'POST'])
def newCatItem(category_id):
    # print("In newCatItem")
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    if login_session['user_id'] != category.user_id:
        flash('You are not permitted to add items to this category.')
        return redirect(url_for('showItem', category_id=category_id))
    if request.method == 'POST':
            newItem = Item(name=request.form['name'], description=request.form
                           ['description'], category_id=category_id,
                           user_id=category.user_id)
            session.add(newItem)
            session.commit()
            flash(' %s Item Successfully Created' % (newItem.name))
            return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('newCatItem.html', category_id=category_id)


# Edit item
@app.route('/category/<int:category_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editCatItem(category_id, item_id):
    # print("In editCatItem")
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    if login_session['user_id'] != category.user_id:
        flash('You are not permitted to edit items in this category.')
        return redirect(url_for('showItem', category_id=category_id))
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash(' %s Item Successfully Edited' % (editedItem.name))
        return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('editItem.html', category_id=category_id,
                               item_id=item_id, item=editedItem)


# Delete item
@app.route('/category/<int:category_id>/item/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteCatItem(category_id, item_id):
    # print("In deleteCatItem")
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if login_session['user_id'] != category.user_id:
        flash('You are not authorized to delete items in this category.')
        return redirect(url_for('showItem', category_id=category_id))
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('deleteCatItem.html', item=itemToDelete)


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    # print("In login")
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # print("in gconnect")
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Get authorization code
    code = request.data

    try:
        # Put auth code in credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token user ID does not match submitted user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app client ID."), 401)
        print("Token's client ID does not match app client ID.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:\
        150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # print("In gdisconnect")
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token = %s' %\
          access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to \
                                 revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# User Helper Functions
def createUser(login_session):
    # print("In createUser")
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    # print("In getUserInfo")
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    # print("In getUserID")
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Disconnect facebook or google
@app.route('/disconnect')
def disconnect():
    print("In disconnect")
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            print("Provider is google.  Call gdisconnect")
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            print("Provider is facebook.  Call fbdisconnect")
            # fbdisconnect()# This doesn't actually work
            # del login_session['facebook_id']# This doesn't actually work
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))


@app.route('/clearSession')
def clear_session():
    print("In clearSession")
    login_session.clear()
    return "session cleared"


# JSON APIs to view Category Information
@app.route('/category/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


@app.route('/category/<int:category_id>/item/JSON')
def categoryItemJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(items=[i.serialize for i in items])


@app.route('/user/<int:user_id>/categories/JSON')
def userCategoriesJSON(user_id):
    categories = session.query(Category).filter_by(id=user_id).one()
    itemList = session.query(Category).filter_by(
        user_id=user_id).all()
    return jsonify(userItems=[i.serialize for i in itemList])


@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    itemList = session.query(Item).filter_by(id=item_id).one()
    return jsonify(itemList=itemList.serialize)


@app.route('/users/JSON')
def usersJSON():
    userList = session.query(User).all()
    return jsonify(userList=[x.serialize for x in userList])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)
