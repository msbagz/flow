# CampusFlow — Individual AI Learning Log

### Fellow: YIYAKAZAH NICODEMUS 
### Role: Engineer A 
### Project: CampusFlow


# Interaction
# 1 — Validating Ticket Input

### Problem

CampusFlow requires users to provide valid information when creating a ticket. The ticket title must not be empty, the category must belong to a supported list, urgency must be low, medium, or high, and the number of affected users must be a positive integer.

I needed to understand how to validate user input in Python and prevent invalid information from being stored in the ticket system.

### My initial understanding

I understood how to collect information using Python's `input()` function, but I was unsure how to repeatedly request input when the user entered an invalid value. I also needed to understand how to validate different data types and handle variations in capitalization.

### Prompt to AI

"Explain how Python functions, while loops, and conditional statements can be used to validate user input. Use an unrelated example involving a student registration system. Show how to reject empty strings, restrict choices to a predefined list, and validate a positive integer. Do not write my CampusFlow implementation for me."

### Useful AI guidance

I learned that a `while True` loop can repeatedly request input until a valid value is entered. Conditional statements check whether the input meets specific requirements, while `return` exits the function once valid input has been obtained.

For example, a student registration system could validate a student's department:


```python
def validate_department():
    allowed_departments = ("Science", "Arts", "Business")

    while True:
        department = input("Enter department: ").strip().capitalize()

        if department in allowed_departments:
            return department

        print("Invalid department. Try again.")
```

The `strip()` method removes unnecessary spaces, while `capitalize()` normalizes the first letter. The function returns only when the department matches one of the allowed options.

I also learned that `isdigit()` can help validate positive whole-number input, although additional checks may be required depending on the accepted input format.

### My independent experiment/test

I planned to test the validation approach with the following inputs:

1. Enter a valid department such as `Science`.
2. Enter an unsupported department such as `Engineering`.
3. Enter a department with extra spaces, such as `science`.
4. Enter an empty value and check that the function requests input again.

I predicted that valid values would be accepted, unsupported values would be rejected, and surrounding spaces would be removed before validation.

### Decision

I accepted the approach of placing validation rules inside separate functions. In CampusFlow, I use this principle in `validate_title()`, `validate_category()`, `validate_urgency()`, and `validate_affected_users()`.

This keeps the input-validation logic separate from ticket creation and makes the program easier to understand and test.


### What I can now explain without AI

I can explain how loops and conditional statements enforce input rules. I understand that separate validation functions make code more organized and that input should be checked before it is used to create a ticket. I can also explain why stripping whitespace and normalizing capitalization improve the user experience.


# 2 — Calculating Ticket Priority

### Problem

CampusFlow must calculate ticket priority using two factors: urgency and the number of affected users. The result can be low, medium, high, or critical.

I needed to understand how to combine multiple conditions in Python and ensure that the most serious conditions take precedence over less serious ones.

### My initial understanding

I understood basic `if` and `else` statements, but I was less confident about combining conditions with `and` and `or`. I also needed to understand why the order of conditional branches matters when several conditions could apply to the same record.

### Prompt to AI

"Explain how Python's if, elif, else, and logical operators work when making decisions based on two variables. Use an unrelated example involving equipment maintenance, with severity and the number of affected machines. Explain why condition order matters and suggest test cases. Do not write my CampusFlow priority function."

### Useful AI guidance

I learned that Python uses logical operators to combine conditions:

- `and` requires both conditions to be true.
- `or` requires at least one condition to be true.
- `elif` checks another condition if the preceding condition was not satisfied.

For example, an equipment maintenance system could determine a response level:

```python
def maintenance_level(severity, affected_machines):
    if severity == "severe" and affected_machines >= 10:
        return "emergency"
    elif severity == "severe" or affected_machines >= 10:
        return "urgent"
    elif severity == "moderate" or affected_machines >= 3:
        return "normal"
    else:
        return "low"
```

I learned that the most serious condition should be checked first. Otherwise, a broader condition might match before the program reaches the more specific condition.

### My independent experiment/test

I planned to test the example using these cases:

