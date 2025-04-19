from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON, LargeBinary, Boolean
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
    skill_type = relationship("SkillType")
    user = relationship("User", foreign_keys=[user_id])


class ConnectionType(Base):
    __tablename__ = "connection_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    datas = Column(JSON)
    icon = Column(LargeBinary)


class Connection(Base):
    __tablename__ = "connections"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Integer, ForeignKey("connection_types.id"))
    name = Column(String)
    datas = Column(JSON)
    connection_type = relationship("ConnectionType")


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


class ProblemAndAnswer(Base):
    __tablename__ = "problem_and_answer"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    problem = Column(Text)
    answer = Column(Text)
    language = Column(Integer, ForeignKey("languages.id"))
    language_ref = relationship("Language")
    owner = relationship("User", foreign_keys=[user_id])


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    fullname = Column(String)
    connects = Column(JSON)  # IDs of connections
    loyihalar = Column(JSON)  # IDs of projects
    startuplar = Column(JSON)  # IDs of startup-type projects
    asosiy_loyiha = Column(Integer, ForeignKey("projects.id"))
    cariere = Column(Text)  # HTML content
    solve_to_problems = Column(JSON)  # IDs of problem_and_answer
    skills = Column(JSON)  # IDs of skills
    profile_image = Column(LargeBinary)
    email = Column(String)
    phone_number = Column(String)

    asosiy_loyiha_ref = relationship("Project", foreign_keys=[asosiy_loyiha])
