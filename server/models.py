from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)

    players = db.relationship("Player", back_populates="team", lazy=True)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    def __repr__(self):
        return f"<Team {self.name}, {self.city}>"


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)

    team = db.relationship("Team", back_populates="players")
    performances = db.relationship("Performance", back_populates="player", lazy=True)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    def __repr__(self):
        return f"<Player {self.name}, {self.position}, Team ID: {self.team_id}>"


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)

    home_team = db.relationship("Team", foreign_keys=[home_team_id], backref="home_games")
    away_team = db.relationship("Team", foreign_keys=[away_team_id], backref="away_games")
    performances = db.relationship("Performance", back_populates="game", lazy=True)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    def __repr__(self):
        return f"<Game Date: {self.date}, Home Team ID: {self.home_team_id}, Away Team ID: {self.away_team_id}>"


class Performance(db.Model):
    __tablename__ = "performances"

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    player = db.relationship("Player", back_populates="performances")
    game = db.relationship("Game", back_populates="performances")

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    def __repr__(self):
        return f"<Performance Player ID: {self.player_id}, Game ID: {self.game_id}, Score: {self.score}>"
