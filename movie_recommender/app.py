from __future__ import annotations

from dataclasses import dataclass
from typing import List

from flask import Flask, render_template, request

app = Flask(__name__)


@dataclass(frozen=True)
class Movie:
    title: str
    genres: List[str]
    mood_tags: List[str]


MOVIES = [
    Movie("The Grand Adventure", ["Adventure", "Family"], ["uplifting", "lighthearted"]),
    Movie("Neon Nights", ["Sci-Fi", "Action"], ["intense", "futuristic"]),
    Movie("Quiet Lake", ["Drama", "Romance"], ["calm", "thoughtful"]),
    Movie("Laugh Out Loud", ["Comedy"], ["funny", "lighthearted"]),
    Movie("Hidden Clues", ["Mystery", "Thriller"], ["suspenseful", "dark"]),
    Movie("Skyline Dreams", ["Drama"], ["inspiring", "emotional"]),
    Movie("Pixel Quest", ["Adventure", "Fantasy"], ["imaginative", "whimsical"]),
    Movie("Sunset Bistro", ["Romance", "Comedy"], ["warm", "feel-good"]),
]


def build_recommendations(selected_title: str, mood: str) -> List[Movie]:
    if not selected_title:
        return []

    selected_movie = next(
        (movie for movie in MOVIES if movie.title == selected_title),
        None,
    )
    if not selected_movie:
        return []

    mood = mood.strip().lower()

    scored = []
    for movie in MOVIES:
        if movie.title == selected_movie.title:
            continue
        genre_overlap = len(set(movie.genres) & set(selected_movie.genres))
        mood_match = 1 if mood and mood in (tag.lower() for tag in movie.mood_tags) else 0
        score = genre_overlap * 2 + mood_match
        scored.append((score, movie))

    scored.sort(key=lambda item: (-item[0], item[1].title))
    return [movie for score, movie in scored if score > 0][:5]


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    selected_title = ""
    mood = ""
    recommendations: List[Movie] = []

    if request.method == "POST":
        selected_title = request.form.get("favorite_movie", "")
        mood = request.form.get("mood", "")
        recommendations = build_recommendations(selected_title, mood)

    return render_template(
        "index.html",
        movies=MOVIES,
        selected_title=selected_title,
        mood=mood,
        recommendations=recommendations,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
