# from fastapi import Depends, HTTPException, Path, APIRouter
# from typing import Annotated
#
# from pydantic import BaseModel, Field
# from sqlalchemy.orm import Session
# from fastapi import status  # 상태 코드를 사용하기 위해 status 모듈을 임포트합니다.
# from models import Todos
# from database import SessionLocal
#
# router = APIRouter()  # FastAPI 애플리케이션 인스턴스 생성
#
#
#
# def get_db():
#     # 데이터베이스 세션 인스턴스 생성
#     db = SessionLocal()
#     try:
#         # 생성된 데이터베이스 세션을 요청 처리 중 사용할 수 있도록 제공
#         yield db
#     finally:
#         # 요청 처리가 완료되면 데이터베이스 세션을 닫습니다.
#         db.close()
#
#
# # 의존성 주입을 위한 타입 힌트
# # 이를 통해 함수가 호출될 때 FastAPI에 의해 자동으로 `get_db` 함수가 호출되며,
# # 그 결과로 데이터베이스 세션 객체가 해당 함수에 전달됩니다.
# db_dependency = Annotated[Session, Depends(get_db)]
#
#
# class TodoRequest(BaseModel):
#     title: str = Field(min_length=3)
#     description: str = Field(min_length=3, max_length=100)
#     priority: int = Field(gt=0, lt=6)
#     complete: bool
#
#
# # 모든 Todo 항목을 조회하는 API 엔드포인트
# # FastAPI의 Depends는 매개 변수로 전달 받은 함수를 실행시킨 결과를 리턴하여 db에 주입
# # -> get_db로 db 세션 객체를 생성하고 함수 종료 직전에 다시 db.close()를 호출하도록
# @router.get('/')
# async def read_all(db: Annotated[Session, Depends(get_db)]):
#     # 데이터베이스에서 모든 Todo 항목을 조회하여 반환
#     return db.query(Todos).all()
#
#
# # 특정 ID를 가진 Todo 항목을 조회하는 API 엔드포인트
# # `db_dependency`를 통해 데이터베이스 세션을 매개변수로 자동 받습니다.
# @router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
# async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
#     # 주어진 ID에 해당하는 Todo 항목을 데이터베이스에서 조회
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is not None:
#         # Todo 항목이 존재하면 반환
#         return todo_model
#     # Todo 항목이 존재하지 않으면 404 에러 발생
#     raise HTTPException(status_code=404, detail='Todo not found')
#
#
# # '/todo' 경로에 POST 요청을 매핑하고, 성공적으로 Todo 항목을 생성한 경우
# # HTTP 201 (Created) 상태 코드를 반환합니다.
# # `db_dependency`를 통해 데이터베이스 세션을 주입받고, `todo_request`에는 클라이언트로부터 받은 데이터가 포함됩니다.
# @router.post("/todo", status_code=status.HTTP_201_CREATED)
# async def create_todo(db: db_dependency, todo_request: TodoRequest):
#     # `TodoRequest` 모델의 `model_dump` 메서드를 사용하여
#     # 클라이언트로부터 받은 요청 데이터를 Todo 모델 인스턴스로 변환합니다.
#     todo_model = Todos(**todo_request.dict())
#     db.add(todo_model)  # 데이터베이스 세션에 Todo 모델 인스턴스를 추가합니다.
#     db.commit()  # 변경 사항을 데이터베이스에 커밋하여 실제로 데이터를 저장합니다.
#
#
# @router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def update_todo(db: db_dependency,todo_reqeust: TodoRequest, todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail='Todo not found')
#     todo_model.title = todo_reqeust.title
#     todo_model.description = todo_reqeust.description
#     todo_model.priority = todo_reqeust.priority
#     todo_model.complete = todo_reqeust.complete
#     db.add(todo_model)
#     db.commit()
#
#
# @router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# # '/todo/{todo_id}' 경로에 DELETE 요청을 매핑합니다.
# # 성공적으로 Todo 항목을 삭제한 경우, HTTP 204 (No Content) 상태 코드를 반환합니다.
# # `db_dependency`를 통해 데이터베이스 세션을 매개변수로 받으며,
# # `todo_id`는 경로에서 받은 Todo 항목의 ID입니다. `Path(gt=0)`은 todo_id가 0보다 커야 한다는 조건을 추가합니다.
# async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
#     # 주어진 ID에 해당하는 Todo 항목을 데이터베이스에서 조회합니다.
#     todo_model = db.query(Todos).filter(todo_id==Todos.id).first()
#     if todo_model is None:
#         # 조회된 Todo 항목이 없으면, HTTP 404 (Not Found) 에러를 발생시킵니다.
#         raise HTTPException(status_code=404, detail='Todo not found')
#     # 조회된 Todo 항목이 있으면, 해당 항목을 데이터베이스에서 삭제합니다.
#     db.query(Todos).filter(Todos.id==todo_id).delete()
#     # 변경 사항을 데이터베이스에 커밋하여 실제로 데이터를 저장합니다.
#     db.commit()
#
#
#
# # 모든 사용자 정보를 반환하는 엔드포인트
# @app.get("/users")
# async def read_users():
#     users = session.query(User).all()
#     return users
#
# # 특정 id로 사용자 정보 조회
# @app.get("/users/{user_id}")
# async def read_user(user_id: int):
#     user = session.query(User).filter(User.id == user_id).first()
#     if user is None:
#         return {"message": "User not found"}
#
#     user_data = {
#         "id": user.id,
#         "username": user.username,
#         "email": user.email,
#         "phone_number": user.phone_number,
#         "gender": user.gender,
#         "school": user.school,
#         "password": user.password
#     }
#
#     return user_data
# # 사용자 등록
# @app.post("/users/")
# async def create_user(item: Item):
#     user = User(**item.dict())
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user
# # 특정 사용자 정보 업데이트
# @app.put("/users/{user_id}")
# async def update_user(user_id: int, item: Item):
#     user = session.query(User).filter(User.id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     for key, value in item.dict().items():
#         setattr(user, key, value)
#     session.commit()
#     session.refresh(user)
#     return user
#
# # 특정 사용자 삭제
# @app.delete("/users/{user_id}")
# async def delete_user(user_id: int):
#     user = session.query(User).filter(User.id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     session.delete(user)
#     session.commit()
#     return {"message": "User deleted successfully"}

