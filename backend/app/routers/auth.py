from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import auth, crud, models, schemas
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    """

    existing_email = crud.get_user_by_email(db, user.email)

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    existing_username = crud.get_user_by_username(
        db,
        user.username
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    return crud.create_user(db, user)


@router.post(
    "/login",
    response_model=schemas.Token
)
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login user and return JWT token.
    """

    db_user = crud.get_user_by_email(
        db,
        user.email
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not auth.verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = auth.create_access_token(
        data={
            "sub": str(db_user.id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get(
    "/me",
    response_model=schemas.UserResponse
)
def get_logged_in_user(
    current_user: models.User = Depends(get_current_user)
):
    """
    Return the currently logged in user.
    """

    return current_user