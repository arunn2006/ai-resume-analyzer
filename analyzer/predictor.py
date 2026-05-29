def predict_category(skills):

    if "Python" in skills and "Django" in skills:
        return "Backend Developer"

    elif (
        "HTML" in skills and
        "CSS" in skills and
        "JavaScript" in skills
    ):
        return "Frontend Developer"

    elif (
        "Machine Learning" in skills or
        "Data Analytics" in skills
    ):
        return "Data Analyst"

    else:
        return "Software Developer"