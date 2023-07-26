from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from app.database import session
import app.model  as model
from app.utils import get_hashed_password,verify_password,create_access_token
from typing import List 
from app.auth import authenticate

app = FastAPI()
db = session()


# creating a model using pydantic
class Item(BaseModel):


    name: str
    description: str
    price: int
    on_offer: bool

    class Config:
        orm_mode = True



class User_Info(BaseModel):
    email:str
    password:str
    
    class Config:
        orm_mode = True



#greeting api         
@app.get('/',tags = ['Greetings'])
def greet():
    return {'message':'write /docs in url to test apis'}

#api to sigup the user 
@app.post('/signup',status_code=status.HTTP_201_CREATED,tags = ['User Signup - Login'])
def signup(user: User_Info):

    try:
        db_user = db.query(model.User_Info).filter(model.User_Info.email == user.email).first()
        if db_user is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Already Exits")
        
        new_user = model.User_Info (
            email =  user.email ,
            hash_password = get_hashed_password(user.password),
            jwt_token = None,
            jwt_expiration_time = None 
            
        )
        
        db.add(new_user)
        db.commit()
        
        return {'Message':'User Created'}
    except Exception as e:
        print(e)

#api to login the user and assign a jwt_token 
@app.post('/login',status_code=status.HTTP_200_OK,tags = ['User Signup - Login'])
def login(user:User_Info):
    
    try: 
        db_user = db.query(model.User_Info).filter(model.User_Info.email == user.email).first()
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Does Not Exits")

        password_verify =  verify_password(user.password,db_user.hash_password)
        if not password_verify:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")


        jwt_access,jwt_exp_time = create_access_token(user.email)
        
        db_user.jwt_token = jwt_access
        db_user.jwt_expiration_time = jwt_exp_time
        
        db.commit()

        return {'Your JWT':jwt_access,'Note':'It will expire in 30 min'}
    
    except Exception as e: 
        print(e)



# CRUD operation with jwt token

# geeting all the items from the database 
@app.get("/items", response_model=List[Item],status_code= status.HTTP_200_OK,tags = ['CRUD Operations'])
def get_all_items(dependencies = Depends(authenticate)):
        
    items = db.query(model.Items).all()
    return items

        


@app.get('/items/{item_name}', response_model=Item, status_code=status.HTTP_200_OK,tags = ['CRUD Operations'])
def get_an_item(item_name: int,dependencies = Depends(authenticate)):
    
    an_item = db.query(model.Items).filter(model.Items.name == item_name).first()
    
    if an_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    return an_item


@app.post('/items', response_model=Item, status_code=status.HTTP_201_CREATED,tags = ['CRUD Operations'])
def create_item(item: Item,dependencies = Depends(authenticate)):
    
    db_item = db.query(model.Items).filter(model.Items.name == item.name).first()
    if db_item is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item Already Exits")

    new_item = model.Items(
        name=item.name,
        description=item.description,
        price=item.price,
        on_offer=item.on_offer
    )
    

    db.add(new_item)
    db.commit()


    return new_item

@app.put('/item/{item_name}', response_model=Item, status_code=status.HTTP_200_OK,tags = ['CRUD Operations'])
def update_item(item_name: str, item: Item,dependencies = Depends(authenticate)):
    
    item_to_update = db.query(model.Items).filter(model.Items.name == item_name).first()
    
    if item_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")    
    item_to_update.name = item.name
    item_to_update.description = item.description
    item_to_update.price = item.price
    item_to_update.on_offer = item.on_offer

    db.commit()

    return item_to_update

@app.delete('/item/{item_name}', response_model=Item, status_code=status.HTTP_200_OK,tags = ['CRUD Operations'])
def delete_item(item_name: str,dependencies = Depends(authenticate)):
    
    item_to_delete = db.query(model.Items).filter(
        model.Items.name == item_name).first()

    if item_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")

    db.delete(item_to_delete)
    db.commit()

    return item_to_delete

