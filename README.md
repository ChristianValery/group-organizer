# Group Organizer / Seating Arrangement Tool

The Group Organizer / Seating Arrangement Tool is a web application designed to help users efficiently generate seating plans or group arrangements based on uploaded Excel files containing names and compatibility constraints. The tool allows users to specify the number of seats per table and downloads the generated seating plan as an Excel file.

## Table of Contents

- [Features](#features)
- [Directory Structure](#directory-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features

- Upload an Excel (`.xlsx`) file containing person names and compatibility constraints.
- Define the number of seats per table/group.
- Generate seating arrangements that can be downloaded as Excel files.
- Frontend built with Streamlit for a simple and interactive user interface.
- Backend API built using FastAPI for robust server-side operations.

## Directory Structure

```
group-organizer/
├── backend/
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── database/
│   │   └── [SQLite database files]
│   ├── files/
│   │   └── [Generated Excel files for seating plans]
│   └── utils/
│       ├── excel_handler.py
│       ├── openspace.py
│       ├── partition.py
│       ├── seat.py
│       └── table.py
├── frontend/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── files/
│       └── [Excel file templates]
├── tests/
│   └── [Test files]
├── docker-compose.yml
└── README.md
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.12.7 or higher

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ChristianValery/group-organizer.git
   cd group-organizer
   ```

2. Build and run the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Usage

1. Navigate to `http://localhost:8501` in your web browser.
2. Upload your `.xlsx` file containing the person names and constraints.
3. Specify the number of seats per table/group.
4. Generate and download the seating plan in Excel format.

## Dependencies

- **Backend:** FastAPI, [additional libraries listed in `backend/requirements.txt`]
- **Frontend:** Streamlit, [additional libraries listed in `frontend/requirements.txt`]

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
