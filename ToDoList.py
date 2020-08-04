from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def get_input():
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    inp = int(input())

    return inp


action = get_input()
while action in (1, 2, 3, 4, 5, 6):
    if action == 1:
        print("Today:")

        today = datetime.today()
        tasks = session.query(Task).filter(Task.deadline == today.date()).all()

        print("Today {} {}:".format(today.day, today.strftime('%b')))

        if len(tasks) == 0:
            print("Nothing to do!\n")
        else:
            i = 1
            while i <= len(tasks):
                print("{}. {}".format(i, tasks[i - 1].task))
                i += 1

            print("")
    elif action == 2:
        weekdays = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

        begin_date = datetime.today()
        end_date = begin_date + timedelta(days=7)
        tasks = session.query(Task).filter(Task.deadline >= begin_date.date(), Task.deadline <= end_date.date()).order_by(Task.deadline).all()

        current_date = datetime.today()
        while current_date <= end_date:
            print(weekdays[current_date.weekday()], "{} {}:".format(current_date.day, current_date.strftime('%b')))

            current_tasks = [t for t in tasks if t.deadline == current_date.date()]
            if len(current_tasks) == 0:
                print("Nothing to do!\n")
            else:
                i = 1
                while i <= len(current_tasks):
                    print("{}. {}".format(i, current_tasks[i - 1].task))
                    i += 1

            current_date = current_date + timedelta(days=1)

            print("")

        print("")
    elif action == 3:
        print("All tasks:")

        tasks = session.query(Task).order_by(Task.deadline).all()

        if len(tasks) == 0:
            print("Nothing to do!\n")
        else:
            i = 1
            while i <= len(tasks):
                task = tasks[i - 1]
                print("{}. {}. {} {}".format(i, task.task, task.deadline.day, task.deadline.strftime('%b')))
                i += 1

            print("")
    elif action == 4:
        print("Missed tasks:")

        today = datetime.today()
        tasks = session.query(Task).filter(Task.deadline < today.date()).order_by(Task.deadline).all()

        if len(tasks) == 0:
            print("Nothing is missed!\n")
        else:
            i = 1
            while i <= len(tasks):
                task = tasks[i - 1]
                print("{}. {}. {} {}".format(i, task.task, task.deadline.day, task.deadline.strftime('%b')))
                i += 1

            print("")
    elif action == 5:
        print("Enter task")
        task_name = input()

        print("Enter deadline")
        deadline = input()

        new_task = Task(task=task_name, deadline=datetime.strptime(deadline, '%Y-%m-%d'))
        session.add(new_task)
        session.commit()

        print("The task has been added!\n")
    elif action == 6:
        print("Choose the number of the task you want to delete:")

        tasks = session.query(Task).order_by(Task.deadline).all()

        if len(tasks) == 0:
            print("Nothing to delete!\n")
        else:
            i = 1
            while i <= len(tasks):
                task = tasks[i - 1]
                print("{}. {}. {} {}".format(i, task.task, task.deadline.day, task.deadline.strftime('%b')))
                i += 1

            task_num_to_delete = int(input())
            task_to_delete = tasks[task_num_to_delete - 1]
            session.delete(task_to_delete)
            session.commit()

            print("The task has been deleted!\n")

    action = get_input()

print("Bye!")
