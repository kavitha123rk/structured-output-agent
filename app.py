
import streamlit as st
from main import generate_student_data


# ---------------------------------------
# 1. Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="AI Student Data Extractor",
    page_icon="🤖",
    layout="wide"
)


# ---------------------------------------
# 2. Professional Header
# ---------------------------------------

st.title("🤖 AI-Powered Student Information Extractor")

st.markdown(
    """
    **Turn unstructured text into structured intelligence.**

    Extract multiple student profiles automatically using
    AI, Python, Ollama, and Pydantic validation.
    """
)

st.divider()


# ---------------------------------------
# 3. Input Section
# ---------------------------------------

st.subheader("📝 Enter Student Information")

student_information = st.text_area(
    "Paste information about one or more students:",
    placeholder=(
        "Example:\n\n"
        "Rahul is 22 years old and studies Computer Science "
        "at ABC College. He knows Python, Java and SQL. "
        "His career goal is to become a Software Developer. "
        "He is a fresher and has a Python certification.\n\n"
        "Priya is 21 years old and studies Information Science "
        "at XYZ College. She knows Python, HTML and CSS. "
        "She wants to become a Data Scientist. "
        "She completed a Python certification."
    ),
    height=230
)


# ---------------------------------------
# 4. Extraction Button
# ---------------------------------------

if st.button(
    "🚀 Extract Student Information",
    type="primary",
    use_container_width=True
):

    if not student_information.strip():

        st.warning(
            "Please enter student information first."
        )

    else:

        try:

            with st.spinner(
                "AI is analyzing and extracting student records..."
            ):

                result = generate_student_data(
                    student_information
                )

            if result is not None and result.students:

                st.success(
                    f"Successfully extracted "
                    f"{len(result.students)} student record(s)!"
                )

                st.divider()

                # -----------------------------------
                # 5. Summary
                # -----------------------------------

                st.subheader("📊 Extraction Summary")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Total Students",
                        len(result.students)
                    )

                with col2:
                    st.metric(
                        "Fields Per Student",
                        8
                    )

                st.divider()

                # -----------------------------------
                # 6. Display All Students
                # -----------------------------------

                st.subheader("👨‍🎓 Extracted Student Profiles")

                for index, student in enumerate(
                    result.students,
                    start=1
                ):

                    with st.container(border=True):

                        st.markdown(
                            f"### Student {index}: {student.name}"
                        )

                        col1, col2 = st.columns(2)

                        with col1:

                            st.write("**Name**")
                            st.write(student.name)

                            st.write("**Age**")
                            st.write(
                                student.age
                                if student.age is not None
                                else "Not provided"
                            )

                            st.write("**Department**")
                            st.write(
                                student.department or "Not provided"
                            )

                            st.write("**College**")
                            st.write(
                                student.college or "Not provided"
                            )

                        with col2:

                            st.write("**Skills**")
                            st.write(
                                ", ".join(student.skills)
                                if student.skills
                                else "Not provided"
                            )

                            st.write("**Career Goal**")
                            st.write(
                                student.career_goal or "Not provided"
                            )

                            st.write("**Experience**")
                            st.write(
                                student.experience or "Not provided"
                            )

                            st.write("**Certifications**")
                            st.write(
                                ", ".join(student.certifications)
                                if student.certifications
                                else "Not provided"
                            )

                        with st.expander(
                            f"View Student {index} JSON"
                        ):

                            st.json(student.model_dump())

                st.divider()

                # -----------------------------------
                # 7. Complete JSON Output
                # -----------------------------------

                st.subheader("📄 Complete Structured JSON")

                student_json = result.model_dump_json(
                    indent=4
                )

                st.code(
                    student_json,
                    language="json"
                )

                # -----------------------------------
                # 8. Download JSON
                # -----------------------------------

                st.download_button(
                    label="⬇️ Download All Student Data (JSON)",
                    data=student_json,
                    file_name="students_data.json",
                    mime="application/json",
                    use_container_width=True
                )

            elif result is not None:

                st.warning(
                    "No student records were found. "
                    "Please provide clearer student information."
                )

            else:

                st.error(
                    "Could not extract valid student information. "
                    "Check that Ollama is running and Qwen is installed."
                )

        except Exception as error:

            st.error("Something went wrong.")

            st.exception(error)


# ---------------------------------------
# 9. Footer
# ---------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:gray;">
        <p>Built with Python | Ollama | Qwen 2.5 | Pydantic | Streamlit</p>
        <p>AI-Powered Structured Data Extraction Agent</p>
    </div>
    """,
    unsafe_allow_html=True
)
