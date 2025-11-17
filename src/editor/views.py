from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Document

from weasyprint import HTML, CSS
import tempfile
import os


def document_create(request):
    if request.method == "POST":
        title = request.POST.get("title", "Documento em branco")
        content_html = request.POST.get("content_html", "")
        doc = Document.objects.create(title=title, content_html=content_html)
        return redirect("editor:document_edit", pk=doc.pk)

    return render(request, "editor/document_edit.html", {"document": None})


def document_edit(request, pk):
    doc = get_object_or_404(Document, pk=pk)

    if request.method == "POST":
        doc.title = request.POST.get("title", doc.title)
        doc.content_html = request.POST.get("content_html", "")
        doc.save()
        return redirect("editor:document_edit", pk=doc.pk)

    return render(request, "editor/document_edit.html", {"document": doc})


def document_pdf(request, pk):
    doc = get_object_or_404(Document, pk=pk)

    html_string = render_to_string(
        "editor/document_pdf.html",
        {
            "document": doc,
        },
    )

    base_url = request.build_absolute_uri("/")

    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_file = os.path.join(tmpdir, "documento.pdf")
        HTML(string=html_string, base_url=base_url).write_pdf(
            pdf_file,
            stylesheets=[
                CSS(
                    string="""
                    @page {
                        size: A4;
                        margin: 2cm;
                    }
                    body {
                        font-family: 'Calibri', system-ui, -apple-system, sans-serif;
                        font-size: 12pt;
                    }
                    h1 {
                        font-size: 20pt;
                        margin-bottom: 0.5em;
                    }
                    h2 {
                        font-size: 16pt;
                        margin-bottom: 0.4em;
                    }
                    p {
                        margin: 0 0 0.4em 0;
                        line-height: 1.4;
                    }
                    """
                )
            ],
        )

        with open(pdf_file, "rb") as f:
            pdf_data = f.read()

    response = HttpResponse(pdf_data, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{doc.title}.pdf"'
    return response


def document_list(request):
    docs = Document.objects.all()
    return render(request, "editor/document_list.html", {"docs": docs})

