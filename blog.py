from flask import Flask, render_template, request, redirect, url_for, flash, session
import devless, datetime

devless = devless.Sdk("http://localhost:3000", "7f0449c4d77ade309aa26ef0a9de6bbe")

def get_posts():
	results = devless.get_data('blog', 'post')
	return results

def get_post_by_id(id):
	results = devless.where('id', id).get_data('blog', 'post')
	return results

def add_blog_post(title, subtitle, author, text):
	date = str(datetime.datetime.now())[:16]
	data = {'title': title, 'subtitle': subtitle, 'author': author, 'pubdate': date, 'text': text}
	results = devless.add_data('blog', 'post', data)
	print results

def update_post(id, title, subtitle, author, text):
	data = {'title': title, 'subtitle': subtitle, 'author': author, 'text': text}
	results = devless.where('id', id).update_data('blog', 'post', data)
	print results

def delete_post(id):
	results = devless.where('id', id).delete_data('blog', 'post')
	print results

app = Flask(__name__)

app.secret_key = 'whatever'

@app.route('/')
def blog():
	all_posts = get_posts()
	posts = all_posts['payload']['results']
	posts = sorted(posts, key=lambda k: k['id'], reverse=True)
	return render_template('index.html', posts=posts)

@app.route('/admin')
def admin_panel():
	all_posts = get_posts()
	posts = all_posts['payload']['results']
	posts = sorted(posts, key=lambda k: k['id'], reverse=True)
	return render_template('admin.html', posts=posts)

@app.route('/add', methods=['POST'])
def add_post():
	title = request.form['title']
	sub_title = request.form['subtitle']
	author = request.form['author']
	text = request.form['text']
	add_blog_post(title, sub_title, author, text)
	flash('New blog entry was succesfully added')
	return redirect(url_for('blog'))

@app.route('/<int:id>')
def show_post(id):
	post = get_post_by_id(id)
	print post
	post = post['payload']['results'][0]
	return render_template('show-post.html', post=post)

@app.route('/update/<int:id>')
def show_update_post(id):
	post = get_post_by_id(id)
	post = post['payload']['results'][0]
	return render_template('show-update.html', post=post)

@app.route('/update/<int:uid>', methods=['POST'])
def update(uid):
	title = request.form['title']
	sub_title = request.form['subtitle']
	author = request.form['author']
	text = request.form['text']
	update_post(uid, title, sub_title, author, text)
	flash('Blog post was successfully updated')
	return redirect(url_for('blog'))

@app.route('/del/<int:id>')
def delete(id):
	delete_post(id)
	return redirect(url_for('blog'))


if __name__ == '__main__':
	app.run()