1. Severe maintenance affecting 10 machines.
2. Severe maintenance affecting one machine.
3. Moderate maintenance affecting three machines.
4. Minor maintenance affecting one machine.

I predicted that the resulting levels would be emergency, urgent, normal, and low, respectively.

I would also test boundary values to confirm how the conditions behave when the number of affected machines changes from two to three and from nine to ten.


### Decision

I accepted the principle of evaluating the highest-priority condition first. In CampusFlow, `calculate_priority(urgency, affected_users)` applies the same approach to determine whether a ticket is critical, high, medium, or low.

I will use boundary-value tests to check that the conditions work correctly, particularly when urgency is high and when the affected-user count reaches the thresholds of three and ten.


### What I can now explain without AI

I can explain how logical operators combine conditions and why the order of `if` and `elif` branches affects the result. I understand that priority rules should be tested using normal cases, edge cases, and boundary values to ensure that each combination produces the expected result.

# 3 — Saving and Retrieving Tickets with JSON

### Problem

CampusFlow needs to preserve ticket information after the program closes. The current implementation stores tickets in a JSON file called `tickets.json`.

I needed to understand how Python reads and writes JSON data, how to handle multiple records, and how to avoid losing previously saved tickets when a new ticket is created.

### My initial understanding

I knew that Python could write information to a file, but I was unsure how to convert dictionaries into JSON and retrieve them later. I also needed to understand how to append a new ticket to an existing collection without overwriting earlier records.

### Prompt to AI

"Explain how Python's json module can store and retrieve a collection of dictionaries in a file. Use an unrelated example involving a collection of library equipment records. Show how to load existing records, append a new record, and write the collection back to the file. Explain how to test the process and handle an initially missing file. Do not write my CampusFlow storage functions."

### Useful AI guidance

I learned that Python's `json` module provides two important functions:

- `json.load()` reads JSON data from an open file and converts it into Python objects.
- `json.dump()` writes Python objects to a file in JSON format.

For example, a library equipment system could store records as follows:


```python
import json

equipment = [
    {"asset_id": "A001", "condition": "good"},
    {"asset_id": "A002", "condition": "repair"},
]

with open("equipment.json", "w") as file:
    json.dump(equipment, file, indent=4)
```

The `indent=4` argument makes the saved JSON easier to read.

I also learned that if the file does not exist, the program can start with an empty list. If it already exists, the program should load the saved records before adding a new one. The complete collection can then be written back to the file.

### My independent experiment/test

I planned to conduct these experiments:

1. Save two equipment records to a new JSON file.
2. Read the file and verify that both records are present.
3. Append a third record and save the collection again.
4. Reload the file and confirm that all three records remain.
5. Repeat the experiment when the file does not initially exist.

I predicted that the first run would create the file and that subsequent runs would preserve earlier records while adding new ones.

### Decision

I accepted the approach of loading existing records, appending a new dictionary, and writing the complete list back to the file. In CampusFlow, the `save_ticket()` function follows this pattern.

I also learned that a JSON file may contain either a single dictionary or a list of dictionaries. My current implementation checks for a dictionary and converts it into a list so that ticket operations can work with a consistent collection.

For further improvement, I would test how the program behaves if the JSON file contains invalid or corrupted data, because the current implementation does not explicitly recover from every possible file-reading error.


### What I can now explain without AI

I can explain how dictionaries represent individual records and how a list of dictionaries can represent multiple records. I understand how `json.load()` retrieves saved information and how `json.dump()` persists updates. I can also explain why existing records must be loaded before adding a new ticket if the program is to preserve previously saved data.

## Final Reflection

These three learning interactions helped me understand input validation, conditional logic, and JSON persistence in Python. They directly relate to the current CampusFlow implementation.

### Evidence Checklist

- [ ]I tested the priority calculation with normal cases and boundary values.
- [ ]I tested saving, loading, and appending JSON records.
- [ ]I recorded the actual output rather than relying only on predicted results.
- [ ]I updated the filenames and test names to match my implementation.
- [ ]I added actual commit SHAs or PR links where available.
- [ ]I can explain the three concepts without AI assistance.


