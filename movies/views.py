from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Review, Comment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ReviewForm, CommentForm, ReplyForm
from django.contrib import messages


def home(request):
    # Получаем 10 популярных фильмов, отсортированных по убыванию голосов
    popular_movies = Movie.objects.order_by('-votes')[:10]

    # Получаем 10 новых фильмов, отсортированных по году выпуска
    new_movies = Movie.objects.order_by('-release_year')[:10]

    return render(request, 'movies/home.html', {
        'popular_movies': popular_movies,
        'new_movies': new_movies,
    })


def search_movies(request):
    query = request.GET.get('q')  # Получаем запрос из строки поиска
    movies = Movie.objects.filter(title__icontains=query) if query else Movie.objects.none()  # Поиск или пустой список
    return render(request, 'movies/search_results.html', {'movies': movies, 'query': query})


def movie_detail(request, title_id):
    # Получаем фильм с использованием prefetch_related
    movie = get_object_or_404(
        Movie.objects.prefetch_related(
            'directors', 'actors', 'producers', 'reviews__user', 'reviews__comments__user', 'reviews__comments__replies__user'
        ),
        title_id=title_id
    )
    
    # Получаем все отзывы для фильма
    reviews = movie.reviews.all()

    # Проверка, оставил ли пользователь отзыв
    user_has_reviewed = movie.reviews.filter(user=request.user).exists() if request.user.is_authenticated else False

    # Инициализируем формы
    form = ReviewForm()
    comment_form = CommentForm()
    reply_form = ReplyForm()  # форма для подкомментариев

    if request.method == 'POST':
        # Обработка отзыва
        if 'review' in request.POST and not user_has_reviewed:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.movie = movie
                review.save()
                messages.success(request, "Ваш отзыв был добавлен!")
                return redirect('movie_detail', title_id=movie.title_id)

        # Обработка комментария
        elif 'comment' in request.POST:
            review_id = request.POST.get('review_id')
            review = get_object_or_404(Review, id=review_id)
            parent_id = request.POST.get('parent_id')
            parent_comment = None
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)

            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.review = review  # Связываем комментарий с отзывом
                comment.parent = parent_comment
                comment.save()
                messages.success(request, "Ваш комментарий был добавлен!")
                return redirect('movie_detail', title_id=movie.title_id)

        # Обработка подкомментария (ответа)
        elif 'reply' in request.POST:
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                comment_id = request.POST.get('comment_id')
                comment = get_object_or_404(Comment, id=comment_id)
                reply = reply_form.save(commit=False)
                reply.user = request.user
                reply.parent = comment
                # Связываем подкомментарий с отзывом, если родительский комментарий связан с отзывом
                if comment.review:
                    reply.review = comment.review  # Устанавливаем отзыв для подкомментария
                reply.save()
                messages.success(request, "Ваш подкомментарий был добавлен!")
                return redirect('movie_detail', title_id=movie.title_id)

        # Обработка удаления комментария
        elif 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            if request.user.profile.role == 'admin':
                comment.deleted = True  # Устанавливаем флаг "удалено"
                comment.save()
                messages.success(request, "Комментарий удален администратором.")
            return redirect('movie_detail', title_id=movie.title_id)

    # Передаем все данные в шаблон
    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'form': form,
        'reviews': reviews,
        'user_has_reviewed': user_has_reviewed,
        'actors': movie.actors.all(),
        'director': movie.directors,
        'producers': movie.producers.all(),
        'comment_form': comment_form,
        'reply_form': reply_form,  # передаем форму для подкомментариев
    })

@login_required
def toggle_like(request, title_id):
    movie = get_object_or_404(Movie, title_id=title_id)
    profile = request.user.profile

    if movie in profile.liked_movies.all():
        profile.liked_movies.remove(movie)  # Удаляем фильм из списка
    else:
        profile.liked_movies.add(movie)  # Добавляем фильм в список

    return redirect('movie_detail', title_id=title_id) 


@login_required
def add_review(request, title_id):
    movie = get_object_or_404(Movie, title_id=title_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return HttpResponseRedirect(reverse('movie_detail', args=[title_id]))
    else:
        form = ReviewForm()

    return render(request, 'movies/add_review.html', {'form': form, 'movie': movie})