# # 모든 시나리오 조회
# @app.get("/scenarios")
# async def read_scenarios():
#     scenarios = session.query(Scenario).all()
#     return scenarios
#
# # 새 시나리오 생성
# @app.post("/scenarios/")
# async def create_scenario(item: Item):
#     scenario = Scenario(**item.dict())
#     session.add(scenario)
#     session.commit()
#     session.refresh(scenario)
#     return scenario
#
# # 특정 시나리오 조회
# @app.get("/scenarios/{scenario_id}")
# async def read_scenario(scenario_id: int):
#     scenario = session.query(Scenario).filter(Scenario.id == scenario_id).first()
#     if scenario is None:
#         raise HTTPException(status_code=404, detail="Scenario not found")
#     return scenario
#
# # 특정 시나리오 삭제
# @app.delete("/scenarios/{scenario_id}")
# async def delete_scenario(scenario_id: int):
#     scenario = session.query(Scenario).filter(Scenario.id == scenario_id).first()
#     if scenario is None:
#         raise HTTPException(status_code=404, detail="Scenario not found")
#     session.delete(scenario)
#     session.commit()
#     return {"message": "Scenario deleted successfully"}
#
# # 모든 피드백 조회
# @app.get("/feedbacks")
# async def read_feedbacks():
#     feedbacks = session.query(Feedback).all()
#     return feedbacks
#
# # 새 피드백 생성
# @app.post("/feedbacks/")
# async def create_feedback(item: Item):
#     feedback = Feedback(**item.dict())
#     session.add(feedback)
#     session.commit()
#     session.refresh(feedback)
#     return feedback
#
# # 특정 피드백 조회
# @app.get("/feedbacks/{feedback_id}")
# async def read_feedback(feedback_id: int):
#     feedback = session.query(Feedback).filter(Feedback.id == feedback_id).first()
#     if feedback is None:
#         raise HTTPException(status_code=404, detail="Feedback not found")
#     return feedback
#
# # 특정 피드백 삭제
# @app.delete("/feedbacks/{feedback_id}")
# async def delete_feedback(feedback_id: int):
#     feedback = session.query(Feedback).filter(Feedback.id == feedback_id).first()
#     if feedback is None:
#         raise HTTPException(status_code=404, detail="Feedback not found")
#     session.delete(feedback)
#     session.commit()
#     return {"message": "Feedback deleted successfully"}
#
# # 모든 역할 조회
# @app.get("/roles")
# async def read_roles():
#     roles = session.query(Role).all()
#     return roles
#
# # 새 역할 생성
# @app.post("/roles/")
# async def create_role(item: Item):
#     role = Role(**item.dict())
#     session.add(role)
#     session.commit()
#     session.refresh(role)
#     return role
#
# # 특정 역할 정보 업데이트
# @app.put("/roles/{role_id}")
# async def update_role(role_id: int, item: Item):
#     role = session.query(Role).filter(Role.id == role_id).first()
#     if role is None:
#         raise HTTPException(status_code=404, detail="Role not found")
#     for key, value in item.dict().items():
#         setattr(role, key, value)
#     session.commit()
#     session.refresh(role)
#     return role
#
# # 특정 역할 삭제
# @app.delete("/roles/{role_id}")
# async def delete_role(role_id: int):
#     role = session.query(Role).filter(Role.id == role_id).first()
#     if role is None:
#         raise HTTPException(status_code=404, detail="Role not found")
#     session.delete(role)
#     session.commit()
#     return {"message": "Role deleted successfully"}


