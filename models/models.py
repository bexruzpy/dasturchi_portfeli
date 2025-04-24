from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON, LargeBinary, Boolean, DATE, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Language(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    view_key = Column(String)


class SkillType(Base):
    __tablename__ = "skill_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    be_grade = Column(Boolean)


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(Integer, ForeignKey("skill_types.id"))
    grade = Column(Integer)
    bio = Column(String)
    skill_type = relationship("SkillType", foreign_keys=[type])
    user = relationship("User", foreign_keys=[user_id])
    def get_public_json(self):
        degrees = {
            1: "Fundamental",
            2: "Intermediate",
            3: "Advanced",
            4: "Expert"
        }
        if self.skill_type.be_grade:
            return {
                "begrade": self.skill_type.be_grade,
                "name": self.skill_type.name,
                "bio": degrees[self.grade]
            }
        return {
            "begrade": self.skill_type.be_grade,
            "name": self.skill_type.name,
            "bio": self.bio
        }


class ConnectionType(Base):
    __tablename__ = "connection_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    datas = Column(JSON)
    url_format = Column(String)
    icon = Column(LargeBinary)


class Connection(Base):
    __tablename__ = "connections"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Integer, ForeignKey("connection_types.id"))
    datas = Column(JSON)
    connection_type = relationship("ConnectionType")
    def get_public_json(self):
        res = self.connection_type.url_format
        for key in self.datas:
            res = res.replace("{"+key+"}", self.datas[key])
        return {
            "type_id": self.connection_type.id,
            "datas": self.datas,
            "url": res,
            "name": self.connection_type.name
        }


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    about_text = Column(Text)
    about_html = Column(Text)
    files = Column(JSON)
    result = Column(LargeBinary)

    user = relationship("User", foreign_keys=[user_id])
    def get_public_json(self, be_startup):
        return {
            "id": self.id,
            "name": self.name,
            "about_text": self.about_text,
            "be_startup": be_startup
        }

class ProblemAndAnswer(Base):
    __tablename__ = "problem_and_answer"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(Text)
    problem = Column(Text) # Html
    answer = Column(Text) # Code text
    language = Column(Integer, ForeignKey("languages.id"))
    language_ref = relationship("Language")
    owner = relationship("User", foreign_keys=[user_id])
    def get_public_json(self):
        return {
            "id": self.id,
            "name": self.name
        }
    def get_code_json(self):
        return {
            "code_text": self.answer,
            "language_name": self.language_ref.name,
            "key_code": self.language_ref.view_key
        }

class Joylashuv(Base):
    __tablename__ = "joylashuvlar"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True)


class Profession(Base):
    __tablename__ = "professions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    fullname = Column(String)
    connections_list = Column(JSON)  # IDs of connections
    loyihalar = Column(JSON)  # IDs of projects
    startuplar = Column(JSON)  # IDs of startup-type projects
    asosiy_loyiha = Column(String) # Loyiha nomi yoki sayt linki misol projectsplatform.uz
    cariere = Column(Text)  # HTML content
    solve_to_problems = Column(JSON)  # IDs of problem_and_answer
    skills = Column(JSON)  # IDs of skills
    profile_image = Column(LargeBinary)
    email = Column(String, unique=True)
    phone_number = Column(String)
    position = Column(Integer, ForeignKey("joylashuvlar.id"))
    profession = Column(Integer, ForeignKey("professions.id"))
    experience = Column(String)
    birth_day = Column(DateTime(timezone=False))
    hozirgi_faoliyat = Column(String) # Ayni payda shug'ullanayotgan ish faoliyati

    joylashuv = relationship("Joylashuv", foreign_keys=[position])
    kasb = relationship("Profession", foreign_keys=[profession])

