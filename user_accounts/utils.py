# from io import BytesIO
# from django.http import HttpResponse
# from django.template.loader import get_template
# from django.conf import settings
# import os
# from django.template.loader import render_to_string
# from weasyprint import HTML
#
#
# def render_to_pdf(template_src, context_dict={}):
#     html_template = render_to_string('invoice_render.html', context_dict)
#     pdf_file = HTML(string=html_template).write_pdf()
#     response = HttpResponse(pdf_file, content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="invoice.pdf"'
#     return response
