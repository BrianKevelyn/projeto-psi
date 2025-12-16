from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.itemcarrinho import ItemCarrinho
from database.connection import db

carrinho_bp = Blueprint("carrinho", __name__)

@carrinho_bp.route("/carrinho")
@login_required
def ver_carrinho():
    itens = ItemCarrinho.query.filter_by(
        usuario_id=current_user.id
    ).all()

    total = sum(
        item.quantidade * item.preco_unitario
        for item in itens
    )

    return render_template(
        "carrinho.html",
        itens=itens,
        total=total
    )

@carrinho_bp.route("/carrinho/aumentar/<int:item_id>")
@login_required
def aumentar(item_id):
    item = ItemCarrinho.query.filter_by(
        id=item_id,
        usuario_id=current_user.usu_id
    ).first_or_404()

    item.quantidade += 1
    db.session.commit()

    return redirect(url_for("carrinho.ver_carrinho"))

@carrinho_bp.route("/carrinho/diminuir/<int:item_id>")
@login_required
def diminuir(item_id):
    item = ItemCarrinho.query.filter_by(
        id=item_id,
        usuario_id=current_user.usu_id
    ).first_or_404()

    if item.quantidade > 1:
        item.quantidade -= 1
        db.session.commit()
    else:
        db.session.delete(item)
        db.session.commit()

    return redirect(url_for("carrinho.ver_carrinho"))

@carrinho_bp.route("/carrinho/remover/<int:item_id>")
@login_required
def remover(item_id):
    item = ItemCarrinho.query.filter_by(
        id=item_id,
        usuario_id=current_user.usu_id
    ).first_or_404()

    db.session.delete(item)
    db.session.commit()

    flash("Item removido do carrinho.", "success")
    return redirect(url_for("carrinho.ver_carrinho"))

