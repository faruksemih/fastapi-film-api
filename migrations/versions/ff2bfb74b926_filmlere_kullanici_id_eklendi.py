"""filmlere kullanici id eklendi

Revision ID: ff2bfb74b926
Revises: e4fbbe27d02b
Create Date: 2026-08-21 10:32:49.287721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff2bfb74b926'
down_revision: Union[str, Sequence[str], None] = 'e4fbbe27d02b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("filmler") as batch_op:
        batch_op.add_column(
            sa.Column("kullanici_id", sa.Integer(), nullable=True)
        )

        batch_op.create_foreign_key(
            "fk_filmler_kullanici_id_kullanicilar",
            "kullanicilar",
            ["kullanici_id"],
            ["id"]
        )

def downgrade() -> None:
    with op.batch_alter_table("filmler") as batch_op:
        batch_op.drop_constraint(
            "fk_filmler_kullanici_id_kullanicilar",
            type_="foreignkey"
        )

        batch_op.drop_column("kullanici_id")