# 모든 Todo 항목을 조회하는 API 엔드포인트
# FastAPI의 Depends는 매개 변수로 전달 받은 함수를 실행시킨 결과를 리턴하여 db에 주입
# -> get_db로 db 세션 객체를 생성하고 함수 종료 직전에 다시 db.close()를 호출하도록
# @router.get('/')
# async def read_all(db: Annotated[Session, Depends(get_db)]):
#     # 데이터베이스에서 모든 Todo 항목을 조회하여 반환
#     return db.query(Todos).all()
#
#
# # 특정 ID를 가진 Todo 항목을 조회하는 API 엔드포인트
# # `db_dependency`를 통해 데이터베이스 세션을 매개변수로 자동 받습니다.
# @router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
# async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
#     # 주어진 ID에 해당하는 Todo 항목을 데이터베이스에서 조회
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is not None:
#         # Todo 항목이 존재하면 반환
#         return todo_model
#     # Todo 항목이 존재하지 않으면 404 에러 발생
#     raise HTTPException(status_code=404, detail='Todo not found')
#
#
# # '/todo' 경로에 POST 요청을 매핑하고, 성공적으로 Todo 항목을 생성한 경우
# # HTTP 201 (Created) 상태 코드를 반환합니다.
# # `db_dependency`를 통해 데이터베이스 세션을 주입받고, `todo_request`에는 클라이언트로부터 받은 데이터가 포함됩니다.
# @router.post("/todo", status_code=status.HTTP_201_CREATED)
# async def create_todo(db: db_dependency, todo_request: TodoRequest):
#     # `TodoRequest` 모델의 `model_dump` 메서드를 사용하여
#     # 클라이언트로부터 받은 요청 데이터를 Todo 모델 인스턴스로 변환합니다.
#     todo_model = Todos(**todo_request.dict())
#     db.add(todo_model)  # 데이터베이스 세션에 Todo 모델 인스턴스를 추가합니다.
#     db.commit()  # 변경 사항을 데이터베이스에 커밋하여 실제로 데이터를 저장합니다.
#
#
# @router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def update_todo(db: db_dependency,todo_reqeust: TodoRequest, todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail='Todo not found')
#     todo_model.title = todo_reqeust.title
#     todo_model.description = todo_reqeust.description
#     todo_model.priority = todo_reqeust.priority
#     todo_model.complete = todo_reqeust.complete
#     db.add(todo_model)
#     db.commit()
#
#
# @router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# # '/todo/{todo_id}' 경로에 DELETE 요청을 매핑합니다.
# # 성공적으로 Todo 항목을 삭제한 경우, HTTP 204 (No Content) 상태 코드를 반환합니다.
# # `db_dependency`를 통해 데이터베이스 세션을 매개변수로 받으며,
# # `todo_id`는 경로에서 받은 Todo 항목의 ID입니다. `Path(gt=0)`은 todo_id가 0보다 커야 한다는 조건을 추가합니다.
# async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
#     # 주어진 ID에 해당하는 Todo 항목을 데이터베이스에서 조회합니다.
#     todo_model = db.query(Todos).filter(todo_id==Todos.id).first()
#     if todo_model is None:
#         # 조회된 Todo 항목이 없으면, HTTP 404 (Not Found) 에러를 발생시킵니다.
#         raise HTTPException(status_code=404, detail='Todo not found')
#     # 조회된 Todo 항목이 있으면, 해당 항목을 데이터베이스에서 삭제합니다.
#     db.query(Todos).filter(Todos.id==todo_id).delete()
#     # 변경 사항을 데이터베이스에 커밋하여 실제로 데이터를 저장합니다.
#     db.commit()
