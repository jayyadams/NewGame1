from extensions import db, bcrypt
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# Accounts Tables

class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

#Relationships

    characters = db.relationship('Character', backref='user', cascade='all, delete-orphan')

#HASH
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    

# Character Items table

class CharacterItem(db.Model):
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    quantity = db.Column(db.Integer, default=1)

#Relationships

    character = db.relationship('Character', back_populates='inventory')
    item = db.relationship('Item', back_populates='character_items')

#TOC 

    def custom_serialize(self):
        return {
            'id': self.item_id,
            'character_id': self.character_id,
            'quantity': self.quantity,
            'item_name': self.item.name,
            'item_type': self.item.type,
            'item_rarity': self.item.rarity,
            'strength_bonus': self.item.strength_bonus,
            'vitality_bonus': self.item.vitality_bonus,
            'armor_bonus': self.item.armor_bonus,
            'luck_bonus': self.item.luck_bonus,
            'dexterity_bonus': self.item.dexterity_bonus,
            'speed_bonus': self.item.speed_bonus,
            'price': self.item.price
        }

# NPC Items Table 

npc_items = db.Table('npc_items',
    db.Column('npc_id', db.Integer, db.ForeignKey('npc.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
)