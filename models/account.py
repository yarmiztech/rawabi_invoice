from odoo import fields, models,api,_

from uuid import uuid4
import qrcode
import base64
import logging

from lxml import etree



class AccountMove(models.Model):
    _inherit = "account.move"

    po_number = fields.Char('PO No')



    def print_einvoice(self):
        return self.env.ref('rawabi_invoice.rawabi_invoice_report').sudo().report_action(self)


    def total_amount_to_words_tamhub(self):
        for invoice in self:
            # amount_total_words = invoice.currency_id.amount_to_text(invoice.amount_total)
            amount_total_words = invoice.currency_id.amount_to_text(invoice.amount_total)
            return amount_total_words

    def total_amount_to_words_tamhub_arabic(self):
        for invoice in self:
            # amount_total_words = invoice.currency_id.amount_to_text(invoice.amount_total)
            amount_total_words = invoice.currency_id.amount_to_text(invoice.amount_total)
            # inv_name_arabic = GoogleTranslator(source='auto', target='ar').translate(name[:3])
            # amount_arabic = GoogleTranslator(source='auto', target='ar').translate(amount_total_words)
            amount_arabic = "jfhftghfjfgjfg"
            return amount_arabic


    def total_tax(self):
        for invoice in self:
            # print(invoice.amount_total)
            total_tax = invoice.amount_untaxed * 0.15
            return total_tax


    def computear_holdername(self):
        if self.partner_bank_id.id:
            # translated = GoogleTranslator(source='auto', target='ar').translate(self.partner_bank_id.acc_holder_name)
            translated = "dvfdsdfgdfgdfg"
            # self.ar_acount_holder_name = translated
            return translated


    @api.onchange('partner_bank_id')
    def computear_bankname(self):
        if self.partner_bank_id.bank_id.id:
            # translated = GoogleTranslator(source='auto', target='ar').translate(self.partner_bank_id.bank_id.name)
            translated ="kjbdfjdsfjdsj"
            # self.ar_bank_name = translated
            return translated


    @api.onchange('partner_bank_id')
    def computear_bankcode(self):
        if self.partner_bank_id.bank_id.id:
            # translated = GoogleTranslator(source='auto', target='ar').translate(self.partner_bank_id.bank_id.code)
            translated = "sfsdfds"
            # self.ar_bank_code = translated
            return translated

    def amount_words(self):
        amount_total_words = self.currency_id.amount_to_text(self.amount_total)
        # return self.currency_id.amount_to_text(self.amount_total)
        return amount_total_words

    def _ubl_add_attachments(self, parent_node, ns, version="2.1"):
        self.ensure_one()
        self.billing_refence(parent_node, ns, version="2.1")
        # if self.decoded_data:
        self.testing()
        self.qr_code(parent_node, ns, version="2.1")
        self.qr_1code(parent_node, ns, version="2.1")
        self.pih_code(parent_node, ns, version="2.1")

        # self.signature_refence(parent_node, ns, version="2.1")
        # if self.company_id.embed_pdf_in_ubl_xml_invoice and not self.env.context.get(
        #     "no_embedded_pdf"
        # ):
        # self.signature_refence(parent_node, ns, version="2.1")
        filename = "Invoice-" + self.name + ".pdf"
        docu_reference = etree.SubElement(
            parent_node, ns["cac"] + "AdditionalDocumentReference"
        )
        docu_reference_id = etree.SubElement(docu_reference, ns["cbc"] + "ID")
        docu_reference_id.text = filename
        attach_node = etree.SubElement(docu_reference, ns["cac"] + "Attachment")
        binary_node = etree.SubElement(
            attach_node,
            ns["cbc"] + "EmbeddedDocumentBinaryObject",
            mimeCode="application/pdf",
            filename=filename,
        )
        ctx = dict()
        ctx["no_embedded_ubl_xml"] = True
        ctx["force_report_rendering"] = True
        # pdf_inv = (
        #     self.with_context(ctx)
        #     .env.ref("account.account_invoices")
        #     ._render_qweb_pdf(self.ids)[0]
        # )
        ########changed########################
        pdf_inv = self.with_context(ctx).env.ref(
            'account_invoice_ubl.account_invoices_1')._render_qweb_pdf(self.ids)[0]
        pdf_inv = self.with_context(ctx).env.ref(
            'account_invoice_ubl.account_invoices_b2b')._render_qweb_pdf(self.ids)[0]
        pdf_inv = self.with_context(ctx).env.ref(
            'account_invoice_ubl.account_invoices_b2b_credit')._render_qweb_pdf(self.ids)[0]
        # pdf_inv = self.with_context(ctx).env.ref(
        #     'account_invoice_ubl.account_invoices_b2b_debit')._render_qweb_pdf(self.ids)[0]
        pdf_inv = self.with_context(ctx).env.ref(
            'account_invoice_ubl.account_invoices_b2c')._render_qweb_pdf(self.ids)[0]
        pdf_inv = self.with_context(ctx).env.ref(
                    'account_invoice_ubl.account_invoices_b2c_credit')._render_qweb_pdf(self.ids)[0]
        # +++++++++++++++++++++++++++++++OUR CUSTOMES ADD HERE+++++++++++++++++++++++++++++++++++++
        # pdf_inv = self.with_context(ctx).env.ref(
        #     'tam.tam_invoice_report')._render_qweb_pdf(self.ids)[0]
        pdf_inv = self.with_context(ctx).env.ref(
            'rawabi_invoice.rawabi_invoice_report')._render_qweb_pdf(self.ids)[0]

       # -----------------------------aboveeeeeeee---------------------------------

        binary_node.text = base64.b64encode(pdf_inv)
        # self.qr3_code(parent_node, ns, version="2.1")


        # filename = "ICV"
        # icv_reference = etree.SubElement(
        #     parent_node, ns["cac"] + "AdditionalDocumentReference"
        # )
        # icv_reference_id = etree.SubElement(icv_reference, ns["cbc"] + "ID")
        # icv_reference_id.text = filename
        # icv_reference_node = etree.SubElement(icv_reference, ns["cac"] + "UUID")
        # icv_reference_node.text = self.name

    @api.model
    def _get_invoice_report_names(self):
        return [
            "account.report_invoice",
            "account.report_invoice_with_payments",
            "account_invoice_ubl.report_invoice_1",
            "account_invoice_ubl.report_invoice_b2b",
            "account_invoice_ubl.report_invoice_b2b_credit",
            # "account_invoice_ubl.report_invoice_b2b_debit",
            "account_invoice_ubl.report_invoice_b2c",
            "account_invoice_ubl.report_invoice_b2c_credit",
            # "account_invoice_ubl.report_invoice_b2c_debit",
            # "tam.invoice_format_view2",
            "rawabi_invoice.rawabi_invoice_view",

        ]
