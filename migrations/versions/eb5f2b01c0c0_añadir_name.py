"""Añadir name

Revision ID: eb5f2b01c0c0
Revises: 682b76ecfa44
Create Date: 2025-03-20 17:07:20.173613

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = 'eb5f2b01c0c0'
down_revision = '682b76ecfa44'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # Agregar la columna `name` permitiendo valores NULL temporalmente
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('name', sa.String(length=100), nullable=True))

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('name', sa.String(length=100), nullable=True))

    with op.batch_alter_table('vehicles', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('name', sa.String(length=100), nullable=True))

    # Asignar valores únicos en `characters`
    result = conn.execute(text("SELECT id FROM characters WHERE name IS NULL"))
    for i, row in enumerate(result.fetchall(), start=1):
        conn.execute(text(
            f"UPDATE characters SET name = 'Unknown_{i}' WHERE id = :id"), {'id': row[0]})

    # Asignar valores únicos en `planets`
    result = conn.execute(text("SELECT id FROM planets WHERE name IS NULL"))
    for i, row in enumerate(result.fetchall(), start=1):
        conn.execute(text(f"UPDATE planets SET name = 'Unknown_{i}' WHERE id = :id"), {
                     'id': row[0]})

    # Asignar valores únicos en `vehicles`
    result = conn.execute(text("SELECT id FROM vehicles WHERE name IS NULL"))
    for i, row in enumerate(result.fetchall(), start=1):
        conn.execute(text(f"UPDATE vehicles SET name = 'Unknown_{i}' WHERE id = :id"), {
                     'id': row[0]})

    # Convertir la columna `name` en NOT NULL y agregar UNIQUE constraint
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.alter_column('name', nullable=False)
        batch_op.create_unique_constraint('uq_characters_name', ['name'])

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.alter_column('name', nullable=False)
        batch_op.create_unique_constraint('uq_planets_name', ['name'])

    with op.batch_alter_table('vehicles', schema=None) as batch_op:
        batch_op.alter_column('name', nullable=False)
        batch_op.create_unique_constraint('uq_vehicles_name', ['name'])


def downgrade():
    with op.batch_alter_table('vehicles', schema=None) as batch_op:
        batch_op.drop_constraint('uq_vehicles_name', type_='unique')
        batch_op.drop_column('name')

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.drop_constraint('uq_planets_name', type_='unique')
        batch_op.drop_column('name')

    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.drop_constraint('uq_characters_name', type_='unique')
        batch_op.drop_column('name')
