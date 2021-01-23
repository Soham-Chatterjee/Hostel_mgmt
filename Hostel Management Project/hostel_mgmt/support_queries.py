from hostel_mgmt import db, cursor

def get_last_stu_id():
    cursor.execute(f"select last_insert_id() from stu_details")
    return cursor.fetchone()[0]


def show_vacant_rooms():
    cursor.execute("select room_id from room where status='vacant'")
    return [res[0] for res in cursor.fetchall()]


def show_vacant_blocks():
    cursor.execute("select block_id from blocks where status='vacant'")
    return [res[0] for res in cursor.fetchall()]


def show_all_rooms():
    cursor.execute("select room_id from room")
    return [res[0] for res in cursor.fetchall()]


def show_rooms(type):
    cursor.execute("select room_id from room where type='{type}'")
    return [res[0] for res in cursor.fetchall()]


def show_rooms_from_block(b_id):
    cursor.execute(f"select room_id from room where block_id='{b_id}' and status='vacant'")
    return [res[0] for res in cursor.fetchall()]


def show_all_blocks():
    cursor.execute("select block_id from blocks")
    return [res[0] for res in cursor.fetchall()]


def get_block_type(b_id):
    cursor.execute(f"select block_type from blocks where block_id='{b_id}'")
    return cursor.fetchone()[0]


def get_w_id(b_id):
    cursor.execute(f"select warden_id from blocks where block_id='{b_id}'")
    return cursor.fetchone()[0]

def get_updated_w_id(wid):
    cursor.execute(f"select staff_id from staff where is_warden='Yes' and staff_id!='{wid}'")
    return [res[0] for res in cursor.fetchall()]

def get_all_wardens():
    cursor.execute(f"select staff_id from staff where is_warden='Yes'")
    return [res[0] for res in cursor.fetchall()]


def show_courses():
    cursor.execute("select course_id from courses")
    return [res[0] for res in cursor.fetchall()]


def show_all_stu():
    cursor.execute("select stu_id from student")
    return [res[0] for res in cursor.fetchall()]

def list_stu_paid():
    cursor.execute("select distinct stu_id from transactions")
    return [res[0] for res in cursor.fetchall()]


def get_stu_name(sid):
    cursor.execute(f"select name from stu_details where stu_id='{sid}'")
    return cursor.fetchone()[0]

def get_stu_cont(sid):
    cursor.execute(f"select contact_no from stu_details where stu_id='{sid}'")
    return cursor.fetchone()[0]

def get_meal_pref(sid):
    cursor.execute(f"select is_veg from student where stu_id='{sid}'")
    return cursor.fetchone()[0]

def get_stu_address(sid):
    cursor.execute(f"select address from stu_details where stu_id='{sid}'")
    return cursor.fetchone()[0]

def get_guar_name(sid):
    cursor.execute(f"select guardian_name from stu_details where stu_id='{sid}'")
    return cursor.fetchone()[0]

def get_guar_cont(sid):
    cursor.execute(f"select guardian_cont_no from stu_details where stu_id='{sid}'")
    return cursor.fetchone()[0]

def get_stu_course(sid):
    cursor.execute(f"select course_id from student where stu_id='{sid}'")
    return cursor.fetchone()[0]

def get_stu_dob(sid):
    cursor.execute(f"select dob from stu_details where stu_id='{sid}'")
    return cursor.fetchone()[0]

def get_stu_gender(sid):
    cursor.execute(f"select gender from stu_details where stu_id='{sid}'")
    return cursor.fetchone()[0]

def get_stu_bgrp(sid):
    cursor.execute(f"select blood_grp from stu_details where stu_id='{sid}'")
    return cursor.fetchone()[0]

def get_stu_room(sid):
    cursor.execute(f"select room_id from student where stu_id='{sid}'")
    return cursor.fetchone()[0]

def get_block_type(bid):
    cursor.execute(f"select block_type from blocks where block_id='{bid}'")
    return cursor.fetchone()[0]

def get_block_warden(bid):
    cursor.execute(f"select warden_id from blocks where block_id='{bid}'")
    return cursor.fetchone()[0]

def get_block_gender(bid):
    cursor.execute(f"select gender from blocks where block_id='{bid}'")
    return cursor.fetchone()[0]

def get_block_mess(bid):
    cursor.execute(f"select mess_id from blocks where block_id='{bid}'")
    return cursor.fetchone()[0]