# CampusFlow — Individual AI Learning Log

**Fellow:** Michael Bulus
**Role:** Engineer B
**Project:** CampusFlow

---
## Interaction 
# 1 — JSON Persistence in Python

**Problem:**

I needed to understand how CampusFlow can save support tickets to a JSON file and load them again when the application restarts. I also needed to understand the difference between `json.dump()` and `json.load()`.

**My initial understanding:**

I knew that JSON stores data in a file, but I was not sure how Python converts dictionaries and lists into JSON or how it retrieves the saved information. I also thought `json.dump()` and `json.load()` might perform the same operation.

**Prompt to AI:**

"Explain `json.dump()`, `json.load()` and JSON persistence with examples. Use a small Python example unrelated to CampusFlow. Explain how data is saved to a file and loaded again, and give me a small experiment I can run to verify the result."

**Useful AI guidance:**

I learned that Python's `json` module provides different functions for writing and reading JSON data.

* `json.dump(data, file)` converts Python data into JSON and writes it to a file.
* `json.load(file)` reads JSON from a file and converts it back into Python data.
* JSON persistence means saving data so it can be recovered after a program stops.

Example:

```python
import json

student = {
    "name": "Ada",
    "score": 85
}

with open("student.json", "w", encoding="utf-8") as file:
    json.dump(student, file)

with open("student.json", "r", encoding="utf-8") as file:
    loaded_student = json.load(file)

print(loaded_student)
```

Expected output:

```text
{'name': 'Ada', 'score': 85}
```

**My independent experiment/test:**

I planned to run the example and predict that the loaded dictionary would contain the same values as the original dictionary. I would then change the score, save the dictionary again, and reload it to check whether the new value was preserved.

**Verification source or result:**

[Record the actual output from your experiment and confirm whether the saved and loaded values matched.]

Reference: Python documentation — https://docs.python.org/3/library/json.html

**Decision:**

I accepted the explanation after checking the Python documentation and running the example. I understood that saving data and loading data are separate operations.

**Related file/commit:**

* File: `campusflow/storage.py`
* Test: `test_save_and_load_tickets` (planned test name; replace with the actual test name)
* Commit/PR: [Add actual commit SHA or PR link]

**What I can now explain without AI:**

`json.dump()` saves Python data to a JSON file, while `json.load()` reads that file and recreates the corresponding Python data. CampusFlow needs both so tickets are not lost when the application closes. I also need to test that the saved tickets can be loaded correctly after restarting the program.

---

## Interaction #2 — Python Exceptions and Input Validation

**Problem:**

CampusFlow must reject invalid inputs, such as a blank ticket title, zero affected users, or an unknown ticket ID. I needed to understand how Python exceptions help handle these errors without crashing the application or changing ticket data incorrectly.

**My initial understanding:**

I knew that invalid input could cause a problem, but I was not sure when to use `raise` and when to use `try` and `except`. I also wanted to understand how to show a useful error message to the user.

**Prompt to AI:**

"Explain Python exceptions, `raise`, `try`, and `except` using a small example unrelated to CampusFlow. Show how to reject an invalid value and handle the error without terminating the whole program. Give me an experiment to verify the behavior."

**Useful AI guidance:**

I learned that:

* `raise` signals that an operation cannot continue because a condition is invalid.
* `try` contains code that might raise an exception.
* `except` handles a matching exception.
* A function can raise a clear exception while the CLI catches it and displays a friendly message.

Example:

```python
def divide(a, b):
    if b == 0:
        raise ValueError("The divisor cannot be zero.")
    return a / b


try:
    print(divide(10, 0))
except ValueError as error:
    print(f"Error: {error}")
```

Expected output:

```text
Error: The divisor cannot be zero.
```

**My independent experiment/test:**

I planned to run the example twice: first with a divisor of zero, then with a valid divisor such as two. The first call should raise a `ValueError`, while the second should return `5.0`. I would verify that the error is handled by the `except` block.

**Verification source or result:**

[Record the actual output from both runs and whether the observed behavior matched the prediction.]

Reference: Python documentation — https://docs.python.org/3/tutorial/errors.html

