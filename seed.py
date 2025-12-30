import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.manufacturer import Manufacturer
from app.models.product import Product
from app.models.customer import Customer
from app.models.sale import Sale, SaleItem


def seed_db():
    db = SessionLocal()
    try:
        print("🚀 Iniciando carga massiva de dados com correções...")

        # 1. Criar 10 Fabricantes (Corrigindo o e-mail que estava null)
        manufacturers = []
        for i in range(1, 11):
            nome_fabrica = f"Fábrica de Móveis {i:02d} S.A."
            # Geramos um e-mail válido para evitar o erro de campo nulo
            m = Manufacturer(
                name=nome_fabrica,
                contact_email=f"contato@fabricamoveis{i}.com.br"
            )
            db.add(m)
            manufacturers.append(m)
        db.flush()
        print(f"✅ {len(manufacturers)} Fabricantes criados com e-mails.")

        # 2. Criar 10 Produtos para cada Fábrica (Total 100)
        products = []
        categories = ["Cadeira", "Mesa", "Armário", "Sofá", "Estante", "Cama", "Poltrona", "Escrivaninha",
                      "Criado-mudo", "Painel TV"]

        for m in manufacturers:
            for i in range(1, 11):
                # Sorteamos a categoria UMA VEZ para usar no nome e na coluna category
                categoria_sorteada = random.choice(categories)

                p = Product(
                    name=f"{categoria_sorteada} Mod. {m.id}{i}",
                    category=categoria_sorteada,  # <--- Alimentação explícita da categoria para o BI
                    price=round(random.uniform(150.0, 4500.0), 2),
                    stock_quantity=random.randint(20, 100),
                    manufacturer_id=m.id
                )
                db.add(p)
                products.append(p)
        db.flush()
        print(f"✅ {len(products)} Produtos criados com categorias atribuídas.")

        # 3. Criar 30 Clientes
        customers = []
        names = ["Gabriel", "Lucas", "Mariana", "Juliana", "Rafael", "Beatriz", "Ricardo", "Fernanda", "Thiago",
                 "Camila"]
        surnames = ["Silva", "Santos", "Oliveira", "Souza", "Pereira", "Costa", "Rodrigues", "Almeida", "Nascimento",
                    "Lopes"]

        for i in range(1, 31):
            nome_completo = f"{random.choice(names)} {random.choice(surnames)} {i}"
            c = Customer(
                name=nome_completo,
                email=f"cliente{i}@provedor.com.br",
                document=f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"
            )
            db.add(c)
            customers.append(c)
        db.flush()
        print(f"✅ {len(customers)} Clientes criados.")

        # 4. Criar 200 Vendas (Distribuídas nos últimos 60 dias)
        print("🛒 Gerando 200 vendas com histórico para o BI...")
        for i in range(200):
            cliente = random.choice(customers)
            # Cada venda terá entre 1 e 4 itens diferentes
            num_itens = random.randint(1, 4)
            venda_produtos = random.sample(products, num_itens)

            # Data aleatória nos últimos 60 dias para o BI ter gráfico de linha funcional
            dias_atras = random.randint(0, 60)
            data_venda = datetime.utcnow() - timedelta(days=dias_atras, hours=random.randint(0, 23))

            venda = Sale(
                customer_id=cliente.id,
                sale_date=data_venda,
                total_price=0.0
            )
            db.add(venda)
            db.flush()

            valor_total_venda = 0
            for prod in venda_produtos:
                qtd = random.randint(1, 3)
                valor_unitario = prod.price
                valor_item = valor_unitario * qtd
                valor_total_venda += valor_item

                item = SaleItem(
                    sale_id=venda.id,
                    product_id=prod.id,
                    quantity=qtd,
                    unit_price=valor_unitario  # Garante que o histórico de preço da venda seja salvo
                )
                db.add(item)

                # Baixa o estoque no seed para testar o alerta de stock baixo
                prod.stock_quantity -= qtd

            venda.total_price = valor_total_venda

        db.commit()
        print(f"🔥 SUCESSO! O banco de dados está pronto para o Dashboard.")

    except Exception as e:
        print(f"❌ ERRO DURANTE O SEED: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_db()