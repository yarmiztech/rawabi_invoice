{
    'name': "Rawabi E-Invoice ",
    'author':
        'ENZAPPS',
    'summary': """
This module is for Rawabi.
""",

    'description': """
        This module is for Rawabi.
    """,
    'website': "",
    'category': 'base',
    'version': '14.0',
    'depends': ['base','account','sale','contacts','project','uom_unece','base_unece','account_tax_unece','base_vat_sanitized','onchange_helper','base_iban','base_bank_from_iban','base_business_document_import','account_invoice_import','base_ubl_payment','account_payment_partner','account_invoice_import_ubl','account_invoice_ubl'],
    "images": ['static/description/icon.png'],
    'data': [
        # 'reports/report_view.xml',
        # 'reports/report.xml',
        'reports/tamhub_reports_view.xml',
        'reports/tamhub_reports.xml',
        'views/account_move.xml',

        # 'views/newxml.xml',


    ],
    'demo': [
    ],
    'qweb': [
        # 'static/src/scss/style.scss',
        # 'static/src/xml/website_widget.xml',
        # 'static/src/xml/theme_preview.xml',
    ],
    'installable': True,
    'application': True,
}
