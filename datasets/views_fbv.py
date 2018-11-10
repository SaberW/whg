# datasets.views FUNCTION-BASED

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
import django.core.files.uploadedfile as upfile
from django.utils.html import escape
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
import codecs, tempfile, os
from pprint import pprint

from .tasks import read_csv, read_lpf
from .forms import DatasetModelForm
from .models import Dataset
from main.models import *

# list datasets per user
def dashboard(request):
    dataset_list = Dataset.objects.filter(owner=request.user.id).order_by('-upload_date')
    print('dataset_list',dataset_list)
    return render(request, 'datasets/dashboard.html', {'datasets':dataset_list})

# display dataset in editable grid
def ds_grid(request, label):
    print('request, pk',request, label)
    ds = get_object_or_404(Dataset, label=label)
    place_list = Place.objects.filter(dataset=label).order_by('title')

    return render(request, 'datasets/ds_grid.html', {'ds':ds, 'place_list': place_list})

# new dataset: upload file, store if valid
def ds_new(request, template_name='datasets/ds_form.html'):
    form = DatasetModelForm(request.POST, request.FILES)
    context = {
        'form':form, 'action': 'new'
    }
    def removekey(d, key):
        r = dict(d)
        del r[key]
        return r

    if request.method == 'POST':
        if form.is_valid():
            context['action'] = 'upload'
            print('form is valid')
            print('cleaned_data', form.cleaned_data)

            # open & write tempf to a temp location;
            # call it tempfn for reference
            tempf, tempfn = tempfile.mkstemp()
            try:
                for chunk in request.FILES['file'].chunks():
                    os.write(tempf, chunk)
            except:
                raise Exception("Problem with the input file %s" % request.FILES['file'])
            finally:
                os.close(tempf)

            # open temp file
            fin = codecs.open(tempfn, 'r', 'utf8')
            # send for format validation
            if form.cleaned_data['format'] == 'csv':
                result = read_csv(fin,request.user.username)
            elif form.cleaned_data['format'] == 'lpf':
                result = read_lpf(fin,request.user.username)
            # print('cleaned_data',form.cleaned_data)
            fin.close()

            # add status
            if len(result['errors']) == 0:
                context['status'] = 'format_ok'
                form.cleaned_data['status'] = 'format_ok'
                form.save()
            else:
                context['status'] = 'format_error'
                print('result:', result)

            context['result'] = result
            # return redirect('/datasets/dashboard')
        else:
            print('not valid', form.errors)
            context['errors'] = form.errors
        print('context',context)
    return render(request, template_name, context=context)

