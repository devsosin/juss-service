from __future__ import annotations

from sqlalchemy import (
    Table, Column, ForeignKey, 
    SmallInteger, Integer, Boolean, BigInteger,
    String, DateTime
    )
from sqlalchemy.orm import relationship, backref

from sqlalchemy.sql import func

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
    """
    유저 정보
    """
    __tablename__ = "tb_user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    accounts = relationship("Account", back_populates="user")

class Account(Base):
    """
    계좌정보
    """
    __tablename__ = "tb_account"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    account_type = Column(SmallInteger, nullable=False) # 계좌 종류 (입출금계좌, 적금, 연락처)
    bank_name = Column(String(16), nullable=False)
    account_name = Column(String(16), nullable=True)
    account_number = Column(String(32), nullable=True)
    balance = Column(BigInteger, nullable=False)


    user_id = Column(Integer, ForeignKey("tb_user.id", name="fk_user_account"))
    user = relationship("User", foreign_keys=[user_id], back_populates='accounts', uselist=False, 
                        primaryjoin='User.id==Account.user_id')
    
    is_show = Column(Boolean, nullable=False, default=True)
    is_favorite = Column(Boolean, nullable=False, default=False)
    
    card_id = Column(Integer, ForeignKey("tb_card.id", name="fk_card_account"), nullable=True)
    card = relationship("Card", foreign_keys=[card_id], uselist=False, 
                        primaryjoin='Card.id==Account.card_id')

    def to_dict(self):
        return {
            'id': self.id,
            'account_type': self.account_type,
            'card_id': self.card_id,
            'bank_name': self.bank_name,
            'account_name': self.account_name,
            'account_number': self.account_number,
            'balance': self.balance,
            'is_show': self.is_show,
            'account_type': self.account_type
        }

class Card(Base):
    """
    카드정보
    """
    __tablename__ = "tb_card"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_name = Column(String(32), nullable=False)
    min_usage = Column(Integer, nullable=False)

    account_id = Column(Integer, ForeignKey("tb_account.id", name="fk_account_card"), nullable=True)
    account = relationship("Account", foreign_keys=[account_id], uselist=False, 
                        primaryjoin='Card.account_id==Account.id')
    
    is_credit = Column(Boolean, nullable=False, default=False) # True : 신용 / False : 체크

    transactions = relationship("Transaction", back_populates="card")

class Transaction(Base):
    """
    거래정보
    """
    __tablename__ = "tb_transaction"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    amount = Column(Integer, nullable=False) # 계좌 종류 (입출금계좌, 적금, 연락처)
    memo = Column(String(128), nullable=False)
    is_fill = Column(Boolean, nullable=False, default=False) # 채우기 / 보내기

    receiver_id = Column(Integer, ForeignKey("tb_account.id", name="fk_account_recv_tr"), nullable=False)
    # , back_populates='recv_trs'
    receiver = relationship("Account", foreign_keys=[receiver_id], backref=backref("recv_trs", remote_side=receiver_id, lazy="dynamic"),
                        primaryjoin='Transaction.receiver_id==Account.id')
    sender_id = Column(Integer, ForeignKey("tb_account.id", name="fk_account_send_tr"), nullable=False)
    # , back_populates='send_trs'
    sender = relationship("Account", foreign_keys=[sender_id], backref=backref("send_trs", remote_side=sender_id, lazy="dynamic"), 
                        primaryjoin='Transaction.sender_id==Account.id')
    
    card_id = Column(Integer, ForeignKey("tb_card.id", name="fk_tr_card"), nullable=True)
    card = relationship("Card", foreign_keys=[card_id], back_populates='transactions', uselist=False, 
                        primaryjoin='Transaction.card_id==Card.id') 
        
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
