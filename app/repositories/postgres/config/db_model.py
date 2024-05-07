from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DATE, Table, DateTime, Numeric, BOOLEAN
from sqlalchemy.orm import relationship
from repositories.postgres.config import db_config


Account = Table(
    "account",
    db_config.metadata,
    Column('id',Integer, primary_key=True, index=True),
    Column('username',String(20), unique=True, index=True, nullable=False),
    Column('hashed_password',String(255), index=True, nullable=False),
    Column('nama',String(255), index=True, nullable=False),
    Column('email',String(255), index=True, nullable=False, unique=True),
    Column('role',String(30), index=True, nullable=False),
    Column('credit', Numeric(precision=10, scale=2), index=True, nullable=False),
    Column('created_at' ,DateTime, index=True, nullable=False),
    Column('updated_at' ,DateTime, index=True),
    Column('is_deleted', BOOLEAN)
)

Transaksi = Table(
    'transaksi',
    db_config.metadata, 
    Column('id',Integer, primary_key=True, index=True),
    Column('kategori' ,String(255), index=True),
    Column('ml_model' ,String(255), index=True),
    Column('created_at', DateTime, index=True, nullable=False),
    Column('updated_at', DateTime, index=True),
    Column('price', Numeric(precision=10, scale=2), index=True, nullable=False),
    Column('total_hit', Numeric(precision=10, scale=2), index=True, nullable=False),
    Column('id_account',Integer, ForeignKey("account.id"), index=True, nullable=False)
)
