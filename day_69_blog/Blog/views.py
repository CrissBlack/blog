from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from flask_login import login_required, current_user
from datetime import datetime as dt
from .forms import NewPostForm, CommentForm
from .models import Article, Comment, db
from functools import wraps
views = Blueprint('views', __name__)

def administrator(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if current_user.id != 1:
            abort(401)
        return func(*args, **kwargs)
    return inner


@views.route('/')
def home():
    all_articles = db.session.query(Article)
    return render_template('index.html', articles=all_articles)

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/contact')
def contact():
    return render_template('contact.html')

@views.route('/article/<article_id>', methods=['get', 'post'])
def show_article(article_id):
    comment_form = CommentForm()
    article = db.session.get(Article, article_id)


    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You can't comment. Log in first!")
            return redirect(url_for('login'))
        else:
            comment = Comment(text=comment_form.body.data, poster_id=current_user.id, article_id=article.id)
            db.session.add(comment)
            db.session.commit()
    return render_template('post.html', article=article, comment_form=comment_form, gravatar=gravatar)

@views.route('/add_article', methods=['get', 'post'])
def add_article():
    form = NewPostForm()
    if form.validate_on_submit():
        formatted_now = dt.now().strftime('%d %B, %Y')
        new_article = Article(title=form.title.data, subtitle=form.subtitle.data, img_url=form.img_url.data,
                           date=formatted_now, body=form.body.data, author_id=current_user.id)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template('make-post.html', form=form, is_edit=0)

@views.route('edit_post/<article_id>', methods=['get', 'post'])
@login_required
def edit_article(article_id):
    article = Article.query.get(article_id)
    form = NewPostForm(obj=article)


    if form.validate_on_submit():
        form.populate_obj(obj=article)
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template('make-post.html', form=form, article=article, is_edit=1)


@views.route('/delete')
@login_required
@administrator
def delete_article():
    article_id = request.args['article_id']
    article = Article.query.get(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('views.home'))


