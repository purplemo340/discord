#Import Libraries
from __future__ import annotations
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Text, Boolean, ForeignKey
from typing import List
from flask_wtf import FlaskForm
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from functools import wraps
from wtforms import StringField, SubmitField, EmailField, PasswordField, DateTimeField
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor
from flask_ckeditor import CKEditorField
from datetime import datetime
import os
import psycopg2


import sys

# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('Flask_Key')
#Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


def admin_only(f):
    @wraps(f)
    def admin(*args, **kwargs):
        print("a")
        if not current_user.is_authenticated or current_user.name != 'admin':
            return abort(403)
        return f(*args, **kwargs)
    return admin


class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)

data = os.getenv('Database_URL')
app.config["SQLALCHEMY_DATABASE_URI"] = data

db.init_app(app)



class LoginForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired()])
    password=PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LogForm(FlaskForm):
    log = CKEditorField("Book Log", validators=[DataRequired()])
    submit = SubmitField("Log")


class BookForm(FlaskForm):
    name = StringField("Book Name", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    rating = StringField("Rating", validators=[DataRequired()])
    status = StringField("Finished?", validators=[DataRequired()])
    submit = SubmitField("Add Book")
class CommentForm(FlaskForm):
    #name = StringField("Book Name", validators=[DataRequired()])
    #author = StringField("Author", validators=[DataRequired()])
    comment = CKEditorField("Thoughts?", validators=[DataRequired()])
    submit = SubmitField("Add Comment")
class PageForm(FlaskForm):
    pages= StringField('Pages Read')
    submit = SubmitField("Add")
class Books(db.Model):
    __tablename__ = "bookshelves"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    complete: Mapped[str] = mapped_column(String(250), nullable=False)
    isbn: Mapped[str] = mapped_column(String(250), nullable=False)
    #book to logs
    logs: Mapped[List["Logs"]] = relationship(back_populates="book")
    #user to books
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("readers.id"))
    #user_name: Mapped[str] = mapped_column(String, db.ForeignKey("readers.name"))

    reader = relationship("User", back_populates="books")
    #readers: Mapped[List["User"]] = relationship(back_populates="readers")
    #user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("readers.id"))

    comments: Mapped[List["Comments"]] = relationship(back_populates="book")
class User(UserMixin, db.Model):
    __tablename__ = "readers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    #user to logs
    logs: Mapped[List["Logs"]] = relationship(back_populates="reader")
    #book to logs
    books: Mapped[List["Books"]] = relationship(back_populates="reader")

    comments:  Mapped[List["Comments"]] = relationship(back_populates="reader")



class Logs(db.Model):
    __tablename__ = "book_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    log: Mapped[str] = mapped_column(Text, nullable=False)
    date_created: Mapped[str] = mapped_column(String(250), nullable=False)
    #book to logs
    book_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("bookshelves.id"))
    book = relationship("Books", back_populates="logs")
    # user to logs
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("readers.id"))
    reader = relationship("User", back_populates="logs")

class Comments(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    date_created: Mapped[int] = mapped_column(String(250), nullable=False)
    username: Mapped[int] = mapped_column(String, db.ForeignKey("readers.name"))
    reader = relationship("User", back_populates="comments")

    book_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("bookshelves.id"))
    book = relationship("Books", back_populates="comments")

#     title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
#     author: Mapped[str] = mapped_column(String(250), nullable=False)
#     comment: Mapped[str] = mapped_column(String(250), nullable=False)
#     books: Mapped[List["Logs"]] = relationship(back_populates="book_log")
#     reader: Mapped[List["User"]] = relationship(back_populates="readers")


class Pages(db.Model):
    __tablename__ = "Pages_2025"
    Jan: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    Feb: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    Mar: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    Apr: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    May: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    Jun: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    Jul: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    Aug: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    Sep: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    Oct: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    Nov: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    Dec: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    id: Mapped[int] = mapped_column(primary_key=True)
with app.app_context():
    db.create_all()
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents=discord.Intents.default()

intents.message_content = True
#client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

