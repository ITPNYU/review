from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import func
from review.database import Base

# ORM classes
class Collection(Base):
    __tablename__ = 'collection'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False, unique=True)
    entries = relationship('Entry', backref='collection')
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return '<Collection %r>' % (self.id)

class Entry(Base):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    external_id = Column(String(50), nullable=False)
    collection_id = Column(ForeignKey('collection.id'), nullable=False)
    code = Column(String(50), nullable=False, unique=True, default=func.uuid())
    response = Column(Enum('accept', 'decline'), nullable=True)
    invoice = Column(String(50), nullable=True)
    reviews = relationship('Review', backref='entry')
    decision = relationship('Decision', uselist=False, backref='entry')
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(DateTime, nullable=False, default=func.now())
    UniqueConstraint('external_id', 'collection_id')

    def __repr__(self):
        return '<Entry %r>' % (self.id)

class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True, nullable=False)
    recommendation = Column(Enum('yes', 'no', 'maybe'), nullable=False)
    reviewer = Column(String(30), nullable=False)
    entry_id = Column(Integer, ForeignKey('entry.id'), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return '<Review %r>' % (self.id)

class Decision(Base):
    __tablename__ = 'decision'
    id = Column(Integer, primary_key=True, nullable=False)
    decision = Column(Enum('accept', 'reject', 'comp'), nullable=False)
    reviewer = Column(String(30), nullable=False)
    entry_id = Column(Integer, ForeignKey('entry.id'), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return '<Decision %r>' % (self.id)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    netid = Column(String(25), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    modified_at = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return '<User %r>' % (self.netid)
