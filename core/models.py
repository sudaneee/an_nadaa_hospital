import random

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile




# Profile Model
class Profile(models.Model):
    USER_ROLES = [
        ('Admin', 'Administrator'),
        ('Doctor', 'Doctor'),
        ('Nurse', 'Nurse'),
        ('LabTech', 'Lab Technician'),
        ('Pharmacist', 'Pharmacist'),
        ('PharmacyHead', 'Pharmacy Head'),
        ('Receptionist', 'Receptionist'),
        ('Cashier', 'Cashier'),
        ('Accountant', 'Accountant'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=20, choices=USER_ROLES)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # Profile picture field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.role}"

class Family(models.Model):
    name = models.CharField(max_length=100)
    file_number = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self):
        return self.name

# HMO Model (for NHI / NHI - Private file types)
class HMO(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


# Company Model (for Company file type)
class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


# Patient Model
class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    FILE_TYPE_CHOICES = [
        ('Private/Individual', 'Private/Individual'),
        ('NHI', 'NHI'),
        ('Company', 'Company'),
        ('Family', 'Family'),
        ('NHI - Private', 'NHI - Private'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    family = models.ForeignKey(Family, related_name='patients', on_delete=models.SET_NULL, null=True, blank=True)
    age = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    patient_file_number = models.CharField(max_length=20, unique=True)
    file_type = models.CharField(max_length=30, choices=FILE_TYPE_CHOICES, null=True, blank=True)
    hmo = models.ForeignKey(HMO, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    next_of_kin_name = models.CharField(max_length=100)
    next_of_kin_relationship = models.CharField(max_length=50)
    next_of_kin_contact = models.CharField(max_length=15)
    blood_type = models.CharField(max_length=3, null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)
    insurance_info = models.CharField(max_length=255, null=True, blank=True)
    current_medications = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='patient_pictures/', null=True, blank=True)  # Profile picture field
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.patient_file_number})"



class Wallet(models.Model):
    family = models.OneToOneField(Family, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, null=True, blank=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def clean(self):
        if not self.family and not self.patient:
            raise ValidationError("Wallet must be associated with either a Family or a Patient.")
        if self.family and self.patient:
            raise ValidationError("Wallet cannot be associated with both a Family and a Patient.")
    
    def __str__(self):
        if self.family:
            return f"Wallet for Family {self.family.name} with balance {self.balance}"
        elif self.patient:
            return f"Wallet for Patient {self.patient.first_name} {self.patient.last_name} with balance {self.balance}"
        else:
            return "Wallet without association"


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=50, choices=[('Credit', 'Credit'), ('Debit', 'Debit'), ('Refund', 'Refund'), ('Transfer', 'Transfer')])
    transaction_method = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.date}"



