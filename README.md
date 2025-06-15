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