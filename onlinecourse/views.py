from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Question, Choice, Submission


def submit(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        choice_id = request.POST.get("choice")
        choice = get_object_or_404(
            Choice, pk=choice_id, question=question
        )
        submission = Submission.objects.create(
            question=question,
            choice=choice,
            is_correct=choice.is_correct
        )
        return HttpResponse(
            "Answer submitted successfully. "
            f"Correct: {submission.is_correct}"
        )

    return HttpResponse("Please submit your answer using the exam form.")


def show_exam_result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    submissions = Submission.objects.filter(question=question)
    score = sum(1 for item in submissions if item.is_correct)

    return HttpResponse(
        f"Congratulations! Your score is {score}. "
        f"Exam results for: {question.question_text}"
    )
