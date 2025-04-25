import asyncio
import logging
from crud import add_skill_type, add_language, add_connection_type, add_profession, add_joylashuv

# SQLAlchemy log darajasini pasaytirish
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

# Hard skills (baholanadigan ko'nikmalar)
hard_skills = list(set([
    "Python Basic", "FastAPI", "Django", "Flask", "SQL", "NoSQL", "REST",
    "GraphQL", "Microservices", "Docker", "Kubernetes", "CI/CD", "Git", "C++",
    "C#", "Java", "JavaScript", "HTML", "CSS", "React", "Vue", "Angular",
    "Node.js", "Express.js", "Nest.js", "MongoDB", "PostgreSQL", "MySQL",
    "Redis", "Elasticsearch", "Kafka", "RabbitMQ", ".NET", "Flutter",
    "Android Studio", "iOS", "Swift", "Objective-C", "Xamarin", "Unity",
    "Unreal Engine", "Blender", "Maya", "Houdini", "Nuke", "After Effects"
]))

# Soft skills (baholanmaydigan ko'nikmalar)
soft_skills = list(set([
    "Communication", "Leadership", "Teamwork", "Problem-solving",
    "Critical thinking", "Analytical thinking", "Attention to detail",
    "Time management", "Fast learning", "Clearing code", "SOLID",
    "OOP", "DRY", "KISS"
]))

# Barcha skill'larni qo‘shish funksiyasi
async def add_all_skill_types():
    total_added = 0
    for name in hard_skills:
        try:
            await add_skill_type(skill_name=name, be_grade=True)
            print(f"✅ Added (graded): {name}")
            total_added += 1
        except Exception as e:
            print(f"⚠️  Skipped (graded): {name} ({str(e)})")

    for name in soft_skills:
        try:
            await add_skill_type(skill_name=name, be_grade=False)
            print(f"✅ Added (non-graded): {name}")
            total_added += 1
        except Exception as e:
            print(f"⚠️  Skipped (non-graded): {name} ({str(e)})")

    print(f"\n🔚 Yangi qo‘shilgan skill_types soni: {total_added}")

# Barcha languages larni kiritish
Languages = [
    "Python", "Java", "C++", "C#", "JavaScript", "C",
    "PHP", "Ruby", "Swift", "Kotlin", "Go", "Rust",
    "TypeScript", "Scala", "R", "Perl", "Haskell",
    "Dart"
]
async def add_all_languages():
    total_added = 0
    for name in Languages:
        try:
            await add_language(language_name=name)
            print(f"✅ Added: {name}")
            total_added += 1
        except Exception as e:
            print(f"⚠️  Skipped: {name} ({str(e)})")

    print(f"\n🔚 Yangi qo‘shilgan languages soni: {total_added}")


# Barcha connection type nomlari
connection_types = [
    "GitHub",
    "Telegram",
    "LinkedIn",
    "Facebook",
    "Instagram",
    "Twitter",
    "YouTube",
    "Upwork",
    "Fiverr"
]
def load_icon_bytes(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()

async def add_all_connection_types():
    total_added = 0
    for name in set(connection_types):
        try:
            result = await add_connection_type(
                name=name,
                datas={"username": "str"},
                icon=load_icon_bytes(f"icons/{name}.png")
            )
            if isinstance(result, dict) and "already exists" in result.get("detail", ""):
                print(f"⚠️ Skipped: {name} (already exists)")
            else:
                print(f"✅ Added: {name}")
                total_added += 1
        except Exception as e:
            print(f"❌ Error: {name} ({str(e)})")

    print(f"\n🔚 Jami qo‘shilgan connection_types soni: {total_added}")
# URL formatlari har bir platforma uchun
url_formats = {
    "GitHub": "https://github.com/{username}",
    "Telegram": "https://t.me/{username}",
    "LinkedIn": "https://linkedin.com/in/{username}",
    "Facebook": "https://facebook.com/{username}",
    "Instagram": "https://instagram.com/{username}",
    "Twitter": "https://twitter.com/{username}",
    "YouTube": "https://youtube.com/@{username}",
    "Upwork": "https://www.upwork.com/freelancers/~{username}",
    "Fiverr": "https://www.fiverr.com/{username}",
}

# Asinxron update funksiyasi
async def update_all_url_formats():
    total_updated = 0
    for name, url_format in url_formats.items():
        try:
            result = await update_connection_type_url(name=name, url_format=url_format)
            if result is True:
                print(f"✅ Updated: {name}")
                total_updated += 1
            else:
                print(f"⚠️ Skipped or not found: {name}")
        except Exception as e:
            print(f"❌ Error updating {name}: {str(e)}")

    print(f"\n🔚 Jami yangilangan connection_types soni: {total_updated}")

jobs = [
    "Backend Developer",
    "Frontend Developer",
    "Fullstack Developer",
    "Mobile Developer",
    "UI/UX Designer",
    "Product Designer",
    "Web Developer",
    "Software Engineer",
    "Data Analyst",
    "Data Scientist",
    "Machine Learning Engineer",
    "AI Engineer",
    "DevOps Engineer",
    "Site Reliability Engineer",
    "Cybersecurity Analyst",
    "Penetration Tester",
    "Security Engineer",
    "Cloud Engineer",
    "Cloud Architect",
    "Database Administrator",
    "Big Data Engineer",
    "System Administrator",
    "Network Engineer",
    "QA Engineer",
    "Test Automation Engineer",
    "Game Developer",
    "VR/AR Developer",
    "Embedded Systems Engineer",
    "IoT Developer",
    "Blockchain Developer",
    "Smart Contract Developer",
    "Technical Writer",
    "IT Support Specialist",
    "Technical Support Engineer",
    "IT Project Manager",
    "Product Manager",
    "Scrum Master",
    "Agile Coach",
    "Business Analyst",
    "Solutions Architect",
    "IT Consultant",
    "Machine Learning Researcher",
    "Natural Language Processing Engineer",
    "Computer Vision Engineer",
    "Bioinformatics Developer",
    "Robotics Engineer",
    "Ethical Hacker",
    "Frontend Architect",
    "Backend Architect",
    "Software Architect",
]

async def add_all_jobs():
    total_added = 0
    for name in set(jobs):
        try:
            await add_profession(name=name)
            print(f"✅ Added: {name}")
            total_added += 1
        except Exception as e:
            print(f"⚠️  Skipped: {name} ({str(e)})")

joylashuvlar = [
    "Toshkent",
    "Samarqand",
    "Andijon",
    "Buxoro",
    "Jizzax",
    "Farg'ona",
    "Namangan",
    "Navoiy",
    "Qashqadaryo",
    "Qoraqalpoqiston",
    "Sirdaryo",
    "Surxondaryo",
    "Toshkent viloyati",
]

async def add_all_joylashuvlar():
    total_added = 0
    for name in set(joylashuvlar):
        try:
            await add_joylashuv(name=name)
            print(f"✅ Added: {name}")
            total_added += 1
        except Exception as e:
            print(f"⚠️  Skipped: {name} ({str(e)})")

    print(f"\n🔚 Yangi qo‘shilgan joylashuvlar soni: {total_added}")


# Ishga tushurish
if __name__ == "__main__":
    # asyncio.run(add_all_skill_types())
    # asyncio.run(add_all_languages())
    # asyncio.run(add_all_connection_types())
    # asyncio.run(add_all_jobs())
    asyncio.run(add_all_joylashuvlar())