class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"


    @classmethod
    def _get_invoice_reports_ubl(cls):
        return [
            "account.report_invoice",
            'account_invoice_ubl.report_invoice_1',
            'account_invoice_ubl.report_invoice_b2b',
            'account_invoice_ubl.report_invoice_b2b_credit',
            'account_invoice_ubl.report_invoice_b2b_debit',
            'account_invoice_ubl.report_invoice_b2c',
            'account_invoice_ubl.report_invoice_b2c_credit',
            'account_invoice_ubl.report_invoice_b2c_debit',
            "account.report_invoice_with_payments",
            "account.account_invoice_report_duplicate_main",
            # "tam.invoice_format_view2",
            "rawabi_invoice.rawabi_invoice_view",
        ]


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"




    def tax_amount_value(self):
        # tax_amount = self.price_subtotal * 0.15
        amount_tax = 0
        if self.tax_ids:
            tax_amount = self.env['account.tax'].search([('name','=',self.tax_ids.name)])
            for tax in tax_amount:
                amount_tax = self.price_subtotal * tax.amount/100
        return amount_tax

    def total_including_tax(self):
        total_including_tax = 0
        tax_amount = self.env['account.tax'].search([('name', '=', self.tax_ids.name)])
        for tax in tax_amount:
            amount_tax = self.price_subtotal * tax.amount / 100
            total_including_tax = amount_tax + self.price_subtotal
        return total_including_tax

    def tax_rate(self):
        amount=0
        for line in self.tax_ids:
            amount=amount+line.amount
            return amount


    def tax_amount(self):
        # taxamount=0
        amount = 0
        for line in self.tax_ids:
            amount = amount + line.amount
        # for x in self.invoice_line_ids:
            tax=self.price_subtotal /100 * amount
            return tax


    def total_including(self):
        amount = 0
        for line in self.tax_ids:
            amount = amount + line.amount
            # for x in self.invoice_line_ids:
            tax = self.price_subtotal / 100 * amount
            total=tax+ self.price_subtotal
            return total



class  ResPartner(models.Model):
    _inherit = 'res.partner'

    bill_to = fields.Char('Bill To')







