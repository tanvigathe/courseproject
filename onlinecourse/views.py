
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Question, Choice, Submission


def submit(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        selected_choice = get_object_or_404(
            Choice,
            pk=request.POST.get('choice'),
            question=question
        )

        submission = Submission.objects.create(
            question=question,
            choice=selected_choice,
            is_correct=selected_choice.is_correct
        )

        return render(
            request,
            'onlinecourse/exam_result.html',
            {
                'question': question,
                'submission': submission,
            }
        )

    return HttpResponse("Invalid request. Please submit your answer.")


def show_exam_result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    submissions = Submission.objects.filter(question=question)
    score = sum(1 for item in submissions if item.is_correct)

    return render(
        request,
        'onlinecourse/exam_result.html',
        {
            'question': question,
            'submissions': submissions,
            'score': score,
        }
    )
