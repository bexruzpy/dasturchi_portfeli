# Loyiha haqida
misol uchun: https://dasturchi.projectsplatform.uz/bexruzdeveloper
shu kabi sahifani yaratish uchun hixmat qiladi.
Hozir dasboard va umumiy frontend qilinmagan ammo backen ishga tushgan
backend: https://animus.uz/docs (Swagger Ui)

# Models
users:
    id: int unique index
    username: str unique
    password: str
    fullname: str
    connects: json[list](forigen key connections.id)
    loyihalar: json[list](forigen key projects.id)
    startuplar: json[list](forigen key projects.id)
    asosiy_loyiha: int (forigen key projects.id)
    cariere: str[html]
    solve_to_problems: json[list](forigen key problem_and_answer.id)
    skills: json[list](forigen key skills.id)
    profile_image: bytes[image_file]
    email: str
    phone_number: str
connections:
    id: int unique index
    type: int (connection_types.id)
    name: str
    datas: json
connection_types:
    id: int unique index
    name: str
    datas: json
projects:
    id: int unique index
    name: str
    about_html: str[html]
    files: json[list](forigen key files.id)
    result: bytes[any_file]
skills:
    id: int unique index
    name: str
    type: int (forigen key skill_types.id)
    grade: int
    bio: str
skill_types:
    id: int unique index
    name: str
    be_grade: bool
problem_and_answer:
    problem: str[html]
    answer: str
    language: int (forigen key languages.id)
languages:
    id: int unique index
    name: str
    view_key: str
