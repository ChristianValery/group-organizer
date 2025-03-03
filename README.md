# Group Organizer / Seating Arrangement Tool

The **Group Organizer / Seating Arrangement Tool** is a web application designed to streamline the process of creating seating arrangements or group assignments based on user-provided data. By leveraging advanced algorithms, it efficiently generates optimal seating plans that satisfy specified constraints and requirements.

## Table of Contents

- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage Guide](#usage-guide)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Mathematical Model](#mathematical-model)

## Key Features

- **Excel File Upload**: Effortlessly upload `.xlsx` files containing attendees' names and compatibility constraints.
- **Customizable Seating**: Specify the number of seats per table/group to tailor the arrangement to your needs.
- **Automated Arrangement**: Generate seating plans that respect all constraints, formatted for easy implementation.
- **User-Friendly Interface**: Built with Streamlit for an interactive and intuitive frontend experience.
- **Robust Backend**: FastAPI ensures efficient and scalable backend operations.

## Project Structure

```
group-organizer/
├── backend/
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── database/
│   │   └── [SQLite database files]
│   ├── files/
│   │   └── [Generated Excel files]
│   └── utils/
│       ├── excel_handler.py
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

- Install **Docker** and **Docker Compose**.
- Ensure you have **Python 3.12.7** or higher.

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

## Usage Guide

1. Open your web browser and navigate to `http://localhost:8501`.
2. Upload your `.xlsx` file containing attendee information and seating constraints.
3. Define the desired number of seats per table or group.
4. Generate the seating plan and download it in Excel format.

## Dependencies

- **Backend**: FastAPI, along with other libraries listed in `backend/requirements.txt`.
- **Frontend**: Streamlit, along with other libraries listed in `frontend/requirements.txt`.

## Contributing

We welcome contributions to enhance this tool. Here’s how you can help:

1. Fork the repository.
2. Create a branch for your feature (`git checkout -b feature/YourFeature`).
3. Commit your modifications (`git commit -am 'Add feature'`).
4. Push to your branch (`git push origin feature/YourFeature`).
5. Submit a Pull Request for review.

## License

This project is licensed under the MIT License, allowing for flexibility in use and distribution. You are free to use, modify, distribute, and even sell copies of the software, provided that proper credit is given. For full details, refer to [opensource.org/licenses/MIT](https://opensource.org/licenses/MIT).

## Mathematical Model

The seating arrangement problem is modeled as a Constraint Satisfaction Problem (CSP) and solved using the CP-SAT solver from Google OR-Tools. The solution involves partitioning individuals into groups based on given constraints, ensuring maximum compatibility and satisfying all requirements.

For a detailed description of the mathematical approach and constraints, please refer to the complete model section in the documentation.
