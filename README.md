# Group Organizer / Seating Arrangement Tool

The **Group Organizer** (or **Seating Arrangement Tool**) is a web application designed to help users efficiently generate seating plans or group arrangements based on uploaded Excel files containing names and compatibility constraints. The tool allows users to specify the number of seats per table and downloads the generated seating plan as an Excel file.

The frontend is built with Streamlit for a simple and interactive user interface, while the backend API is built using FastAPI for robust server-side operations.

## Table of Contents

- [Features](#features)
- [Directory Structure](#directory-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Underlying Mathematical Model](#underlying-mathematical-model)

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

This project is licensed under the MIT License, a permissive open source license. This means you are free to use, modify, merge, distribute, and even sell copies of the software, provided that you include the original copyright notice and this permission notice in all copies or substantial portions of the software. The license also makes it clear that the software is provided "as is," without any warranty—neither expressed nor implied.

For the complete terms, please view it online at [opensource.org/licenses/MIT](https://opensource.org/licenses/MIT).

## Underlying Mathematical Model

Our approach to solving the seating arrangement problem (or group organization problem) were to formulate it as a constraint satisfaction problem (CSP) and solve it using the CP-SAT solver from Google OR-Tools.

Given a set $P=\{p_{0}, p_{1}, \dots, p_{n-1}\}$ of $n$ persons and $m$ the maximum number of persons that can be seated at a table, the goal is to partition $P$ into $k$ groups $G=\{G_{0}, G_{1}, \dots, G_{k-1}\}$ such that each group $G_{i}$ contains at most $m$ persons and the compatibility constraints are satisfied.

We assume that $m<n$ and consider the euclidean division of $n$, that is, $n = q \times m + r$ where $q$ is the quotient and $r$ is the remainder. Then the number of groups $k$ is then given by
\[
   k =%
   \begin{cases}
      q + 1 & \text{if } r \neq 0, \\
      q & \text{if } r = 0.
   \end{cases}
\]
Let $C$ be a set of pairs $(p_{i}, p_{j})$ of persons that are compatible with each other (must be seated at the same table), and $I$ be a set of pairs $(p_{i}, p_{j})$ of persons that are incompatible with each other (must not be seated at the same table).

The problem can be formulated as an integer linear programming (ILP) problem as follows:

#### Decision Variables

Let $x_{ij}$ be a binary variable that is equal to 1 if person $p_{i}$ is in group $G_{j}$, and 0 otherwise.

#### Constraints

1. Each person $p_{i}$ must be assigned to exactly one group $G_{j}$:
\[
   \sum_{j=0}^{k-1} x_{ij} = 1 \quad \text{for all } i \in \{0, 1, \dots, n-1\}.
\]

2. Each group $G_{j}$ must contain at least one person and at most $m$ persons:
\[
   1 \leq \sum_{i=0}^{n-1} x_{ij} \leq m \quad \text{for all } j \in \{0, 1, \dots, k-1\}.
\]

3. Persons $p_{i}$ and $p_{j}$ that are compatible must be assigned to the same group:
\[
   x_{ij} = x_{ji} \quad \text{for all } (p_{i}, p_{j}) \in C.
\]

4. Persons $p_{i}$ and $p_{j}$ that are incompatible must not be assigned to the same group:
\[
   x_{ij} + x_{ji} \leq 1 \quad \text{for all } (p_{i}, p_{j}) \in I.
\]