def get_sing_room(bid):
    cursor.execute(f"select count(*) from room where block_id='{bid}' and no_of_beds=1 group by no_of_beds;")
    return cursor.fetchone()[0]

def get_doub_room(bid):
    cursor.execute(f"select count(*) from room where block_id='{bid}' and no_of_beds=2 group by no_of_beds;")
    return cursor.fetchone()[0]

def get_trip_room(bid):
    cursor.execute(f"select count(*) from room where block_id='{bid}' and no_of_beds=3 group by no_of_beds;")
    return cursor.fetchone()[0]

def show_all_staff():
    cursor.execute(f"select staff_id from staff")
    return [res[0] for res in cursor.fetchall()]

def get_staff_name(stid):
    cursor.execute(f"select name from staff where staff_id='{stid}'")
    return cursor.fetchone()[0]

def get_staff_gender(stid):
    cursor.execute(f"select gender from staff where staff_id='{stid}'")
    return cursor.fetchone()[0]

def get_staff_dob(stid):
    cursor.execute(f"select dob from staff where staff_id='{stid}'")
    return cursor.fetchone()[0]

def get_staff_cont(stid):
    cursor.execute(f"select contact_no from staff where staff_id='{stid}'")
    return cursor.fetchone()[0]

def get_staff_pos(stid):
    cursor.execute(f"select is_warden from staff where staff_id='{stid}'")
    return cursor.fetchone()[0]

def show_all_mess():
    cursor.execute("select mess_id from mess")
    return [res[0] for res in cursor.fetchall()]


def get_fee_details(sid):
    cursor.execute(f"select room_charges, mess_charges, add_charges, total_charge from stu_fees where stu_id={sid}")
    result = cursor.fetchone()
    room_charges = result[0]
    mess_charges = result[1]
    add_charges = result[2]
    total_charge = result[3]
    return (room_charges, mess_charges, add_charges, total_charge)


def get_tranid(sid):
    cursor.execute(f"select transaction_id, month_paid from transactions where stu_id='{sid}'")
    return cursor.fetchall()


def get_tmonth(sid, tmonth):
    cursor.execute(f"select transaction_id from transactions where stu_id='{sid}' and month_paid='{tmonth}'")
    return cursor.fetchone()[0]


def get_room_by_cat(cat):
    cursor.execute(f"select block_id from blocks where gender='{cat}' and status='vacant'")
    b_ids = cursor.fetchall()
    room_list = []
    for bid in b_ids:
        cursor.execute(f"select room_id from room where block_id='{bid[0]}' and status='vacant'")
        rooms = cursor.fetchall()
        for room in rooms:
            room_list.append(room[0])
    return room_list

def get_stu_for_show():
    heading_list = ['Student ID', 'Name', 'Contact','Course ID', 'Room ID']
    cursor.execute(f"select s.stu_id, sd.name, sd.contact_no, s.course_id, s.room_id from student s, stu_details sd where s.stu_id=sd.stu_id")
    return ('stu_details', heading_list, cursor.fetchall())



def get_block_for_show():
    heading_list = ['Block ID', 'Type', 'Gender', 'Total Rooms', 'Number of beds', 'Vacant Beds']
    cursor.execute(f"select block_id, block_type, gender, no_of_rooms, no_of_beds, vacant_beds from blocks")
    return ('block_details', heading_list, cursor.fetchall())



def get_room_for_show():
    heading_list = ['Room ID', 'Block ID', 'Type', 'Total Rooms', 'Occupants']
    cursor.execute(f"select room_id, block_id, room_type, no_of_beds, occupants from room")
    return ('room_details', heading_list, cursor.fetchall())



def get_staff_for_show():
    heading_list = ['Staff ID', 'Name', 'Gender', 'Date of Birth', 'Contact']
    cursor.execute(f"select staff_id, name, gender, dob, contact_no from staff")
    return ('staff_details', heading_list, cursor.fetchall())



def get_mess_for_show():
    heading_list = ['Mess ID']
    cursor.execute(f"select mess_id from mess")
    return ('mess_details', heading_list, cursor.fetchall())

def get_courses_for_show():
    heading_list = ['Course ID', 'Course Name', 'Semesters']
    cursor.execute(f"select course_id, course_name, num_sems from courses")
    return ('courses_details', heading_list, cursor.fetchall())


