
from django.shortcuts import get_object_or_404, render, redirect
from .models import Course, Question, Choice, Submission


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
        question_id = request.POST.get("question_id")
        choice_id = request.POST.get("choice")

        question = get_object_or_404(
            Question, pk=question_id, course=course
        )
        choice = get_object_or_404(
            Choice, pk=choice_id, question=question
        )

        submission = Submission.objects.create(
            question=question,
            choice=choice,
            is_correct=choice.is_correct
        )

        return redirect(
            "show_exam_result",
            course_id=course.id,
            submission_id=submission.id
        )

    return redirect("/")


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        question__course=course
    )

    submissions = Submission.objects.filter(
        question__course=course
    )
    score = sum(1 for item in submissions if item.is_correct)

    return render(
        request,
        "onlinecourse/exam_result.html",
        {
            "course": course,
            "submission": submission,
            "submissions": submissions,
            "score": score,
        }
    )
