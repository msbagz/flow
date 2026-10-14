# CampusFlow — AI-Native Engineering Sprint

**A Python Command-Line Helpdesk Ticket Management System**

## 1. Project Overview

### The Problem

Learn2Earn campus staff receive technical support requests involving Wi-Fi outages, faulty laptops, broken development environments, and inaccessible platforms. When these problems are reported informally, requests can be lost, priorities can become unclear, and responsibility may not be assigned.

### Our Solution

**CampusFlow** is a Python command-line application that helps campus staff record technical problems, calculate their priorities, assign responsibility, track progress, and monitor unresolved issues.

The application uses ordinary Python business logic to calculate ticket priorities and JSON files to preserve ticket data between sessions.

### Project Goals

* Record and validate support tickets.
* Automatically generate unique ticket IDs.
* Calculate ticket priority using specified rules.
* Assign tickets to responsible staff members.
* Track ticket status from open to resolved.
* Display an ordered queue of unresolved tickets.
* Generate reports showing ticket totals and breakdowns.
* Save and reload tickets using JSON.
* Verify functionality with automated tests.
* Demonstrate responsible AI-assisted learning and professional GitHub collaboration.

## 2. Team Members and Responsibilities

Update the placeholders below with the actual names and GitHub usernames of both fellows.

| Team member       | Role                              | Main responsibilities                                                                                                                                       |
| ----------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Fellow A's Name] | Engineer A                        | Ticket creation, input validation, priority calculation, and related automated tests.                                                                       |
| [Fellow B's Name] | Engineer B                        | Ticket assignment, status workflow, work queue, reporting, and related automated tests.                                                                     |
| Both fellows      | Integration and quality assurance | Agree on function contracts, integrate JSON persistence, review each other's pull requests, maintain AI learning logs, and prepare the final demonstration. |


## 3. Technology Stack

* **Language:** Python 3
* **Interface:** Command-line interface (CLI)
* **Data storage:** JSON
* **Automated testing:** Python's built-in `unittest` module
* **Version control:** Git
* **Collaboration and code review:** GitHub
* **AI-assisted learning:** AI tools used for explanations, experimentation, debugging, and critical evaluation

The project uses Python's standard library. No web framework, database server, AI SDK, or API key is required.

## 4. Project Features

CampusFlow must provide the following seven features through a menu that continues running until the user chooses Exit.

### F1 — Create Tickets

Users can create a support ticket by providing:

* `title`: Description of the reported problem.
* `category`: Type of technical issue.
* `urgency`: Reported urgency level.
* `affected_users`: Number of users affected.

The application validates the input, calculates priority, generates a unique ID, and stores the new ticket.

### F2 — List and View Tickets

Users can display all tickets or inspect an individual ticket by its ID.

### F3 — Assign Tickets

Users can assign a ticket to a named staff member. Blank staff names and unknown ticket IDs must be rejected.

### F4 — Manage Ticket Status

Tickets use three main statuses:

* `open`: The issue has been reported.
* `in_progress`: An assigned staff member is working on the issue.
* `resolved`: The issue has been fixed.

An unassigned ticket cannot move into `in_progress`. A resolved ticket must be explicitly reopened, setting its status to `open`, before it can be modified again.

### F5 — Display the Work Queue

The queue displays unresolved tickets in this priority order:

1. Critical
2. High
3. Medium
4. Low

Tickets with the same priority are ordered by their numeric ticket IDs, from earliest to latest. Resolved tickets are excluded.

### F6 — Generate Reports

Reports display:

* Total number of tickets.
* Ticket counts grouped by status.
* Ticket counts grouped by priority.

### F7 — JSON Persistence

Tickets are saved to JSON and reloaded when the application starts.

* A missing data file allows a fresh start.
* Malformed JSON produces a clear error rather than silently erasing data.
* Existing ticket IDs are preserved.
* New tickets must receive unique IDs after a restart.

## 5. Ticket Data Structure

Each ticket contains the following eight required fields:

| Field            | Description              | Example                  |
| ---------------- | ------------------------ | ------------------------ |
| `id`             | Unique ticket identifier | `"T001"`                 |
| `title`          | Problem description      | `"Campus Wi-Fi is down"` |
| `category`       | Type of issue            | `"Network"`              |
| `urgency`        | Reported urgency         | `"high"`                 |
| `affected_users` | Number of affected users | `15`                     |
| `priority`       | Calculated priority      | `"critical"`             |
| `status`         | Current workflow status  | `"open"`                 |
| `assigned_to`    | Responsible staff member | `None`                   |

Example ticket:

```python
{
    "id": "T001",
    "title": "Campus Wi-Fi is down",
    "category": "Network",
    "urgency": "high",
    "affected_users": 15,
    "priority": "critical",
    "status": "open",
    "assigned_to": None,
}
```

### Validation Rules

* Ticket IDs must be unique and automatically generated.
* Allowed categories are `Network`, `Hardware`, `Software`, and `Other`.
* Allowed urgency levels are `low`, `medium`, and `high`.
* Titles must not be blank.
* `affected_users` must be a positive integer; zero, negative numbers, decimals, and text are invalid.
* Valid case variations must be normalized consistently.
* Invalid inputs must produce useful errors without corrupting stored tickets.

## JSON Persistence Format

CampusFlow stores ticket records as a JSON array. Each ticket is a dictionary with these fields:

```json
[
  {
    "id": "T001",
    "title": "Campus Wi-Fi is down",
    "category": "Network",
    "urgency": "high",
    "affected_users": 15,
    "priority": "critical",
    "status": "open",
    "assigned_to": null,
    "notes": [
      {
        "note_id": "N001",
        "author": "Ada",
        "message": "Initial triage started."
      }
    ]
  }
]
```

Notes are optional in older data files. When they are absent after a load, the application normalizes them to an empty list instead of overwriting the source file. The save operation writes to a temporary file and then replaces the original file atomically so a crash cannot corrupt the current dataset.

## 6. Priority Calculation Rules

Ticket priority is calculated using ordinary Python business logic. AI is not used to determine ticket priority at runtime.

The rules must be evaluated in the following order, applying the first matching rule.

| Rule | Condition                                   | Result     |
| ---- | ------------------------------------------- | ---------- |
| 1    | High urgency AND at least 10 affected users | `critical` |
| 2    | High urgency OR at least 10 affected users  | `high`     |
| 3    | Medium urgency OR at least 3 affected users | `medium`   |
| 4    | All remaining valid tickets                 | `low`      |

Examples:

| Urgency | Affected users | Expected priority |
| ------- | -------------: | ----------------- |
| High    |             12 | Critical          |
| High    |              2 | High              |
| Low     |             10 | High              |
| Low     |              4 | Medium            |
| Medium  |              1 | Medium            |
| Low     |              1 | Low               |

## 7. Project Structure

The planned repository structure is:

```text
campusflow/
├── README.md
├── .gitignore
├── main.py
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py
│   ├── workflow.py
│   ├── storage.py
│   └── reports.py
├── tests/
│   ├── test_tickets.py
│   ├── test_workflow.py
│   └── test_storage.py
└── docs/
    ├── ai-learning-log.md
    └── design-decisions.md
```

### Module Responsibilities

| File                       | Responsibility                                                                                                                |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `main.py`                  | Displays the menu, collects user input, calls application functions, handles user-facing errors, and coordinates persistence. |
| `campusflow/tickets.py`    | Validates ticket fields, calculates priority, and creates ticket records.                                                     |
| `campusflow/workflow.py`   | Assigns tickets, manages status transitions, retrieves tickets, and builds the work queue.                                    |
| `campusflow/storage.py`    | Generates unique IDs and loads and saves JSON data.                                                                           |
| `campusflow/reports.py`    | Calculates totals and breakdowns by status and priority.                                                                      |
| `tests/test_tickets.py`    | Tests ticket creation, input validation, and priority rules.                                                                  |
| `tests/test_workflow.py`   | Tests assignment, lifecycle rules, ticket retrieval, and queue ordering.                                                      |
| `tests/test_storage.py`    | Tests JSON persistence, missing files, malformed JSON, and ID uniqueness after reload.                                        |
| `docs/design-decisions.md` | Records agreed function contracts, data structures, and design decisions.                                                     |
| `docs/ai-learning-log.md`  | Records each fellow's verified AI learning interactions.                                                                      |


## 8. Installation and Setup

### Prerequisites

Install Python 3 and Git. Python 3.10 or later is a suitable baseline for this project structure.

Verify the installations:

```bash
python --version
git --version
```

Depending on your operating system, you may need to use `python3` instead of `python`.

### Clone the Repository

Replace the URL with your team's actual GitHub repository URL.

```bash
git clone https://github.com/michaelbag8/campusflow-my
cd campusflow-my
```

### Optional: Create a Virtual Environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

CampusFlow uses the Python standard library, so installing external packages should not be necessary.

## 9. Running CampusFlow

From the project root, run:

```bash
python main.py
```

The CLI should present a menu containing the following options:

1. Create a ticket.
2. List all tickets.
3. View a ticket by ID.
4. Assign a ticket.
5. Change ticket status.
6. Display the work queue.
7. Generate a report.
8. Reopen a resolved ticket.
9. Exit.


## 10. Running Automated Tests

CampusFlow uses Python's built-in `unittest` framework.

Run the complete test suite from the repository root:

```bash
python -m unittest discover -s tests -v
```

The test cover:

* Successful ticket creation.
* Priority calculation and rule boundaries.
* Invalid input rejection.
* Assignment and unknown ticket IDs.
* Status transitions and assignment requirements.
* Reopening resolved tickets.
* Work queue priority ordering and numeric ID tie-breaking.
* Correct reports, including an empty ticket list.
* JSON save-and-load behavior.
* Unique ticket IDs after reloading existing tickets.


### Pull Request Links

* Engineer A's PR: [PR Link](https://github.com/yini-19/campusflow-my/pull/5#issue-5791514130)
* Engineer B's PR: [PR Link](https://github.com/yini-19/campusflow-my/pull/7#issue-5795730642)