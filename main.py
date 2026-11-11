
import json
import logging

from ollama import chat
from pydantic import BaseModel, Field, ValidationError


# ---------------------------------------
# 1. Logging Configuration
# ---------------------------------------

logging.basicConfig(
    filename="agent.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


# ---------------------------------------
# 2. Student Data Model (8 Fields)
# ---------------------------------------

class Student(BaseModel):
    name: str
    age: int | None = None
    department: str | None = None
    college: str | None = None
    skills: list[str] = Field(default_factory=list)
    career_goal: str | None = None
    experience: str | None = None
    certifications: list[str] = Field(default_factory=list)


# ---------------------------------------
# 3. Multiple Student Collection
# ---------------------------------------

class StudentCollection(BaseModel):
    students: list[Student]


# ---------------------------------------
# 4. Agent Configuration
# ---------------------------------------

MODEL_NAME = "qwen2.5:1.5b"
MAX_RETRIES = 3


# ---------------------------------------
# 5. Main AI Extraction Function
# ---------------------------------------

def generate_student_data(student_information):

    messages = [
        {
            "role": "system",
            "content": """
You are a professional student information extraction agent.

Your task is to identify and extract ALL students
mentioned in the user's input.

IMPORTANT RULES:

1. Extract every student separately.
2. Never combine information from different students.
3. Extract exactly these 8 fields for each student:

   - name
   - age
   - department
   - college
   - skills
   - career_goal
   - experience
   - certifications

4. Do not invent or guess information.
5. If information is missing, use null for scalar fields.
6. For missing skills or certifications, use an empty list.
7. Skills must be returned as a list of strings.
8. Certifications must be returned as a list of strings.
9. Return one JSON object containing a "students" array.
10. Return only valid JSON matching the given schema.

Example structure:

{
    "students": [
        {
            "name": "Rahul",
            "age": 22,
            "department": "Computer Science",
            "college": "ABC College",
            "skills": ["Python", "Java"],
            "career_goal": "Software Developer",
            "experience": "Fresher",
            "certifications": ["Python Certificate"]
        }
    ]
}
"""
        },
        {
            "role": "user",
            "content": student_information
        }
    ]

    # -----------------------------------
    # 6. Retry Mechanism
    # -----------------------------------

    for attempt in range(1, MAX_RETRIES + 1):

        ai_output = None

        try:

            logger.info(
                "Starting extraction attempt %s",
                attempt
            )

            response = chat(
                model=MODEL_NAME,
                messages=messages,
                format=StudentCollection.model_json_schema(),
                options={
                    "temperature": 0
                }
            )

            ai_output = response.message.content

            # -----------------------------------
            # 7. JSON Parsing
            # -----------------------------------

            parsed_data = json.loads(ai_output)

            # -----------------------------------
            # 8. Pydantic Validation
            # -----------------------------------

            student_collection = (
                StudentCollection.model_validate(parsed_data)
            )

            logger.info(
                "Successfully extracted %s students",
                len(student_collection.students)
            )

            return student_collection

        except json.JSONDecodeError as error:

            error_message = f"Invalid JSON: {error}"

            logger.warning(
                "Attempt %s failed: %s",
                attempt,
                error_message
            )

        except ValidationError as error:

            error_message = f"Validation failed: {error}"

            logger.warning(
                "Attempt %s failed: %s",
                attempt,
                error_message
            )

        except Exception:

            logger.exception(
                "Unexpected error during extraction"
            )

            return None

        # -----------------------------------
        # 9. Retry with Correction
        # -----------------------------------

        if attempt < MAX_RETRIES:

            if ai_output is not None:
                messages.append(
                    {
                        "role": "assistant",
                        "content": ai_output
                    }
                )

            messages.append(
                {
                    "role": "user",
                    "content": (
                        "Your previous response was invalid. "
                        "Correct the response and return valid "
                        "JSON matching the required schema. "
                        "Do not invent missing information. "
                        + error_message
                    )
                }
            )

    logger.error(
        "All extraction attempts failed."
    )

    return None


# ---------------------------------------
# 10. Run from Terminal
# ---------------------------------------

if __name__ == "__main__":

    print("\n===================================")
    print("   STRUCTURED OUTPUT AGENT")
    print("===================================\n")

    student_information = input(
        "Enter information about students:\n"
    )

    result = generate_student_data(
        student_information
    )

    if result is not None:

        print("\nExtraction Successful!\n")

        print(
            result.model_dump_json(indent=4)
        )

        print(
            f"\nTotal Students Extracted: "
            f"{len(result.students)}"
        )

    else:

        print(
            "\nCould not generate valid student data."
        )
