import csv
import datetime
import logging
from typing import Union
from io import StringIO

from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.shortcuts import render
from django.template import Template, RequestContext
from django.views.decorators.csrf import csrf_exempt

from .models import Horse
from .forms import UploadFileForm


def clean_null(input_str: str) -> Union[str, None]:
    """When uploading from a file (DB dump), remove NULL values"""
    if input_str == 'NULL':
        return None
    else:
        return input_str


def parse_date(input_date: str) -> datetime.date:
    """1/15/20"""
    try:
        date = datetime.datetime.strptime(input_date, '%m/%d/%y').date()
        return date
    except Exception as e:
        date = datetime.datetime.strptime(input_date, '%m/%d/%Y').date()
        return date
    except Exception as e:
        print(e)


class UploadHorsesSuccessHandler(View):

    def get(self, request):
        html = """<html><head></head><body>
                    <h4><a href="{% url 'admin:index' %}">Admin</a></h4>
    
                    <p>imported {{new_horses}} horses</p>
                    </body>
                """
        new_horses = request.GET.get('new_horses', '')
        t = Template(html)
        c = RequestContext(request, {'new_horses': new_horses})
        html = t.render(c)
        return HttpResponse(html)


class UploadHorsesHandler(View):
    column_names = [
        "Type", "Name", "Sex", "DateofBirth", "Starts", "DateLastStart",
        "Country", "TFReg", "RaceRating", "Active", "Elite", "Status", "OptimalDistance", "Distance1", "Distance2",
        "Size1", "Class1", "Class2", "Class3", "Sire", "Dam", "Broodmare Sire"
    ]

    def get(self, request):
        form = UploadFileForm()
        post_url = reverse('upload-horses')
        upload_type = 'Horses'
        column_names = str(self.column_names)
        return render(request, 'velox_app/upload_file.html', context={'form': form, 'post_url': post_url,
                                                                      'column_names': column_names,
                                                                      'upload_type': upload_type})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            content = uploaded_file.read().decode()
            f = StringIO(content)
            f.seek(0)
            csv_reader = csv.DictReader(f)
            headers = csv_reader.fieldnames
            bad_column_names = list(set(headers).difference(set(self.column_names)))
            bad_column_names = list(set(self.column_names).difference(set(headers)))
            if bad_column_names:
                return HttpResponse(
                    f"These columns are not matching/expected: <b>{bad_column_names}</b> </br>Check if you have these columns in input file since their are mandatory.")
            new_horses = 0
            for line in csv_reader:
                type = line['Type']
                name = line['Name']
                sex = line['Sex']
                date_of_birth = line['DateofBirth']
                if date_of_birth:
                    date_of_birth = parse_date(date_of_birth)
                else:
                    date_of_birth = None
                starts = line['Starts']
                if starts:
                    starts = int(starts)
                else:
                    starts = None
                date_last_start = line['DateLastStart']
                if date_last_start:
                    date_last_start = parse_date(date_last_start)
                else:
                    date_last_start = None
                country = line['Country']
                tf_reg = line['TFReg']
                if tf_reg == "":
                    tf_reg = None
                race_rating = line['RaceRating']
                if race_rating:
                    race_rating = int(race_rating)
                else:
                    race_rating = None
                active = line['Active']
                if not active:
                    active = 'No'
                elite = line['Elite']
                if not elite:
                    elite = 'No'
                status = line['Status']
                if not status:
                    status = 'Unnamed'
                optimal_distance = clean_null(line['OptimalDistance'])
                distance1 = clean_null(line['Distance1'])
                distance2 = clean_null(line['Distance2'])
                size1 = clean_null(line['Size1'])
                class1 = clean_null(line['Class1'])
                class2 = clean_null(line['Class2'])
                class3 = clean_null(line['Class3'])
                dam = clean_null(line['Dam'])
                sire = clean_null(line['Sire'])
                broodmare_sire = clean_null(line['Broodmare Sire'])

                existing_horses = Horse.objects.filter(name=name, date_of_birth=date_of_birth).all()
                if existing_horses:
                    logging.info(f'skipping horse {name} {date_of_birth}')
                else:
                    horse = Horse.objects.create(name=name, type=type, sex=sex, date_of_birth=date_of_birth,
                                                 starts=starts,
                                                 date_last_start=date_last_start, country=country, tf_reg=tf_reg,
                                                 race_rating=race_rating, active=active, elite=elite, status=status,
                                                 optimal_distance=optimal_distance, distance1=distance1,
                                                 distance2=distance2,
                                                 size1=size1, class1=class1, class2=class2, class3=class3,
                                                 dam=dam, sire=sire, broodmare_sire=broodmare_sire
                                                 )
                    new_horses += 1
            redirect_url = '{}?new_horses={}'.format(reverse('upload-horses-success'), new_horses)
            return HttpResponseRedirect(redirect_url)

        return HttpResponse("Form is not valid, you probably need to include file to upload")
