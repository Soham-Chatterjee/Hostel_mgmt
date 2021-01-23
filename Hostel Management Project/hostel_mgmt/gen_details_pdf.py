from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.platypus.paragraph import Paragraph
import os


def gen_details_pdf(filename, heading, records):
    """
    Heading:
    student = id, name, cid, rid, contact
    block = id, type, gender, num_rooms, vacant
    room = id, bid, type, no_of_beds, occuoants
    staff = id, name, gender, dob, contact
    mess = mid
    """
    data = []
    data.append(heading)
    data.extend(records)
    
    
    filename += '.pdf'
    filedir = os.getcwd()
    directory = "details"
    outfilepath = os.path.join(filedir, directory, filename)

    pdf = SimpleDocTemplate(
        outfilepath,
        pagesize=A4
    )

    table = Table(data)

    # add style
    
    style = TableStyle([
        ('BACKGROUND', (0,0), (5,0), colors.gray),

        ('ALIGN',(0,0),(-1,-1),'CENTER'),

        ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 11),

        ('BOTTOMPADDING', (0,0), (-1,0), 12),

    ])
    table.setStyle(style)

    #Add borders
    ts = TableStyle(
        [
        ('BOX',(0,0),(-1,-1),1,colors.black),


        ('GRID',(0,1),(-1,-1),1,colors.black),
        ]
    )
    table.setStyle(ts)

    elems = []
    elems.append(table)

    pdf.build(elems)

    

    