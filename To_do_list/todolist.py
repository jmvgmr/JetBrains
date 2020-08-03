from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


def show_week_tasks(ses):
    today = datetime.today()
    for i in range(7):
        date = today + timedelta(days=i)
        print(f"{date.strftime('%A %d %b')}:")
        show_tasks(ses, date=date)
        print('')


def show_missed_tasks(ses):
    rows = ses.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    print('Missed tasks:')
    if rows:
        for i, row in enumerate(rows, 1):
            print(f'{i}. {row}. {row.deadline.strftime("%d %b")}')
    else:
        print('Nothing is missed!')


def show_tasks(ses, all_tasks=False, date=datetime.today()):
    if all_tasks:
        rows = ses.query(Table).all()
    else:
        rows = ses.query(Table).filter(Table.deadline == date.date()).all()
    if rows:
        for i, row in enumerate(rows, 1):
            print(f'{i}. {row}')
    else:
        print('Nothing to do!')


def add_task(ses):
    in_task = input('Enter task\n')
    in_deadline = input('Enter deadline\n')
    new_row = Table(task=in_task, deadline=datetime.strptime(in_deadline, '%Y-%m-%d'))
    ses.add(new_row)
    ses.commit()
    print('The task has been added!')


def delete_task(ses):
    rows = ses.query(Table).order_by(Table.deadline).all()
    if rows:
        print('Choose the number of the task you want to delete:')
        for i, row in enumerate(rows, 1):
            print(f'{i}. {row}. {row.deadline.strftime("%d %b")}')
        ses.delete(rows[int(input()) - 1])
        ses.commit()
        print('The task has been deleted!')
    else:
        print('Nothing to delete')


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

choice = 1
while choice != 0:
    print("""
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
    choice = int(input())
    print('')
    if choice == 1:
        tod = datetime.today()
        print(f'Today {tod.strftime("%d %b")}:')
        show_tasks(session, date=tod)
    elif choice == 2:
        show_week_tasks(session)
    elif choice == 3:
        print('All tasks:')
        show_tasks(session, True)
    elif choice == 4:
        show_missed_tasks(session)
    elif choice == 5:
        add_task(session)
    elif choice == 6:
        delete_task(session)
    else:
        break
print('Bye!')
