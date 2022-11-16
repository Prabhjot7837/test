from django.shortcuts import render
import os
import mimetypes
from reportlab.graphics.charts.barcharts import VerticalBarChart
import os
import matplotlib.pyplot as plt
from django.http.response import HttpResponse
from .models import Potholedata,Pothole_density
from django.shortcuts import render
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.graphics.shapes import Drawing
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter

def home(request):
    return render(request,'home.html')

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Image
from reportlab.lib.pagesizes import letter, inch

def download_file(request):
    file_name = "Report.pdf"
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    # container for the 'Flowable' objects
    elements = []
    m = Potholedata.objects.get(id=1)
    # table
    data= [['Data',''],
        ['Address',m.Address ],
    ['Road_condition',m.Road_condition ],
    ['Killometers covered',m.kms_covered],
    ['Anomalies_detetcted',m.anomalies_detected],
    ['Pothole',m.pothole],
    ['Cracks',m.cracks],
    ['patches',m.patches]]
    t=Table(data)
    t=Table(data,2*[3.3*inch], 8*[0.5*inch],hAlign='LEFT')
    t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
    ('ALIGN',(0,0),(0,-1),'CENTER'),
    ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
    ('SPAN',(0,0),(-1,0)),
    ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
    ('TEXTCOLOR',(0,-1),(0,-1),colors.blue),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    elements.append(t)
    # pie chart
    d = Drawing(350, 340)
    pc = Pie()
    pc.x = 100
    pc.y = 50
    pc.width = 200
    pc.height = 200
    pc.data = [m.pothole,m.cracks,m.patches]
    pc.labels = ['pothole','cracks','patches']
    d.add(pc)
    elements.append(d)
    # bar graph
    dobj = Pothole_density.objects.get(id =1)
    potholes = ['0-500', '500-1000', '1000-1500',
                                    '1500-2000', '2000-2500']
    km_covered = [dobj.p500,dobj.p1000,dobj.p1500,dobj.p2000,dobj.p2500]

    # colour = ['green', 'blue', 'purple', 'brown', 'teal']
    plt.bar(potholes, km_covered)
    plt.title('Pothole/Patch density in 500 meters', fontsize=14)
    plt.xlabel('km Covered', fontsize=14)
    plt.ylabel('no. of potholes', fontsize=14)
    plt.savefig('my_plot.png')
    elements.append(Image('my_plot.png',300,300))
    doc.build(elements)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(BASE_DIR)
    # Define the full file path
    filepath = os.path.join(BASE_DIR + '\Report.pdf')
    print(filepath)
    # d.save(formats=[filepath], outDir='.', fnRoot='test-pie')
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % file_name
    # Return the response value
    return response
    


