from faker import Faker
from app import db  # Assuming your SQLAlchemy instance is named db
from app.models import Student  # Import your Student model


def generate_dummy_students(num_students=50):
    fake = Faker()
    students = []
    for _ in range(num_students):
        user_id = fake.uuid4()[:8]  # Generate a short UUID
        first_name = fake.first_name()
        last_name = fake.last_name()
        date_of_birth = fake.date_of_birth(
            minimum_age=18, maximum_age=25)  # Between 18 and 25 years old
        gender = fake.random_element(elements=('Male', 'Female'))
        address = fake.address()
        student_index_number = fake.unique.random_number(
            digits=8, fix_len=True)

        student = Student(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            student_index_number=student_index_number
        )
        students.append(student)

    # Bulk save to the database
    db.session.bulk_save_objects(students)
    db.session.commit()


if __name__ == "__main__":
    from app import app
    with app.app_context():
        generate_dummy_students(50)