# insert LP-compatible records from csv file to database
def ds_insert(request, pk ):
    # retrieve just-added record then db insert
    import os, csv, codecs,json
    dataset = get_object_or_404(Dataset, id=pk)
    context = {'status': 'inserting'}

    infile = dataset.file.open(mode="r")
    dialect = csv.Sniffer().sniff(infile.read(1024),['\t',';','|'])
    reader = csv.reader(infile, dialect)
    infile.seek(0)
    header = next(reader, None)
    print('header', header)

    objs = {"PlaceName":[], "PlaceType":[], "PlaceGeom":[], "PlaceWhen":[],
        "PlaceLink":[], "PlaceRelated":[], "PlaceDescription":[],
        "PlaceDepiction":[]}

    # id*, name*, name_src*, type^, variants[], ccode[]^, lon^, lat^, geom_src, close_match[]^, exact_match[]^, description, depiction
    #
    # TODO: what if simultaneous inserts?
    countrows=0
    countlinked = 0
    countlinks = 0
    # for r in reader:
    for i, r in zip(range(200), reader):
        # ABANDONED place.placeid ## poll Place.objects.placeid.max()
        # nextpid = (Place.objects.all().aggregate(models.Max('id'))['id__max'] or 0) + 1
            # if Place.objects.all().count() > 0 else 10000001

        # TODO: should columns be required even if blank?
        # required
        src_id = r[header.index('id')]
        title = r[header.index('name')]
        name_src = r[header.index('name_src')]
        # encouraged for reconciliation
        type = r[header.index('type')] if 'type' in header else 'unk.'
        aat_type = r[header.index('aat_type')] if 'aat_type' in header else ''
        ccode = r[header.index('ccode')] if 'ccode' in header else 'unk.'
        coords = [float(r[header.index('lon')]), float(r[header.index('lat')])]
        close_match = r[header.index('close_match')][2:-2].split('", "') if 'close_match' in header else []
        exact_match = r[header.index('exact_match')][1:-1] \
            if 'exact_match' in header else []
        # nice to have
        description = r[header.index('description')] \
            if 'description' in header else []
        depiction = r[header.index('depiction')] \
            if 'depiction' in header else []

        # build and save Place object
        newpl = Place(
            # placeid = nextpid,
            src_id = src_id,
            dataset = dataset,
            title = title,
            ccode = ccode
        )
        newpl.save()
        countrows += 1
        # build associated objects and add to arrays

        # PlaceName()
        objs['PlaceName'].append(PlaceName(place_id=newpl,
            # src_id = src_id,
            # dataset = dataset,
            toponym = title,
            # TODO get citation label through name_src FK; here?
            json={"toponym": title, "citation": {"id":name_src,"label":""}}
        ))
        # TODO: variants array

        # PlaceType()
        objs['PlaceType'].append(PlaceType(place_id=newpl,
            json={"src_label": type, "label":aat_type}
        ))

        # PlaceGeom()
        objs['PlaceGeom'].append(PlaceGeom(place_id=newpl,
            # src_id = src_id,
            # dataset = dataset,
            json={"type": "Point", "coordinates": coords,
                "geowkt": 'POINT('+str(coords[0])+' '+str(coords[1])+')'}
        ))

        # # PlaceLink()
        if len(list(filter(None,close_match))) > 0:
            countlinked += 1
            # print('close_match',close_match)
            for m in close_match:
                countlinks += 1
                objs['PlaceLink'].append(PlaceLink(place_id=newpl,
                    # src_id = src_id,
                    # dataset = dataset,
                    json={"type":"closeMatch", "identifier":m}
                ))

        #
        # # PlaceWhen()
        # objs['PlaceWhen'].append(PlaceWhen())
        #
        # # PlaceRelated()
        # objs['PlaceRelated'].append(PlaceRelated())
        #
        # # PlaceDescription()
        # objs['PlaceDescription'].append(PlaceDescription())
        #
        # # PlaceDepiction()
        # objs['PlaceDepiction'].append(PlaceDepiction())

        # print('new place:', newpl)

    # bulk_create(Class, batchsize=n) for each
    PlaceName.objects.bulk_create(objs['PlaceName'])
    PlaceType.objects.bulk_create(objs['PlaceType'])
    PlaceGeom.objects.bulk_create(objs['PlaceGeom'])
    PlaceLink.objects.bulk_create(objs['PlaceLink'])

    context['status'] = 'inserted'
    print('rows,linked,links:',countrows,countlinked,countlinks)
    dataset.numrows = countrows
    dataset.numlinked = countlinked
    dataset.total_links = countlinks
    dataset.header = header
    dataset.status = 'inserted'
    dataset.save()
    print('record:', dataset.__dict__)
    print('context:',context)
    infile.close()
    # dataset.file.close()

    return redirect('/datasets/dashboard', context=context)

def ds_update(request, pk, template_name='datasets/ds_form.html'):
    record = get_object_or_404(Dataset, pk=pk)
    form = DatasetModelForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('/datasets/dashboard')
    else:
        print('not valid', form.errors)
    return render(request, template_name, {'form':form, 'action': 'update'})

def ds_delete(request, pk):
    record = get_object_or_404(Dataset, pk=pk)
    # print('request, pk',request, pk)
    # print('record',type(record))
    # it's a GET not POST
    record.delete()
    return redirect('dashboard')

# initiate, monitor reconciliation service
def ds_recon(request, pk):
    ds = get_object_or_404(Dataset, id=pk)
    print('request, method:',request, request.method)
    context = {
        "dataset": ds.name,
    }

    if request.method == 'GET':
        print('context',context)
    elif request.method == 'POST' and request.POST:
        authority = request.POST['recon']
        dataset = request.POST['ds']
        pprint(request.POST)
        # run task
        context['response'] = 'ran something'
        context['dataset'] = ds.label
        context['authority'] = authority
        context['hits'] = '?? not wired yet'
        context['result'] = 'completed'
        return render(request, 'datasets/ds_recon.html', {'ds':ds, 'context': context})

    return render(request, 'datasets/ds_recon.html', {'ds':ds})