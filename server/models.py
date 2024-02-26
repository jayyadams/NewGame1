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

# Stats

def get_stats(self):
        return {
            'max_hp': self.max_hp,
            'vitality': self.vitality,
            'strength': self.strength,
            'dexterity': self.dexterity,
            'speed': self.speed,
            'luck': self.luck
        }

def calculate_stat(base, growth, level):
    return round(base + (base * growth * (level - 1)))

# Leveling up

def level_up(self):
        old_stats = self.get_stats()
        self.level += 1
        self.update_stats_for_level()
        new_stats = self.get_stats()

        return {
            'level': self.level,
            'old_stats': old_stats,
            'new_stats': new_stats
        }

def calculate_required_exp(level):
    return round(100 * (1.2 ** (level - 1)))

# Character 

class Character(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, default=1)
    exp = db.Column(db.Integer, default=0)
    max_hp = db.Column(db.Integer, default=150)
    current_hp = db.Column(db.Integer, default=150)
    strength = db.Column(db.Integer, default=5)
    vitality = db.Column(db.Integer, default=5)
    dexterity = db.Column(db.Integer, default=5)
    speed = db.Column(db.Integer, default=5)
    armor = db.Column(db.Integer, default=0)
    luck = db.Column(db.Integer, default=0)
    dungeon_level = db.Column(db.Integer, default=0)
    highest_dungeon_level = db.Column(db.Integer, default=0)
    location = db.Column(db.String, nullable=False, default='Home')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    has_seen_intro = db.Column(db.Boolean, default=False)
    isInCombat = db.Column(db.Boolean, default=False)

    inventory = db.relationship('CharacterItem', back_populates='character', cascade="delete, delete-orphan")
    quests = db.relationship('CharacterQuest', back_populates='character')
    gold = db.Column(db.Integer, default=69)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_saved = db.Column(db.DateTime, onupdate=datetime.utcnow)

    equipped_necklace_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    equipped_necklace = db.relationship('Item', foreign_keys=[equipped_necklace_id])
    equipped_armor_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    equipped_ring_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    equipped_ring = db.relationship('Item', foreign_keys=[equipped_ring_id])
    equipped_armor = db.relationship('Item', foreign_keys=[equipped_armor_id])
    equipped_melee_weapon_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    equipped_melee_weapon = db.relationship('Item', foreign_keys=[equipped_melee_weapon_id])
    equipped_ranged_weapon_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    equipped_ranged_weapon = db.relationship('Item', foreign_keys=[equipped_ranged_weapon_id])