""" @client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
###########################################

@client.event
async def on_message(message):
    
    print(message.content)
    if message.author == client.user:
        return
    if message.content=='pages!':
        response = 'How many pages have you read today?'
        await message.channel.send(response)
        def check(m):
            if m.content.isnumeric():
                with app.app_context():
                    day=int(datetime.now().strftime('%d'))
                    month_num=(datetime.now().strftime('%m'))
                    value_update = db.session.execute(db.select(Pages).where(Pages.id == day)).scalar()
                    update =[value_update.Jan, value_update.Feb, value_update.Mar, value_update.Apr, value_update.May,
                    value_update.Jun, value_update.Jul, value_update.Aug, value_update.Sep, value_update.Oct,
                    value_update.Nov, value_update.Dec]
                    update[month_num-1]=int(m.content)
                    db.session.commit()
            return m.channel==message.channel
        msg=await client.wait_for('message', check=check)
        response = 'Good job! Keep it up!'
        await message.channel.send(response)
        
    
        
            
    elif message.content=='show!':
        with app.app_context():
            result = db.session.execute(db.select(Books.title).order_by(Books.title).where(Books.user_id==2))
            all_books = result.scalars()
            hi=""
            for book in all_books:
                id = db.session.execute(db.select(Books.id).where(Books.user_id==2, Books.title==book))
                id=id.scalar()
                hi=hi + str(id) + ": "+book+ '\n'
                
            response=hi
            await message.channel.send(response)
        
    elif message.content.startswith('log:'):
            book=message.content[4:]
            if book.isnumeric():
                with app.app_context():
                    result = db.session.execute(db.select(Books.title).order_by(Books.title).where(Books.user_id==2, Books.id==book))
                    response="Do you want to create a log for this book?: "+result.scalar()
                    await message.channel.send(response)
                   
                    def check(m):
                        
                        new_log = Logs(log=m[4:],
                        book=book,
                        date_created=datetime.now().strftime('%b. %d, %Y  %I:%M:%S%p'),
                        id=db.session.query(Logs.id).count() + 1,
                        user_id=2)
                        db.session.add(new_log)
                        db.session.commit()
                        return m.channel==message.channel
                    msg=await client.wait_for('message', check=check)
                    await message.channel.send(msg[4:]) #Send log
    elif message.content=="log: yes":
        response="Start log with log message:"
        await message.channel.send(response)
#event to show the codes to use for information:
@client.event
async def on_ready():
    mes="System Reboot(aka Power Outage)"
    "Moshimoshi, What do you want to do? \n"
    "show_books!: see the books that were read.\n"
    "make_log!: Log for a specific book\n"
    "show_pages!: show the pages read for the month\n"
    "show_log!: Show the logs for a specified book\n"
    "add_book!: Add book to database\n"
    "add_pages!: Add what was read today\n"
     """
@bot.event
async def on_ready():
    mes="System Reboot(aka Power Outage)\
    \n Moshimoshi, What do you want to do? \n \
    show_books!: see the books that were read.\n\
    make_log!: Log for a specific book\n\
    show_pages!: show the pages read for the month\n\
    show_log!: Show the logs for a specified book\n\
    add_book!: Add book to database\n\
    add_pages!: Add what was read today\n"
    await bot.get_channel(1333564862835589205).send(mes)
    print(f'{bot.user.name} has connected to Discord!')
@bot.command(name='add_pages')
async def show_pages(ctx):
    response = 'How many pages have you read today?'
    await ctx.send(response)
    def check(m):
        if m.content.isnumeric():
            with app.app_context():
                day=int(datetime.now().strftime('%d'))
                month_num=int(datetime.now().strftime('%m'))
                value_update = db.session.execute(db.select(Pages).where(Pages.id == day)).scalar()
                update =[value_update.Jan, value_update.Feb, value_update.Mar, value_update.Apr, value_update.May,
                value_update.Jun, value_update.Jul, value_update.Aug, value_update.Sep, value_update.Oct,
                value_update.Nov, value_update.Dec]
                value_update.Feb =int(m.content)
                print(update[month_num-1])
                print(day)
                db.session.commit()
            response = 'Good job! Keep it up!'
            return m.channel==ctx.channel
    
    msg=await bot.wait_for('message', check=check)
    
    await ctx.send(response)
    
@bot.command(name='show_books')
async def show_books(ctx):
    with app.app_context():
        result = db.session.execute(db.select(Pages.Feb).order_by(Pages.id))
        all_books = result.scalars()
        hi=""
        for book in all_books:
            hi=hi +": "+str(book)+ '\n'
        response=hi
        await ctx.channel.send(response)

#client.run(TOKEN)
bot.run(TOKEN)
###############################################