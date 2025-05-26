from lib import api
import os
# Este arquivo é o ponto de entrada para a aplicação FastAPI.
# Para rodar o servidor, use:
# uvicorn main:app --reload

app = api.app
os.environ["DATABASE_URL"] = "postgresql://usuario:senha@localhost/Exemplo"
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
