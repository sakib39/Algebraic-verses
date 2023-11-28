from django.shortcuts import render,get_object_or_404, redirect
from .models import Category, Problem
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
import json

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'problems/category_list.html', {'categories': categories})

def problem_list(request, category_id):
    category = Category.objects.get(pk=category_id)
    subcategories = category.subcategories.all()
    problems = Problem.objects.filter(sub_category__in=subcategories)
    return render(request, 'problems/problem_list.html', {'category': category, 'problems': problems})

# def problem_answer(request, problem_id):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_answer = data.get('answer', '') == 'True'
#         problem = get_object_or_404(Problem, pk=problem_id)
#         sub_category = problem.sub_category

#         mastery = request.session.get('mastery', {})
#         sub_mastery = mastery.get(str(sub_category.id), {'correct_streak': 0, 'incorrect_streak': 0, 'mastered': False})

#         if user_answer == problem.answer:
#             sub_mastery['correct_streak'] += 1
#             sub_mastery['incorrect_streak'] = 0
#             if sub_mastery['correct_streak'] >= 2:
#                 sub_mastery['mastered'] = True
#                 response_data = {'message': 'Sub-category mastered!'}
#             else:
#                 response_data = {'message': 'Correct! Answer one more correctly to master this sub-category.'}
#         else:
#             sub_mastery['incorrect_streak'] += 1
#             sub_mastery['correct_streak'] = 0
#             if sub_mastery['incorrect_streak'] >= 2:
#                 response_data = {'message': 'Incorrect twice. Showing answer: {}'.format(problem.solution)}
#                 sub_mastery['incorrect_streak'] = 0  # Reset after showing answer
#             else:
#                 response_data = {'message': 'Incorrect. Try again.'}

#         mastery[str(sub_category.id)] = sub_mastery
#         request.session['mastery'] = mastery
#         request.session.modified = True

#         return JsonResponse(response_data)

def problem_answer(request, problem_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_answer = data.get('answer', '') == 'True'
        problem = get_object_or_404(Problem, pk=problem_id)
        sub_category = problem.sub_category

        # Initialize or get the mastery tracking from the session
        mastery = request.session.get('mastery', {})
        sub_mastery = mastery.get(str(sub_category.id), {
            'correct_streak': 0,
            'incorrect_streak': 0,
            'mastered': False
        })

        # Prepare the base response data
        response_data = {}

        # Check the user's answer against the actual answer
        if user_answer == problem.answer:
            sub_mastery['correct_streak'] += 1
            sub_mastery['incorrect_streak'] = 0
            if sub_mastery['correct_streak'] >= 2:
                sub_mastery['mastered'] = True
                response_data['message'] = 'Sub-category mastered!'
            else:
                response_data['message'] = 'Correct! Answer one more correctly to master this sub-category.'
        else:
            sub_mastery['incorrect_streak'] += 1
            sub_mastery['correct_streak'] = 0
            if sub_mastery['incorrect_streak'] >= 2:
                response_data['message'] = 'Incorrect twice.'
                response_data['solution'] = problem.solution
                response_data['show_solution'] = True
                sub_mastery['incorrect_streak'] = 0  # Reset after showing answer
            else:
                response_data['message'] = 'Incorrect. Try again.'

        # Save the updated mastery tracking in the session
        mastery[str(sub_category.id)] = sub_mastery
        request.session['mastery'] = mastery
        request.session.modified = True

        # Return the JSON response
        return JsonResponse(response_data)