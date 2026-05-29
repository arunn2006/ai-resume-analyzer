from django.shortcuts import render
from .forms import ResumeForm
from .pdf_utils import extract_text_from_pdf
from .skills import skills_list
from .jobs import job_roles
from .skill_gap import target_role_skills
from .courses import course_recommendations
from .predictor import predict_category


def home(request):

    extracted_text = ""
    found_skills = []
    recommended_jobs = []
    missing_skills = []
    recommended_courses = []

    ats_score = 0
    predicted_role = ""
    resume_summary = ""

    if request.method == "POST":

        form = ResumeForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            resume = form.save()

            extracted_text = extract_text_from_pdf(
                resume.resume_file.path
            )

            for skill in skills_list:

                if skill.lower() in extracted_text.lower():

                    found_skills.append(skill)

            if len(skills_list) > 0:

                ats_score = int(
                    (len(found_skills) / len(skills_list)) * 100
                )

            for skill in found_skills:

                if skill in job_roles:

                    job = job_roles[skill]

                    if job not in recommended_jobs:

                        recommended_jobs.append(job)

            target_skills = target_role_skills[
                "Full Stack Developer"
            ]

            for skill in target_skills:

                if skill not in found_skills:

                    missing_skills.append(skill)

            for skill in missing_skills:

                if skill in course_recommendations:

                    course = course_recommendations[skill]

                    if course not in recommended_courses:

                        recommended_courses.append(course)

            predicted_role = predict_category(
                found_skills
            )

            if found_skills:

                resume_summary = (
                    f"This candidate possesses skills in "
                    f"{', '.join(found_skills[:5])}. "
                    f"The profile is most suitable for "
                    f"{predicted_role} positions."
                )

    else:

        form = ResumeForm()

    return render(
        request,
        "index.html",
        {
            "form": form,
            "skills": found_skills,
            "ats_score": ats_score,
            "recommended_jobs": recommended_jobs,
            "missing_skills": missing_skills,
            "recommended_courses": recommended_courses,
            "predicted_role": predicted_role,
            "resume_summary": resume_summary
        }
    )