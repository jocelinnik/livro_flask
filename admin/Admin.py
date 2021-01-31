# -*- coding: utf-8 -*-
from flask_admin import Admin
from flask_admin.menu import MenuLink

from admin.Views import UserView, HomeView, RoleView, CategoryView, ProductView

from model.Role import Role
from model.User import User
from model.Category import Category
from model.Product import Product


def start_views(app, db):
    admin = Admin(app, name="Meu Estoque", template_mode="bootstrap3", index_view=HomeView())

    admin.add_view(RoleView(Role, db.session, "Funções", category="Usuários"))
    admin.add_view(UserView(User, db.session, "Usuários", category="Usuários"))
    admin.add_view(CategoryView(Category, db.session, "Categorias", category="Produtos"))
    admin.add_view(ProductView(Product, db.session, "Produtos", category="Produtos"))

    admin.add_link(MenuLink(name="Logout", url="/logout"))
