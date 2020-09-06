from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __str__(self):
        return self.task


Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()


def add_task():
    task = input()
    print('Enter deadline')
    session.add(Task(task=task, deadline=datetime.strptime(input(), '%Y-%m-%d').date()))
    session.commit()
    print('The task has been added!\n')


def day_task(date):
    tasks = session.query(Task).filter(Task.deadline == date).all()
    if len(tasks) == 0:
        print('Nothing to do!\n')
    else:
        i = 1
        for _task in tasks:
            print(f'{i}. {_task}\n')
            i += 1


def week_tasks():
    start_date = datetime.now().date()
    for i in range(0, 7):
        date = start_date + timedelta(days=i)
        print(f'{date.strftime("%A")} {date.strftime("%#d")} {date.strftime("%b")}')
        print(date)
        day_task(date)


def all_tasks():
    print('All tasks:')
    tasks = session.query(Task).order_by(Task.deadline)
    print_task(tasks)
    print()


def missed_tasks():
    print('Missed tasks:')
    tasks = session.query(Task).filter(Task.deadline < datetime.now().date()).order_by(Task.deadline).all()
    if len(tasks) == 0:
        print('Nothing to do!')
    else:
        print_task(tasks)
    print()


def delete_tasks():
    print('Choose the number of the task you want to delete:')
    tasks = session.query(Task).order_by(Task.deadline)
    print_task(tasks)
    session.delete(tasks[int(input()) - 1])
    session.commit()
    print('The task has been deleted!\n')


def print_task(tasks):
    i = 1
    for task in tasks:
        print(f'{i}. {task}. {task.deadline.strftime("%#d")} {task.deadline.strftime("%b")}')
        i += 1


if __name__ == '__main__':
    while True:
        print('1) Today\'s tasks\n2) Week\'s tasks\n3) All tasks'
              '\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit')
        check = int(input())
        print()
        if check == 0:
            print('Bye!')
            break
        elif check == 1:
            day_task(datetime.now().date())
        elif check == 2:
            week_tasks()
        elif check == 3:
            all_tasks()
        elif check == 4:
            missed_tasks()
        elif check == 5:
            add_task()
        elif check == 6:
            delete_tasks()

