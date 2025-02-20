"""
This module defines the FastAPI application and the endpoints for uploading
and downloading seating arrangements. It uses SQLite to store the seating
arrangements and the uploaded Excel files.

The application uses SQLAlchemy to interact with the SQLite database and
Pydantic to define the data models. The endpoints are defined using FastAPI
decorators.

The upload endpoint accepts an Excel file and processes it to generate a
seating arrangement. It stores the session ID, the uploaded file, and the
seating plan in the SQLite database.

The download endpoint accepts a session ID and retrieves the seating plan
from the database. It writes the seating plan to an Excel file and returns
it as a FileResponse.

The application uses the `process_file` and `write_file` functions from the
`utils.excel_handler` module to process the Excel files.

The `Openspace` class from the `utils.openspace` module is used to generate
the seating arrangements.

The database schema is defined using the `SeatingSession` class, which
represents the seating sessions table in the database.

The application uses a SQLite database stored in a file called `seating.db`.
The database is created using SQLAlchemy and the `create_engine` function.

The application uses a `SessionLocal` object to interact with the database.
The `Base` object is used to create the table if it doesn't exist.

The `safely_delete_file` function is used to safely delete files, handling
exceptions such as `PermissionError` and `FileNotFoundError`.

The `upload_excel` endpoint uploads an Excel file, processes it to generate
a seating arrangement, and stores the session ID, the file, and the seating
plan in the SQLite database.

The `download_seating` endpoint downloads the seating arrangement as an Excel
file using the session ID. It retrieves the seating plan from the database,
writes it to an Excel file, and returns it as a `FileResponse`.

To run the application, use the following command:
```
$ uvicorn backend.main:app --reload
```	
"""


from typing import Dict
import os
import uuid
from tempfile import NamedTemporaryFile
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

from sqlalchemy import create_engine, Column, String, LargeBinary, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.utils.excel_handler import process_file, write_file
from backend.utils.openspace import Openspace


# Use a SQLite database for storing the seating arrangements
# The database URL is a file path to the SQLite database
DATABASE_URL = "sqlite:///backend/database/seating.db"

# SQLite requires a special flag for multithreading
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the model for seating sessions
class SeatingSession(Base):
    """
    Class to represent the seating sessions table in the database.
    """
    __tablename__ = "seating_sessions"
    session_id = Column(String, primary_key=True, index=True)
    uploaded_file = Column(LargeBinary) # Store the Excel file as binary data
    seating_plan = Column(JSON) # Store the seating plan as JSON
    create_at = Column(DateTime, default=datetime.now()) # Store the creation time


# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)


# Create the FastAPI application
app = FastAPI()


def safely_delete_file(file_path: str):
    """
    Safely deletes a file at the given path.

    Parameters:
    -----------
    file_path : str
        The path to the file to delete.

    Returns:
    --------
    None
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except PermissionError as e:
        # Attempt to close any handles to the file or retry
        # Additional handling could involve logging or exponential backoff
        print(f"PermissionError while deleting {file_path}. Details: {e}")
    except FileNotFoundError as e:
        print(
            f"FileNotFoundError: the file {file_path} was not found. Details: {e}")
    except OSError as e:
        # Handle other OSError exceptions (e.g., file in use on Windows)
        print(f"OSError while deleting {file_path}. Details: {e}")


@app.post("/upload/", response_model=Dict)
async def upload_excel(
    table_capacity: int = 4,
    file: UploadFile = File(...),
) -> Dict:
    """
    Uploads an Excel file, processes it to generate a seating arrangement,
    and stores the session ID, the file, and the seating plan in the SQLite database.
    """
    # Save uploaded file temporarily
    temp_file = NamedTemporaryFile(suffix=".xlsx", delete=False)
    contents = await file.read()

    try:
        with open(temp_file.name, "wb") as f:
            f.write(contents)

        success, data = process_file(temp_file.name)
        if success:
            person_names = data["person_names"]
            compatible_pairs = data["compatible_pairs"]
            incompatible_pairs = data["incompatible_pairs"]

            num_tables = len(person_names) // table_capacity + \
                (1 if len(person_names) % table_capacity else 0)
            open_space = Openspace(num_tables=num_tables,
                                   table_capacity=table_capacity)

            try:
                open_space.organize_seating(
                    person_names, compatible_pairs, incompatible_pairs)
                seating_data = open_space.display_seating()

                # Generate a unique session ID
                session_id = str(uuid.uuid4())

                # Store the data in SQLite
                db = SessionLocal()
                db_session = SeatingSession(
                    session_id=session_id,
                    uploaded_file=contents, # save binary content of the uploaded file
                    seating_plan=seating_data, # save seating plan as JSON
                    create_at=datetime.now() # save the creation time
                )
                db.add(db_session)
                db.commit()
                db.refresh(db_session)
                db.close()

                return {"status": True, "session_id": session_id}
            except ValueError as e:
                return {"status": False, "message": str(e)}
        else:
            return {"status": False, "message": "Error processing file."}
    finally:
        safely_delete_file(temp_file.name)


@app.get("/download/")
async def download_seating(session_id: str) -> FileResponse:
    """
    Downloads the seating arrangement as an Excel file using the session ID.
    It retrieves the seating plan from the database, writes it to an Excel file,
    and returns it as a FileResponse.
    """
    db = SessionLocal()
    session_record = db.query(SeatingSession).filter(
        SeatingSession.session_id == session_id).first()
    if not session_record:
        db.close()
        raise HTTPException(
            status_code=404, detail="No seating arrangement available.")

    file_name = f"seating_arrangement_{session_id}.xlsx"
    file_path = os.path.join("backend/files", file_name)

    # Generate the Excel file using the stored seating plan
    write_file(file_path, session_record.seating_plan)

    # Optionally, you might want to delete the record after download
    # db.delete(session_record)
    # db.commit()
    db.close()

    return FileResponse(path=file_path, filename=file_name)


@app.delete("/delete/", response_model=Dict)
async def delete_seating_file(session_id: str) -> Dict:
    """
    Deletes the seating arrangement Excel file from the backend/files directory
    using the session ID. The database record is left intact.
    """
    db = SessionLocal()
    session_record = db.query(SeatingSession).filter(
        SeatingSession.session_id == session_id
    ).first()
    db.close()

    if not session_record:
        raise HTTPException(
            status_code=404, detail="Seating arrangement not found.")

    file_name = f"seating_arrangement_{session_id}.xlsx"
    file_path = os.path.join("backend/files", file_name)

    if not os.path.exists(file_path):
        return {"status": False, "message": "Excel file not found in backend/files directory."}

    safely_delete_file(file_path)
    return {"status": True, "message": "Excel file deleted successfully."}
