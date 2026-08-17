from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('update-profile/<int:profile_id>/', views.update_profile, name='update_profile'),
    path('receptionist/', views.receptionist_dashboard, name='receptionist_dashboard'),
    path('receptionist/create-patient/', views.create_patient, name='create_patient'),
    path('receptionist/create-family/', views.create_family, name='create_family'),
    path('receptionist/family-list/', views.family_list, name='family_list'),
    path('receptionist/family-member-list/<int:family_id>/', views.view_family_members, name='view_family_members'),
    path('receptionist/edit-family/<int:family_id>/', views.edit_family, name='edit_family'),
    path('receptionist/delete-family/<int:family_id>/', views.delete_family, name='delete_family'),
    path('receptionist/update-patient/<int:patient_id>/', views.update_patient, name='update_patient'),
    path('receptionist/delete-patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),

    # HMOs
    path('hmos/', views.hmo_list, name='hmo_list'),
    path('hmos/create/', views.hmo_form, name='hmo_create'),
    path('hmos/update/<int:hmo_id>/', views.hmo_form, name='hmo_update'),
    path('hmos/delete/<int:hmo_id>/', views.hmo_delete, name='hmo_delete'),

    # Companies
    path('companies/', views.company_list, name='company_list'),
    path('companies/create/', views.company_form, name='company_create'),
    path('companies/update/<int:company_id>/', views.company_form, name='company_update'),
    path('companies/delete/<int:company_id>/', views.company_delete, name='company_delete'),

    # Appointments
    path('appointments/create/', views.create_appointment, name='create_appointment'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/update/<int:appointment_id>/', views.update_appointment, name='update_appointment'),
    path('appointments/view/<int:appointment_id>/', views.view_appointment, name='view_appointment'),
    path('appointments/<int:appointment_id>/notes/', views.view_notes, name='view_appointment_notes'),
    path('appointments/<int:appointment_id>/delete/', views.delete_appointment, name='delete_appointment'),
    path('create-diagnosis/appointment/<int:appointment_id>/', views.create_diagnosis, name='create_diagnosis_appointment'),
    
    # Vital Sign
    path('appointments/<int:appointment_id>/vital-signs/add/', views.add_vital_sign, name='add_vital_sign'),
    path('appointment/<int:appointment_id>/vital-signs/update/<int:vital_sign_id>/', views.update_vital_sign, name='update_vital_sign'),
    path('appointment/<int:appointment_id>/vital-signs/delete/<int:vital_sign_id>/', views.delete_vital_sign, name='delete_vital_sign'),

    # Doctor Dashboard
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/<int:appointment_id>/complete/', views.complete_appointment, name='complete_appointment'),
    
    # For Appointment
    path('doctor/<int:appointment_id>/prescription/add/', views.add_prescriptions, name='add_prescription'),
    path('doctor/<int:appointment_id>/investigation-request/create/', views.create_investigation_requests, name='create_investigation_request'),
    
    
    # For Admissions
    path('doctor/admission/<int:admission_id>/prescription/add/', views.add_prescriptions, name='add_prescription_admission'),
    path('doctor/admission/<int:admission_id>/investigation-request/create/', views.create_investigation_requests, name='create_investigation_request_admission'),
    
    path('doctor/<int:appointment_id>/admission/create/', views.create_admission, name='create_admission'),
    path('doctor/admissions/', views.admissions, name='admissions'),
    path('doctor/admissions/discharge-patient/<int:admission_id>/', views.discharge_patient, name='discharge_patient'),
    path('admissions/<int:admission_id>/notes/', views.view_notes, name='view_admission_notes'),
    path('create-diagnosis/admission/<int:admission_id>/', views.create_diagnosis, name='create_diagnosis_admission'),



    # Nurse Dashboard
    path('nurse/dashboard/', views.nurse_dashboard, name='nurse_dashboard'),
    path('nurse/observation-chart/create/<int:admission_id>/', views.create_observation_chart, name='create_observation_chart'),
    path('nurse/observation-chart/update/<int:chart_id>/', views.update_observation_chart, name='update_observation_chart'),
    path('nurse/observation-chart/delete/<int:chart_id>/', views.delete_observation_chart, name='delete_observation_chart'),

    path('nurse/fluid-chart/create/<int:admission_id>/', views.create_fluid_chart, name='create_fluid_chart'),
    path('nurse/fluid-chart/update/<int:chart_id>/', views.update_fluid_chart, name='update_fluid_chart'),
    path('nurse/fluid-chart/delete/<int:chart_id>/', views.delete_fluid_chart, name='delete_fluid_chart'),

    path('nurse/seizure-chart/create/<int:admission_id>/', views.create_seizure_chart, name='create_seizure_chart'),
    path('nurse/seizure-chart/update/<int:chart_id>/', views.update_seizure_chart, name='update_seizure_chart'),
    path('nurse/seizure-chart/delete/<int:chart_id>/', views.delete_seizure_chart, name='delete_seizure_chart'),

    path('nurse/down-score-chart/create/<int:admission_id>/', views.create_down_score_chart, name='create_down_score_chart'),
    path('nurse/down-score-chart/update/<int:chart_id>/', views.update_down_score_chart, name='update_down_score_chart'),
    path('nurse/down-score-chart/delete/<int:chart_id>/', views.delete_down_score_chart, name='delete_down_score_chart'),

    path('nurse/admission/view/<int:admission_id>/', views.view_admission, name='view_admission'),
    path('nurse/handover-note/', views.create_nurse_handover, name='create_nurse_handover'),
    path('nurse/handover-note-list/', views.list_nurse_handover, name='list_nurse_handover'),
    path('nurse/handover-note/update/<int:pk>/', views.update_nurse_handover, name='update_nurse_handover'),
    path('nurse/handover-note/delete/<int:pk>/', views.delete_nurse_handover, name='delete_nurse_handover'),

    # Investigation
    path('investigations/<int:request_id>/result/', views.view_investigation_result, name='view_investigation_result'),

    # Pharmacy
    path('pharmacy/dashboard/', views.pharmacy_dashboard, name='pharmacy_dashboard'),
    path('pharmacy/invoice/create/<int:appointment_id>/', views.create_invoice, name='create_invoice'),
    # path('pharmacy/mark_as_dispensed/<int:invoice_id>/', views.dispense_medication, name='dispense_medication'),
    path('pharmacy/sell-medications/', views.sell_medications, name='sell_medications'),


    path('medications/', views.manage_medications, name='manage_medications'),
    path('medications/form/', views.medication_form, name='medication_form'),
    path('medications/delete/<int:medication_id>/', views.delete_medication, name='delete_medication'),
    path('medications/form/<int:medication_id>/', views.medication_form, name='medication_form'),
    path('pharmacy-stock/', views.manage_pharmacy_stock, name='manage_pharmacy_stock'),
    path('pharmacy-stock/form/', views.pharmacy_stock_form, name='pharmacy_stock_form'),
    # path('pharmacy-stock/form/<int:stock_id>/', views.pharmacy_stock_form, name='pharmacy_stock_form'),
    path('pharmacy_stock/update/<int:pk>/', views.pharmacy_stock_update, name='pharmacy_stock_update'),
    path('pharmacy_stock/delete/<int:pk>/', views.pharmacy_stock_delete, name='pharmacy_stock_delete'),
    path('pharmacy_stock_transaction/', views.pharmacy_stock_transaction, name="pharmacy_stock_transaction"),
    path('pharmacy/bin-card/', views.bin_card_list, name='bin_card_list'),
    path('pharmacy/bin-card/<int:medication_id>/', views.bin_card_detail, name='bin_card_detail'),

    path('suppliers/', views.manage_suppliers, name='manage_suppliers'),
    path('suppliers/form/', views.supplier_form, name='supplier_form'),
    path('suppliers/form/<int:supplier_id>/', views.supplier_form, name='supplier_form'),


    # Invoice management for medications
    path('pharmacy/invoices/', views.manage_medication_invoices, name='manage_medication_invoices'),
    path('pharmacy/invoice/update/<int:invoice_id>/', views.update_invoice, name='update_invoice'),
    


    # Cashier
    path('cashier/dashboard/', views.cashier_dashboard, name='cashier_dashboard'),
    path('cashier/payments/', views.payments, name='payments'),
    path('cashier/update-invoice-payment/<int:invoice_id>/', views.update_invoice_payment, name='update_invoice_payment'),
    path('cashier/invoice/<int:invoice_id>/', views.view_invoice, name='view_invoice'),
    path('cashier/merge-invoices/', views.merge_invoices, name='merge_invoices'),
    path('cashier/delete_invoices/', views.delete_invoices, name='delete_invoices'),
    path('cashier/edit-payment/<int:payment_id>/', views.edit_payment, name='edit_payment'),
    path('cashier/delete-payment/<int:payment_id>/', views.delete_payment, name='delete_payment'),
    path('cashier/create-invoice-items/', views.create_invoice_and_items, name='create_invoice_and_items'),
    path('cashier/day-book/', views.day_book, name='day_book'),
    path('cashier/wallets/', views.wallet_list, name='wallet_list'),
    path('cashier/wallets/<int:wallet_id>/transactions/', views.view_wallet_transactions, name='view_wallet_transactions'),
    path('cashier/wallets/transfer/', views.transfer_funds, name='transfer_funds'),
    path('cashier/credit-wallet/', views.credit_wallet_view, name='credit_wallet'),
    path('cashier/wallet/receipt/<int:transaction_id>/', views.wallet_funding_receipt, name='wallet_funding_receipt'),
    path('cashier/view_paid_invoice/<int:invoice_id>/', views.view_paid_invoice, name='view_paid_invoice'),

    


# Lab Technician URLs
    path('labtech/dashboard/', views.labtech_dashboard, name='labtech_dashboard'),
    path('labtech/investigation-result/create/<int:invoice_id>/', views.create_grouped_investigation_results, name='create_grouped_investigation_results'),
    path('labtech/investigation-requests/', views.manage_investigation_requests, name='manage_investigation_requests'),
    path('labtech/investigation-requests/create/', views.create_investigation_request, name='create_investigation_request'),
    path('labtech/investigation-requests/delete/<int:request_id>/', views.delete_investigation_request, name='delete_investigation_request'),
    path('labtech/investigations/', views.manage_investigations, name='manage_investigations'),
    path('labtech/investigations/create/', views.create_investigation, name='create_investigation'),
    path('labtech/investigations/update/<int:investigation_id>/', views.update_investigation, name='update_investigation'),
    path('labtech/investigations/delete/<int:investigation_id>/', views.delete_investigation, name='delete_investigation'),
    path('labtech/investigation-result/view/<int:invoice_id>/', views.view_grouped_investigation_results, name='view_grouped_investigation_results'),


# admin
    path('statistics/', views.statistics_dashboard, name='statistics_dashboard'),
    path('users-profiles/', views.manage_user_profiles, name='manage_user_profiles'),
    path('users-profiles/delete/<int:profile_id>', views.delete_user_profiles, name='delete_user_profiles'),
    path('dispense-medication/<int:invoice_id>/', views.dispense_medication, name='dispense_medication'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/update/<int:pk>/', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
    
    path('items/', views.item_list, name='item_list'),
    path('items/create/', views.item_create, name='item_create'),
    path('items/update/<int:pk>/', views.item_update, name='item_update'),
    path('items/delete/<int:pk>/', views.item_delete, name='item_delete'),
    
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/create/', views.transaction_create, name='transaction_create'),
    path('transactions/update/<int:pk>/', views.transaction_update, name='transaction_update'),
    path('transactions/delete/<int:pk>/', views.transaction_delete, name='transaction_delete'),


 # DiagnosticReportType URLs
    path('report-types/', views.report_type_list, name='report_type_list'),
    path('report-types/create/', views.report_type_create, name='report_type_create'),
    path('report-types/update/<int:pk>/', views.report_type_update, name='report_type_update'),
    path('report-types/delete/<int:pk>/', views.report_type_delete, name='report_type_delete'),

    # DiagnosticReportParameter URLs
    path('report-parameters/', views.report_parameter_list, name='report_parameter_list'),
    path('report-parameters/create/', views.report_parameter_create, name='report_parameter_create'),
    path('report-parameters/update/<int:pk>/', views.report_parameter_update, name='report_parameter_update'),
    path('report-parameters/delete/<int:pk>/', views.report_parameter_delete, name='report_parameter_delete'),

    # Diagnostic Report
    path('diagnostic-reports/create/', views.create_diagnostic_report, name='create_diagnostic_report'),
    path('reports/get-parameters/<int:report_type_id>/', views.get_parameters, name='get_parameters'),
    path('diagnostic-reports/', views.diagnostic_report_list, name='diagnostic_report_list'),
    path('diagnostic-reports/delete/<int:report_id>/', views.diagnostic_report_delete, name='diagnostic_report_delete'),
    path('diagnostic-reports/edit/<int:report_id>/', views.diagnostic_report_edit, name='diagnostic_report_edit'),

]
