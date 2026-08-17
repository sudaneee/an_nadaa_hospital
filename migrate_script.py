import sqlite3
import os
from django.utils import timezone
from django.db import IntegrityError
from core.models import (Profile, Family, Patient, Wallet, Transaction, Doctor, Appointment, Admission,
                                    VitalSign, ObservationChart, FluidChart, SeizureChart, DownScoreChart, 
                                    NurseHandover, Investigation, InvestigationRequest, InvestigationResult, 
                                    Medication, PharmacyStock, Prescription, DoctorNote, Diagnosis, Supplier, 
                                    Service, Invoice, InvoiceItem, Payment, Refund, Feedback)

# Path to old SQLite database
old_db_path = os.path.join(os.getcwd(), 'db_backup.sqlite3')

# Connect to the old database
conn = sqlite3.connect(old_db_path)
cursor = conn.cursor()

# Function to migrate data
def migrate_data():
    # Migrate Profiles
    try:
        cursor.execute("SELECT * FROM core_profile")
        profiles = cursor.fetchall()
        for profile in profiles:
            try:
                # Unpack profile data (adjust indices based on actual table structure)
                _, user_id, role, contact_number, address, profile_picture, created_at, updated_at, is_active = profile
                
                # Create new Profile
                new_profile = Profile(
                    user_id=int(user_id) if user_id.isdigit() else None,
                    role=role,
                    contact_number=contact_number,
                    address=address,
                    profile_picture=profile_picture,
                    created_at=created_at,
                    updated_at=updated_at,
                    is_active=bool(is_active)
                )
                new_profile.save()
            except IntegrityError as e:
                print(f"Error saving profile: {e}")
        print("Profiles migrated successfully.")
    except Exception as e:
        print(f"Error migrating profiles: {e}")

    # Migrate Families
    try:
        cursor.execute("SELECT * FROM core_family")
        families = cursor.fetchall()
        for family in families:
            try:
                _, name, file_number, address, phone_number, created_at, updated_at, created_by_id = family

                # Create new Family
                new_family = Family(
                    name=name,
                    file_number=file_number,
                    address=address,
                    phone_number=phone_number,
                    created_at=created_at,
                    updated_at=updated_at,
                    created_by_id=int(created_by_id) if created_by_id else None
                )
                new_family.save()
            except IntegrityError as e:
                print(f"Error saving family: {e}")
        print("Families migrated successfully.")
    except Exception as e:
        print(f"Error migrating families: {e}")

    # Migrate Patients
    try:
        cursor.execute("SELECT * FROM core_patient")
        patients = cursor.fetchall()
        for patient in patients:
            try:
                _, first_name, last_name, age, gender, contact_number, address, patient_file_number, \
                next_of_kin_name, next_of_kin_relationship, next_of_kin_contact, blood_type, allergies, \
                medical_history, insurance_info, current_medications, profile_picture, created_at, updated_at, \
                is_active = patient

                # Create new Patient
                new_patient = Patient(
                    first_name=first_name,
                    last_name=last_name,
                    age=age,
                    gender=gender,
                    contact_number=contact_number,
                    address=address,
                    patient_file_number=patient_file_number,
                    next_of_kin_name=next_of_kin_name,
                    next_of_kin_relationship=next_of_kin_relationship,
                    next_of_kin_contact=next_of_kin_contact,
                    blood_type=blood_type,
                    allergies=allergies,
                    medical_history=medical_history,
                    insurance_info=insurance_info,
                    current_medications=current_medications,
                    profile_picture=profile_picture,
                    created_at=created_at,
                    updated_at=updated_at,
                    is_active=bool(is_active)
                )
                new_patient.save()
            except IntegrityError as e:
                print(f"Error saving patient: {e}")
        print("Patients migrated successfully.")
    except Exception as e:
        print(f"Error migrating patients: {e}")

    # Migrate Appointments
    try:
        cursor.execute("SELECT * FROM core_appointment")
        appointments = cursor.fetchall()
        for appointment in appointments:
            try:
                _, appointment_date, reason, status, reason_category, created_at, updated_at, \
                doctor_id, patient_id, created_by_id = appointment

                # Create new Appointment
                new_appointment = Appointment(
                    appointment_date=appointment_date,
                    reason=reason,
                    status=status,
                    reason_category=reason_category,
                    created_at=created_at,
                    updated_at=updated_at,
                    doctor_id=int(doctor_id) if doctor_id else None,
                    patient_id=int(patient_id) if patient_id else None,
                    created_by_id=int(created_by_id) if created_by_id else None
                )
                new_appointment.save()
            except IntegrityError as e:
                print(f"Error saving appointment: {e}")
        print("Appointments migrated successfully.")
    except Exception as e:
        print(f"Error migrating appointments: {e}")

    # Close the cursor and connection
    cursor.close()
    conn.close()

# Run the migration
migrate_data()