**Decision:**

I accepted the approach after verifying the example. For CampusFlow, I will use exceptions for invalid operations and handle expected errors in `main.py`. I will avoid catching every possible exception indiscriminately because that could hide programming errors.

**Related file/commit:**

* File: `campusflow/tickets.py` or `campusflow/workflow.py`
* Test: [Add the actual invalid-input or unknown-ticket test name]
* Commit/PR: [Add actual commit SHA or PR link]

**What I can now explain without AI:**

`raise` allows a function to reject invalid data, while `try` and `except` allow the calling code to respond appropriately. In CampusFlow, a blank title or unknown ticket ID should produce a clear error instead of causing an incorrect update.

---

## Interaction #3 — Automated Testing with Python `unittest`

**Problem:**

CampusFlow must have at least eight meaningful automated tests. I needed to understand how to write a test that checks whether a function returns the expected result and how to test invalid inputs.

**My initial understanding:**

I understood that tests help find bugs, but I was unsure how `unittest` discovers test methods, how assertions work, and how to test a function that is expected to raise an exception.

**Prompt to AI:**

"Explain Python's `unittest` module with a small example unrelated to CampusFlow. Show how to test a normal result, an incorrect input, and an expected exception. Explain how to run the test and interpret the output."

**Useful AI guidance:**

I learned that `unittest.TestCase` provides methods for checking expected behavior.

* `assertEqual(actual, expected)` checks whether two values are equal.
* `assertTrue(condition)` checks whether a condition is true.
* `assertRaises(ExceptionType)` checks whether an operation raises the expected exception.

Example:

```python
import unittest


def square(number):
    if not isinstance(number, (int, float)) or isinstance(number, bool):
        raise ValueError("A number is required.")
    return number * number


class TestSquare(unittest.TestCase):

    def test_square_positive_number(self):
        self.assertEqual(square(4), 16)

    def test_square_zero(self):
        self.assertEqual(square(0), 0)

    def test_reject_invalid_input(self):
        with self.assertRaises(ValueError):
            square("four")


if __name__ == "__main__":
    unittest.main()
```

Save the example as `test_square.py` and run:

```bash
python -m unittest -v test_square
```

**My independent experiment/test:**

I planned to run the three tests and predict that all would pass. I would then temporarily change the expected result from `16` to `15` and rerun the tests to observe how `unittest` reports a failure. Afterward, I would restore the correct assertion.

**Verification source or result:**

[Record the actual test output, including the number of tests run and whether they passed. Also record the result of the temporary incorrect assertion.]

Reference: Python documentation — https://docs.python.org/3/library/unittest.html

**Decision:**

I accepted the testing approach after verifying the example. I learned that a test should contain a clear expectation and assertion, and that a failing test can reveal a mismatch between the implementation and the expected behavior.

**Related file/commit:**

* File: `tests/test_tickets.py` or `tests/test_workflow.py`
* Test: [Add the actual test name]
* Commit/PR: [Add actual commit SHA or PR link]

**What I can now explain without AI:**

`unittest` lets me verify program behavior automatically. I can test successful operations, invalid inputs, and expected exceptions without manually interacting with the CLI. In CampusFlow, this helps verify priority rules, ticket assignment, workflow restrictions, and JSON persistence before the changes are merged into `main`.

---

## Final Reflection

Through these learning interactions, I learned about JSON persistence, exception handling, and automated testing. I understand how these concepts contribute to a reliable command-line application.

My next step is to apply the concepts to CampusFlow, run the relevant tests, inspect the actual output, and document any corrections or improvements I make after verification.

**Evidence checklist:**

* [ ] Ran the JSON experiment and recorded the actual result.
* [ ] Ran the exception-handling experiment and recorded the actual result.
* [ ] Ran the `unittest` experiment, including the deliberate failure.
* [ ] Updated each entry with actual test names and project files.
* [ ] Added real commit SHAs or pull request links where available.
* [ ] Can explain each concept without reading the AI response.
* [ ] Documented at least one AI suggestion that I independently corrected, improved, or rejected after checking it.
