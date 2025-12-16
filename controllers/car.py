from flask import Blueprint, render_template
# from models.item_carrinho import ItemCarrinho

carrinho_bp = Blueprint("carrinho", __name__)

@carrinho_bp.route("/carrinho")
def ver_carrinho():
    itens = ItemCarrinho.query.all()

    total = sum(
        item.quantidade * item.preco_unitario
        for item in itens
    )

    return render_template(
        "carrinho.html",
        itens=itens,
        total=total
    )
