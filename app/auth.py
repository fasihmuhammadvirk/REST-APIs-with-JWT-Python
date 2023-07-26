from app.database import session
import app.model  as model
from app.utils import decode_access_token
from fastapi import status, HTTPException, Header


db = session()

#helper function to authnticate the user and jwt token
def authenticate(jwt_token:str = Header(...),user_email:str = Header(...)):
    
    #checking if the user that user exits or not
    is_user_exists = db.query(model.User_Info).filter(model.User_Info.email == user_email).first()
    
    if is_user_exists is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='User Does not Exits, Signup First')
    
    #checking it the token given is correct according to the user or not 
    is_user , is_exp = decode_access_token(jwt_token,user_email)
    
    if is_user == False and is_exp == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid Token')
    
    #checking if the token has expired or not 
    if is_exp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Token has Expire, Re Login')