# Doctor Model
class Doctor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'Doctor'})
    specialty = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.PositiveIntegerField()
    qualifications = models.TextField()
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.profile.user.first_name} {self.profile.user.last_name} ({self.specialty})"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    REASON_CATEGORY_CHOICES = [
        ('General Consultation', 'General Consultation'),
        ('Pediatrics', 'Pediatrics'),
        ('Antenatal Care', 'Antenatal Care'),
        ('Gynecology Registration', 'Gynecology Registration'),
        ('Gynecology FollowUp', 'Gynecology Follow Up'),
        ('Cardiology', 'Cardiology'),
        ('Gastroenterology', 'Gastroenterology'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_created')
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    reason_category = models.CharField(max_length=100, choices=REASON_CATEGORY_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self):
        return f"Appointment for {self.patient} with {self.doctor} on {self.appointment_date}"
# Ward Model
class Ward(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)  # inactive wards stay linked to historical admissions but drop out of the "create admission" picklist
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# Admission Model
class Admission(models.Model):
    STATUS_CHOICES = [
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    admission_date = models.DateTimeField(auto_now_add=True)
    discharge_date = models.DateTimeField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Ongoing')
    reason_category = models.CharField(max_length=100, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"Admission for {self.patient} by {self.doctor} on {self.admission_date}"

# Vital Sign Model
class VitalSign(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    recorded_at = models.DateTimeField(auto_now_add=True)
    height = models.CharField(max_length=20, null=True, blank=True)
    weight = models.CharField(max_length=20, null=True, blank=True)
    blood_pressure = models.CharField(max_length=20, null=True, blank=True)
    temperature = models.CharField(max_length=20, null=True, blank=True)
    pulse = models.CharField(max_length=20, null=True, blank=True)
    respiratory_rate = models.CharField(max_length=20, null=True, blank=True)
    oxygen_saturation = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Vital signs for {self.appointment.patient} recorded at {self.recorded_at}"


class ObservationChart(models.Model):
    admission = models.ForeignKey(Admission, null=True, blank=True, on_delete=models.CASCADE)
    temperature = models.FloatField(null=True, blank=True)
    pulse = models.CharField(max_length=20, null=True, blank=True)
    respiratory_rate = models.CharField(max_length=20, null=True, blank=True)
    blood_pressure = models.CharField(max_length=20, null=True, blank=True)
    oxygen_saturation = models.FloatField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    remark = models.TextField(null=True, blank=True)
    recorded_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f"Observation chart for {self.admission.patient} recorded at {self.recorded_at} by {self.recorded_by}"

class FluidChart(models.Model):
    admission = models.ForeignKey(Admission, null=True, blank=True, on_delete=models.CASCADE)
    intake_type = models.CharField(max_length=20, null=True, blank=True)
    intake_amount = models.CharField(max_length=20, null=True, blank=True)
    intake_route = models.CharField(max_length=20, null=True, blank=True)
    output_type = models.CharField(max_length=20, null=True, blank=True)
    output_amount = models.CharField(max_length=20, null=True, blank=True)
    output_remark = models.CharField(max_length=20, null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f"Fluid chart for {self.admission.patient} recorded at {self.recorded_at} by {self.recorded_by}"
    
class SeizureChart(models.Model):
    admission = models.ForeignKey(Admission, null=True, blank=True, on_delete=models.CASCADE)
    duration = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Seizure chart for {self.admission.patient} recorded at {self.recorded_at} by {self.recorded_by}"


class DownScoreChart(models.Model):
    admission = models.ForeignKey(Admission, null=True, blank=True, on_delete=models.CASCADE)
    respiratory_rate = models.CharField(max_length=20, null=True, blank=True)
    cyanosis = models.CharField(max_length=20, null=True, blank=True)
    retraction = models.CharField(max_length=20, null=True, blank=True)
    grunting = models.CharField(max_length=20, null=True, blank=True)
    air_entry = models.CharField(max_length=20, null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Down's score chart for {self.admission.patient} recorded at {self.recorded_at} by {self.recorded_by}"
     


class NurseHandover(models.Model):
    notes = models.TextField()
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)    

    def __str__(self):
        return f"Hand Over Note recorded at {self.recorded_at} by {self.recorded_by}"

class Investigation(models.Model):
    RESULT_TYPE_CHOICES = [
        ('Numeric', 'Numeric'),
        ('Reactive/Non-Reactive', 'Reactive/Non-Reactive'),
        ('Positive/Negative', 'Positive/Negative'),
        ('Text', 'Text'),
    ]
    
    name = models.CharField(max_length=100)
    unit_of_measurement = models.CharField(max_length=50)
    reference_range = models.CharField(max_length=100)
    result_type = models.CharField(max_length=200, choices=RESULT_TYPE_CHOICES, default='Text')  # Added field
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Investigation Request Model
class InvestigationRequest(models.Model):
    patient_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True, choices=[('Male', 'Male'), ('Female', 'Female')])
    age = models.CharField(max_length=100, null=True, blank=True)
    appointment = models.ForeignKey(Appointment, null=True, blank=True, on_delete=models.CASCADE)
    admission = models.ForeignKey(Admission, null=True, blank=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, null=True, blank=True, on_delete=models.CASCADE)
    investigation = models.ForeignKey(Investigation, on_delete=models.CASCADE)
    date_requested = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Requested', 'Requested'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Requested')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"InvestigationRequest for {self.patient if self.patient else self.patient_name} - {self.investigation.name} on {self.date_requested}"

# Investigation Result Model
class InvestigationResult(models.Model):
    request = models.OneToOneField(InvestigationRequest, on_delete=models.CASCADE)
    result_type_choices = [
        ('Numeric', 'Numeric'),
        ('Boolean', 'Boolean'),
        ('Text', 'Text'),
    ]
    result_type = models.CharField(max_length=10, choices=result_type_choices)
    numeric_result = models.FloatField(null=True, blank=True)
    boolean_result = models.BooleanField(null=True, blank=True)
    text_result = models.TextField(null=True, blank=True)
    result_date = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)  # Technician or Doctor who recorded the result
    is_abnormal = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"Result for {self.request} - {self.result_date}"

# Medication Model
class Medication(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Pharmacy Stock Model
class PharmacyStock(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_of_stock = models.DateTimeField(auto_now_add=True)
    unit = models.CharField(max_length=50, null=True, blank=True)  # e.g., 'bottles', 'packs', 'tablets'
    unit_price = unit_price = models.DecimalField(max_digits=10, decimal_places=2) 
    expiry_date = models.DateField(null=True, blank=True)
    batch_number = models.CharField(max_length=50, null=True, blank=True)
    manufacture_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='pharmacy_stock_created')    
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='pharmacy_stock_updated')    

    def __str__(self):
        return f"{self.medication.name} - {self.quantity}"

    def amount(self):
        return self.quantity * self.unit_price

class PharmacyStockTransaction(models.Model):
    pharmacy_stock = models.ForeignKey(PharmacyStock, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=[('Addition', 'Addition'), ('Removal', 'Removal')], null=True, blank=True)
    quantity = models.PositiveIntegerField()
    patient = models.ForeignKey('Patient', on_delete=models.SET_NULL, null=True, blank=True, related_name='stock_transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='pharmacy_stock_transaction_created')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='pharmacy_stock_transaction_updated')

    def __str__(self):
        return f"{self.pharmacy_stock.medication.name} - {self.transaction_type} - {self.quantity} - {self.created_by}"   


# Prescription Model
class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, null=True, blank=True, on_delete=models.CASCADE)
    admission = models.ForeignKey(Admission, null=True, blank=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    date_prescribed = models.DateTimeField(auto_now_add=True)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    dosage = models.TextField()
    instructions = models.TextField()
    duration = models.CharField(max_length=50, null=True, blank=True)
    frequency = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_invoiced = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f"Prescription for {self.appointment.patient if self.appointment else self.admission.patient} on {self.date_prescribed}"


class DoctorNote(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, null=True, blank=True )
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming User model is used for doctors
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note by {self.doctor.username} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
class Diagnosis(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, null=True, blank=True )
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming User model is used for doctors
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Diagnosis by {self.doctor.username} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

# Supplier Model
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Invoice(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    family = models.ForeignKey(Family, related_name='invoices', on_delete=models.CASCADE, null=True, blank=True)
    custom_name = models.CharField(max_length=255, null=True, blank=True)
    invoice_number = models.CharField(max_length=10, unique=True, blank=True, editable=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Dispensed', 'Dispensed')], default='Pending')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.invoice_number:
            Invoice.objects.filter(pk=self.pk).update(invoice_number=str(self.pk))
            self.invoice_number = str(self.pk)

    def __str__(self):
        return f"Invoice #{self.invoice_number} for {self.patient or self.family or self.custom_name}"

            # Method to check if medication is dispensed
    def is_dispensed(self):
        return self.status == 'Dispensed'


    def clean(self):
        # Ensure only one of patient, family, or custom name is set
        if not self.patient and not self.family and not self.custom_name:
            raise ValidationError("Invoice must be linked to either a patient, family, or have a custom name.")
        if (self.patient and self.family) or (self.patient and self.custom_name) or (self.family and self.custom_name):
            raise ValidationError("Invoice cannot be linked to more than one of patient, family, or custom name.")



class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, related_name='items', null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    medication = models.ForeignKey(Medication, on_delete=models.SET_NULL, null=True, blank=True)
    investigation_request = models.ForeignKey(InvestigationRequest, on_delete=models.SET_NULL, null=True, blank=True)
    descriptions = models.CharField(max_length=255, null=True, blank=True)  # For 'Others' type
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        
        if self.service:
            return f"Service: {self.service.name} x {self.quantity} for Invoice #{self.invoice.id}"
        elif self.medication:
            return f"Medication: {self.medication.name} x {self.quantity} for Invoice #{self.invoice.id}"
        elif self.investigation_request:
            return f"Investigation: {self.investigation_request.investigation.name} x {self.quantity} for Invoice #{self.invoice.id}"
        elif self.descriptions:
            return f"Other: {self.descriptions} x {self.quantity} for Invoice #{self.invoice.id}"
        else:
            return str(self.invoice)


# Payment Model
class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_number = models.CharField(max_length=10, blank=True, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True, db_index=True)
    payment_method = models.CharField(max_length=50)  # e.g., 'Cash', 'Credit Card', 'Insurance'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)  # Technician or Doctor who recorded the result

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.payment_number:
            Payment.objects.filter(pk=self.pk).update(payment_number=str(self.pk))
            self.payment_number = str(self.pk)

    def __str__(self):
        return f"Payment of {self.amount} for {self.invoice.patient} on {self.payment_date}"
    


class Refund(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)  # Technician or Doctor who recorded the result
    def __str__(self):
        return f"Refund for {self.payment.invoice}"
    



# Feedback Model
class Feedback(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    feedback = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback from {self.patient} - Rating: {self.rating}"



# Inventory Category Model
class InventoryCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Inventory Item Model
class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(InventoryCategory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_level = models.PositiveIntegerField(default=10)  # Level to trigger reordering
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Inventory Transaction Model
class InventoryTransaction(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity_changed = models.IntegerField()  # Positive for addition, negative for removal
    transaction_type = models.CharField(max_length=50, choices=[('Addition', 'Addition'), ('Removal', 'Removal')])
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.quantity_changed} for {self.item.name} on {self.date}"




# Define report types, e.g., 'X-Ray', 'Blood Test', etc.
class DiagnosticReportType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Model to store key-value parameters specific to the report type
class DiagnosticReportParameter(models.Model):
    report_type = models.ForeignKey(DiagnosticReportType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


# Main Diagnostic Report model
class DiagnosticReport(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    patient_name = models.CharField(max_length=100)
    patient_age = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    report_type = models.ForeignKey(DiagnosticReportType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.report_type.name} Report for {self.patient_name}"


# Model to store results of parameters specific to the report
class DiagnosticReportResult(models.Model):
    report = models.ForeignKey(DiagnosticReport, on_delete=models.CASCADE)
    diagnostic_report_parameter = models.ForeignKey(DiagnosticReportParameter, on_delete=models.CASCADE)
    value = models.TextField()

    def __str__(self):
        return f"{self.diagnostic_report_parameter.name}: {self.value}"

    class Meta:
        unique_together = ('report', 'diagnostic_report_parameter')


class DiagnosticReportImage(models.Model):
    report = models.ForeignKey('DiagnosticReport', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='diagnostic_reports/')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
            # Open the image file
            img = Image.open(self.image)

            # Set maximum size for the image (width, height) in pixels
            max_size = (800, 800)  # You can adjust this as needed

            # Resize the image (maintaining aspect ratio)
            img.thumbnail(max_size, Image.LANCZOS)

            # Save the image to a BytesIO buffer
            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=70)  # Compress the image to 70% quality (adjustable)

            # Create a new Django file-like object to save to the model
            img_content = ContentFile(img_io.getvalue(), self.image.name)

            # Save the compressed image file to the model
            self.image.save(self.image.name, img_content, save=False)

            super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.report}"