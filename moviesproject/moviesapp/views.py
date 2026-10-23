from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie
from .forms import MovieForm
from django.http import JsonResponse
import requests
import json
import os

def home2(request):
    movies = Movie.objects.all()
    return render(request, "home.html", {"movies": movies})


def movie_create(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("catalog")
    else:
        form = MovieForm()

    return render(request, "movie_form.html", {"form": form, "title": "Novo filme"})

def movie_update(request, movie_id):
    movie = get_object_or_404(Movie, id = movie_id)
    if request.method == "POST":
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect("catalog")
    else:
        form = MovieForm(instance=movie)

    return render(request, "movie_form.html", {"form": form, "title": "Novo filme"})

def movie_delete(request, movie_id):
    movie = get_object_or_404(Movie, id = movie_id)
    if request.method == "POST":
        string_confirm = request.POST["Confirm"]
        if string_confirm == "Sim":
            movie.delete()
        return redirect("catalog")
    return render(request, "movie_delete.html", {"movie":movie})
    

GEMINI_API_KEY = ""
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

def call_bot(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use o método POST."}, status=405)

    body = json.loads(request.body)
    message = body.get("message", "")

    payload = {
        "system_instruction": {
            "parts": [{"text": "Você é o Cine Assistente da Lumière. Responda em português, de forma curta e simpática, com recomendações e curiosidades sobre filmes."}]
        },
        "contents": [
            {"role": "user", "parts": [{"text": message}]}
        ],
    }
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY,
    }

    response = requests.post(GEMINI_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return JsonResponse({"error": response.text}, status=502)

    response_json = response.json()
    print(response_json)
    reply = response_json["candidates"][0]["content"]["parts"][0]["text"]

    return JsonResponse({"reply": reply})


def home(request):
    response = requests.get("https://omdbapi.com/?apikey=38b4b85b&s=Batman&y=2022&type=movie")
    response_json = response.json()
    movies = response_json["Search"]
    context = {
        "movies": movies
    }

    return render(request, "index.html", context)

def chat(request):
    return render(request, "chat.html")

