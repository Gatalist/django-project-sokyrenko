from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from .models import Sculpture, ImageHome, News, Author, Development
from .forms import ReviewForm, NewOrderForm


def massage_email(massages, theme):
    # create message object instance
    msg = MIMEMultipart()
    message = massages

    # setup the parameters of the message
    password = "234ft0ph8isoargt234AS-09sd"
    msg['From'] = "quality.figures.shop@gmail.com"
    msg['To'] = "kostencko.alexander2012@gmail.com"
    msg['Subject'] = theme

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    print("successfully sent email to %s:" % (msg['To']))


class IndexView(ListView):
    """главная"""
    model = ImageHome
    queryset = ImageHome.objects.filter(draft=False)
    template_name = "sculptures/index.html"


class AboutView(ListView):
    """О нас"""
    model = Author
    queryset = Author.objects.all()
    template_name = "sculptures/about.html"


class NewsView(ListView):
    """Новости"""
    model = News
    queryset = model.objects.filter(draft=False).order_by('-year')
    template_name = "sculptures/news.html"


class SculptureView(ListView):
    """список скульптур"""
    model = Sculpture
    queryset = Sculpture.objects.filter(draft=False, category__url='sculpture')
    template_name = "sculptures/sculpture_list.html"


class PortalView(ListView):
    """список порталов"""
    model = Sculpture
    queryset = Sculpture.objects.filter(draft=False, category__url='portals')
    template_name = "sculptures/portals_list.html"


class SculptureDetailView(DetailView):
    """полное описание скульптуры"""
    model = Sculpture
    slug_field = "url"
    template_name = "sculptures/sculpture_detail.html"


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        sculpture = Sculpture.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.sculpture = sculpture
            form.save()

        message = """
        ┏─══─━══─⊱ <:─══──:> ⊰─══━─══─┓
                    %s
        ┗─══─━══─⊱ <:─══──:> ⊰─══━─══─┛
        
        ╔═════════════════════════════╗
        ║ Имя: ➳ %s
        ║ ────────────────────────────
        ║ Email: ➳ %s
        ║ ────────────────────────────
        ║ Сообщение: ⤵
        ║ ────────────────────────────
        ║ ✎ %s
        ╚═════════════════════════════╝
                   """ % (sculpture.title, form.name, form.email, form.text)

        theme = "Отзыв на сайте"
        massage_email(message, theme)

        return redirect(sculpture.get_absolute_url())


class DevSculptureView(ListView):
    """список скульптур | мастервкая"""
    model = Development
    queryset = Development.objects.filter(draft=False, category__url='free_sculpture')
    template_name = "sculptures/dev_sculpture_list.html"


class DevSculptureDetailView(DetailView):
    """полное описание скульптуры | мастервкая"""
    model = Development
    slug_field = "url"
    template_name = "sculptures/dev_sculpture_detail.html"


class DevPortalView(ListView):
    """список скульптур | мастервкая"""
    model = Development
    queryset = Development.objects.filter(draft=False, category__url='free_portals')
    template_name = "sculptures/dev_portal_list.html"


class PaySculptureView(View):
    def get(self, request, slug):
        sculpture = Sculpture.objects.get(url=slug)
        return render(request, "sculptures/pay_sculpture.html", {"sculpture": sculpture})


class NewOrder(View):
    """заказ"""
    def post(self, request, pk):
        form = NewOrderForm(request.POST)
        sculpture = Sculpture.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.sculpture = sculpture
            form.save()

            message = """     
            ┏─══─━══─⊱ <:─══──:> ⊰─══━─══─┓
                        %s
            ┗─══─━══─⊱ <:─══──:> ⊰─══━─══─┛  
    
            ╔═════════════════════════════╗
            ║ Имя: ➳ %s
            ║ ────────────────────────────
            ║ Фамилия: ➳ %s
            ║ ────────────────────────────
            ║ Телефон: ➳ %s
            ║ ────────────────────────────
            ║ Email: ➳ %s
            ║ ────────────────────────────
            ║ Сообщение: ⤵ 
            ║ ────────────────────────────
            ║ %s
            ╚═════════════════════════════╝
            
                      """ % (sculpture.title, form.first_name, form.last_name, form.phone, form.email, form.text)

            theme = "•——◤✧Заказ на сайте✧◥——•"
            massage_email(message, theme)

        return render(request, "sculptures/successfully.html", {"sculpture": sculpture})
