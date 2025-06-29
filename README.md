# YourCloud

> **Note:**  
> To avoid `ModuleNotFoundError: No module named 'app'`, run the backend from the `embedded-backend` directory or set `PYTHONPATH` to include this directory:
> 
> ```
> cd embedded-backend
> uvicorn app.main:app --reload
> ```
> or
> ```
> PYTHONPATH=. uvicorn app.main:app --reload
> ```

## Running test scripts

To run scripts in `app/test-scripts` that import from `app`, use one of the following methods:

- **Recommended:**  
  ```
  cd embedded-backend
  python -m app.test-scripts.create-chat-folder
  ```

- **Or set PYTHONPATH:**  
  ```
  set PYTHONPATH=.
  python app/test-scripts/create-chat-folder.py
  ```