from todo_app import app
import dotenv

file_path = dotenv.find_dotenv('.env')
dotenv.load_dotenv(file_path, override=True)

application = app.create_app()
