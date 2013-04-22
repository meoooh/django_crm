# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.views.generic import TodayArchiveView, DayArchiveView, MonthArchiveView, YearArchiveView, ListView, DetailView
from django.contrib.auth.views import login
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from crm.forms import *
from crm.models import *
from django.core.urlresolvers import reverse
from crm.utility import *
from django.utils.decorators import method_decorator


def logging(request):
    print request.META['REMOTE_ADDR'], request.META['HTTP_USER_AGENT']

    return


@login_required
def mainPage(request):
    variables = RequestContext(request, {
        'user': request.user,
    })

    return render_to_response('mainPage.html', variables)


def userRegistration(request):
#    if request.user.is_authenticated(): #로그인 여부 검사
#        return HttpResponseRedirect('/')
#로그인 중에도 회원가입 가능하게 해야할지...
    if request.method == 'POST':
        form = userRegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
            )
            UserProfile.objects.create(user=user)
            # get_profile관련 https://docs.djangoproject.com/en/dev/topics/auth/customizing/#auth-profiles
            # http://www.turnkeylinux.org/blog/django-profile
            # http://stackoverflow.com/questions/5477925/django-1-3-userprofile-matching-query-does-not-exist
            user = user.get_profile()
#            import pdb
#            pdb.set_trace()
            user.name = form.cleaned_data['name']
            user.mobile = form.cleaned_data['mobile']

            user.save()

            return HttpResponseRedirect('/')
    elif request.method == 'GET':
        form = userRegistrationForm()
    else:
        return HttpResponseRedirect(reverse('userRegistration'))
        # 로깅 할 필요 있음. 구현 후 추가 예정.

    variables = RequestContext(request, {
        'form': form,
    })
    return render_to_response(
        'registration/userRegistration.html',
        variables,
    )


def logoutPage(request):
    logout(request)  # from django.contrib.auth import logout

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    # from django.http import HttpResponseRedirect


def loginPage(request):
    # print request
    # import ipdb;ipdb.set_trace()
    print request.META['REMOTE_ADDR'], request.META['HTTP_USER_AGENT']
    if 'next' in request.GET:
        request.GET['next']
    loginReturnValue = login(request=request)

    if request.method == 'POST' and request.user.is_authenticated():
        user = request.user.get_profile()
        user.lastIp = request.META.get('REMOTE_ADDR')
        user.save()

    return loginReturnValue


@login_required
def workDailyRecord(request, mode_name):
    form = WorkDailyRecordForm()
    if request.method == 'GET':
        if mode_name == u'edit/':
            workDailyRecord = WorkDailyRecord.objects.get(pk=request.GET['pk'])
            target_user = ', '.join(
                w.get_profile().name for w in workDailyRecord.target_user.all()
            )
            form = WorkDailyRecordForm({
                # 'ongoing_or_end':workDailyRecord.ongoing_or_end,
                'contents': workDailyRecord.contents,
                'target_user': target_user,
            })

            variables = RequestContext(request, {
                'form': form,
            })

            return render_to_response('workDailyRecordForm.html', variables)
        elif mode_name is None:
            # import pdb;pdb.set_trace()
            try:
                return TodayLogView.as_view()(request)
            except Http404:
                # workDailyRecord = WorkDailyRecord.objects.filter(ongoing_or_end=date.today)
                pass
            else:
                return render_to_response('test.html')
            workDailyRecord = WorkDailyRecord.objects.order_by('date')

        # import ipdb
        # ipdb.set_trace()
        variables = RequestContext(request, {
            'user': request.user,
            'form': form,
            'workDailyRecord': workDailyRecord,
        })

        return render_to_response('workDailyRecord.html', variables)
    elif request.method == 'POST':
#        import pdb
#        pdb.set_trace()
        #form = WorkDailyRecordForm(request.POST)
        ajax = 'ajax' in request.GET
        if mode_name == u'del/':
            if ajax:
                workDailyRecord = WorkDailyRecord.objects.get(pk=request.POST['pk'])
                workDailyRecord.delete()
                return HttpResponse('1')  # from django.http import HttpResponse
        elif mode_name is None:
            if ajax:
                # import pdb;pdb.set_trace()
                if 'pk' in request.POST:  # 수정
                    if 'edit' in request.GET:
                        workDailyRecord = WorkDailyRecord.objects.get(pk=request.POST['pk'])
                        workDailyRecord.contents = request.POST['contents']
#                        workDailyRecord.ongoing_or_end = request.POST['ongoing_or_end']

                        workDailyRecord.target_user.clear()

                        target_users = request.POST['target_user'].split(',')

                        for target_user in target_users:
                            user = ''
                            target_user = target_user.strip()
                            try:
                                user = UserProfile.objects.get(name=target_user).user
                            except ObjectDoesNotExist:
                                continue
                            workDailyRecord.target_user.add(user)

                        workDailyRecord.save()
                    elif 'check' in request.GET:
                        workDailyRecord = WorkDailyRecord.objects.get(pk=request.POST['pk'])

                        workDailyRecord.check_user.add(request.user)
                        workDailyRecord.save()

                        return HttpResponse('1')
                    elif 'uncheck' in request.GET:
                        workDailyRecord = WorkDailyRecord.objects.get(pk=request.POST['pk'])

                        workDailyRecord.check_user.remove(request.user)
                        workDailyRecord.save()

                        return HttpResponse('1')
                    elif 'ongoing' in request.GET:
#                        import pdb;pdb.set_trace()
                        workDailyRecord = WorkDailyRecord.objects.get(pk=request.POST['pk'])

                        workDailyRecord.ongoing_or_end = u'ing'
                        workDailyRecord.save()

#                        return HttpResponse('1')
                    elif 'end' in request.GET:
#                        import pdb;pdb.set_trace()
                        workDailyRecord = WorkDailyRecord.objects.get(pk=request.POST['pk'])

                        workDailyRecord.ongoing_or_end = u'end'
                        workDailyRecord.save()

#                        return HttpResponse('1')
                else:
                    workDailyRecord = WorkDailyRecord.objects.create(
                        user=request.user,
                        contents=request.POST['contents'],
#                        ongoing_or_end=request.POST['ongoing_or_end'],
                    )

                    target_users = request.POST['target_user'].split(',')

                    for target_user in target_users:
                        user = ''
                        target_user = target_user.strip()
                        try:
                            user = UserProfile.objects.get(name=target_user).user
                        except ObjectDoesNotExist:
                            continue
                        workDailyRecord.target_user.add(user)
                        workDailyRecord.save()

                variables = RequestContext(request, {
                    'form': form,
                    'workDailyRecord': [workDailyRecord],
                })

                return render_to_response('onlyWorkDailyRecord.html', variables)
            else:
                # import ipdb;ipdb.set_trace()
                workDailyRecord = WorkDailyRecord.objects.create(
                    user=request.user,
                    contents=request.POST['contents'],
#                    ongoing_or_end=request.POST['ongoing_or_end'],
                )

                target_users = request.POST['target_user'].split(',')

                for target_user in target_users:
                    user = ''
                    target_user = target_user.strip()
                    try:
                        user = UserProfile.objects.get(name=target_user).user
                    except ObjectDoesNotExist:
                        continue
                    workDailyRecord.target_user.add(user)
                    workDailyRecord.save()

                return HttpResponseRedirect('/workDailyRecord/')


@login_required
def searchUser(request):
    if 'q' in request.GET:
        users = UserProfile.objects.filter(name__istartswith=request.GET['q'])

        return HttpResponse('\n'.join(user.name for user in users))
    return HttpResponse()


class TodayLogView(TodayArchiveView):
    """
    https://gist.github.com/4579130
    http://ccbv.co.uk/projects/Django/1.4/django.views.generic.dates/TodayArchiveView/
    """
    model = WorkDailyRecord  # 임포트 한 모델 클래스 명을 적어 줍니다.
    context_object_name = 'workDailyRecord'  # 템플릿에서 쓸 때 필요합니다.
    date_field = 'date'
#    month_format = '%m' # 달을 숫자[01-12]형태로 표현합니다.
    template_name = "workDailyRecord.html"
#    allow_empty = True

    def get_context_data(self, *args, **kwargs):  # WorkDailyRecordForm()을 template에 전달하기 위해서
        context = super(TodayLogView, self).get_context_data(*args, **kwargs)
        context['form'] = WorkDailyRecordForm()
#        import pdb;pdb.set_trace()
        return context

    # https://docs.djangoproject.com/en/1.4/topics/class-based-views/#decorating-class-based-views
    # @method_decorator(login_required)  # from django.utils.decorators import method_decorator
    # 이 class는 workDailyRecord 함수에서 사용되고, workDailyRecord함수는 login_required 데코레이터에 보호되고 있으므로 여기수 굳이 login_require 처리를 해주지 않아도 된다.
    # def dispatch(self, *args, **kwargs):
    #     return super(TodayLogView, self).dispatch(*args, **kwargs)


class DailyLogView(DayArchiveView):
    model = WorkDailyRecord
    context_object_name = 'workDailyRecord'
    date_field = 'date'
    month_format = '%m'
    template_name = "workDailyRecord.html"
    allow_empty = True

    def get_context_data(self, **kwargs):  # WorkDailyRecordForm()을 template에 전달하기 위해서
        context = super(DayArchiveView, self).get_context_data(**kwargs)
        context['form'] = WorkDailyRecordForm()
#        import pdb;pdb.set_trace()
        return context


class MonthlyLogView(MonthArchiveView):
    model = WorkDailyRecord
    context_object_name = 'workDailyRecord'
    date_field = 'date'
    month_format = '%m'
    template_name = "workDailyRecord.html"
    allow_empty = True

    def get_context_data(self, **kwargs):  # WorkDailyRecordForm()을 template에 전달하기 위해서
        context = super(MonthArchiveView, self).get_context_data(**kwargs)
        context['form'] = WorkDailyRecordForm()
#        import pdb;pdb.set_trace()
        return context


class YearlyLogView(YearArchiveView):
    model = WorkDailyRecord
    context_object_name = 'workDailyRecord'
    date_field = 'date'
    # year_format = '%Y'
    template_name = "workDailyRecord.html"
    # month_format = '%m'
    make_object_list = True  # 중요!!
    # allow_empty = True

    def get_context_data(self, *args, **kwargs):  # WorkDailyRecordForm()을 template에 전달하기 위해서
        context = super(YearArchiveView, self).get_context_data(*args, **kwargs)
        context['form'] = WorkDailyRecordForm()
        # import pdb;pdb.set_trace()
        return context


def customer(request):
    if request.method == "GET":
        form = CustomerRegistrationForm()

    variables = RequestContext(request, {
        'form': form,
    })

    return render_to_response('customer.html', variables)


@login_required
def customerRegistration(request):
    if request.method == "GET":
        form = CustomerRegistrationForm()
    elif request.method == "POST":
        # import pdb;pdb.set_trace()
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            customer = Customer.objects.create(
                name=form.cleaned_data['name'],
                position=form.cleaned_data['position'],
                serviceName=form.cleaned_data['serviceName'],
                detailedServiceName=form.cleaned_data['detailedServiceName'],
                serviceNumber=form.cleaned_data['serviceNumber'],
                dataFolder=form.cleaned_data['dataFolder'],
            )

            personInCharge, created = PersonInCharge.objects.get_or_create(
                name=form.cleaned_data['personInChargesName'],
                telephone1=form.cleaned_data['personInChargesTel'],
                mobile1=form.cleaned_data['personInChargesMobile'],
                email1=form.cleaned_data['personInChargesEmail'],
            )
            customer.personInCharges.add(personInCharge)

            worker = UserProfile.objects.get(name=form.cleaned_data['workers']).user
            customer.workers.add(worker)

            salesperson = UserProfile.objects.get(name=form.cleaned_data['salespersons']).user
            customer.salespersons.add(salesperson)

            for i in form.cleaned_data['ipaddrs'].split(','):
                if ipValidation(i.strip()):
                    for j in iptools.IpRange(i.strip()):
                        ipaddr, created = IPaddr.objects.get_or_create(
                            addr=j,
                        )
#                        ipaddr.country=GeoIP(j)
                        note = Note(
                            content_object=ipaddr,
                            contents=form.cleaned_data['ipaddrsNote'],
                            writer=request.user,
                        )
                        note.save()
                        customer.ipaddrs.add(ipaddr)
                else:
                    # validation 실패시...
                    pass

            for i in form.cleaned_data['domains'].split(','):
                domain, created = Domain.objects.get_or_create(
                    url=i,
                )
                note = Note(
                    content_object=domain,
                    contents=form.cleaned_data['domainsNote'],
                    writer=request.user,
                )
                note.save()
                customer.domains.add(domain)
            if ipValidation(form.cleaned_data['equipmentsIpaddr']):
                ipaddr, created = IPaddr.objects.get_or_create(
                    addr=form.cleaned_data['equipmentsIpaddr'],
                )
                #ipaddr.country=GeoIP(j)
                equipment, created = Equipment.objects.get_or_create(
                    ipaddr=ipaddr
                )
                equipment.type = form.cleaned_data['equipmentsType']
                equipment.save()
                note = Note(
                    content_object=ipaddr,
                    contents=form.cleaned_data['equipmentsNote'],
                    writer=request.user,
                )
                note.save()
                customer.equipments.add(equipment)

            for i in form.cleaned_data['alertEmails'].split(','):
                # import pdb;pdb.set_trace()
                personInCharge, created = PersonInCharge.objects.get_or_create(
                    email1=i,
                )
                if created:
                    personInCharge.name = customer.name+u' 담당자'
                    personInCharge.save()
                customer.alertEmails.add(personInCharge)

            for i in form.cleaned_data['alertSMSs'].split(','):
                personInCharge, created = PersonInCharge.objects.get_or_create(
                    mobile1=i,
                )
                if created:
                    personInCharge.name = customer.name + u' 담당자'
                    personInCharge.save()
                customer.alertSMSs.add(personInCharge)

            note = Note(
                content_object=customer,
                contents=form.cleaned_data['notes'],
                writer=request.user,
            )
            note.save()

            customer.save()
            return HttpResponseRedirect(reverse('customer'))  # from django.core.urlresolvers import reverse

    variables = RequestContext(request, {
        'form': form,
    })

    return render_to_response('customerRegistration.html', variables)


class customerList(ListView):
    model = Customer
    context_object_name = 'customerList'
    template_name = "customer.html"
    allow_empty = True


class customerDetailView(DetailView):
    context_object_name = 'customerDetail'
    template_name = "customerDetail.html"
    allow_empty = True
    model = Customer
    #queryset = Customer.objects.order_by('note__date') # 실패했음...
    slug_field = 'name'

    def get_context_data(self, **kwargs):
    # WorkDailyRecordForm()을 template에 전달하기 위해서
        context = super(DetailView, self).get_context_data(**kwargs)
        context['form'] = CustomerRegistrationForm()
        # import pdb;pdb.set_trace()
        return context


def addCustomerNotes(request, slug):
    if request.method == "POST":
        if 'ajax' in request.GET:
            try:
                customer = Customer.objects.get(name=slug)
            except ObjectDoesNotExist:
                return HttpResponse(u'등록되지 않은 고객.')
            else:
                note = Note(
                    content_object=customer,
                    contents=request.POST['notes'],
                    writer=request.user,
                )
                note.save()
                # import ipdb;ipdb.set_trace()
                return HttpResponse(simplejson.dumps(note.to_dict()), content_type="application/json")
    else:
        return HttpResponse('addCustomerNotes: Other methods is denied.')


def actionCustomerNote(request, slug, pk):
    # import ipdb;ipdb.set_trace()
    if request.is_ajax():
        content_type = ContentType.objects.get_for_model(Customer)
        try:
            note = Note.objects.get(content_type=content_type, pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse(u'등록되지 않은 메모.')

        if request.method == "DELETE":
            note.delete()

            return HttpResponse(u'1')
        elif request.method == "PUT":
            # import ipdb;ipdb.set_trace()
            key, value = request.raw_post_data.split("=")

            if key == "contents":
                import urllib
                note.contents = urllib.unquote(value).replace("+", " ")
                # 뭔가 깔끔하게 해결할수있는 방법이 있을꺼 같다... 찾아봐야지...
                note.save()
            else:
                return HttpResponse(
                    'actionCustomerNote: Other key is denied.',
                )
            return HttpResponse(u'1')
        elif request.method == "GET":
            return HttpResponse(
                simplejson.dumps({"contents": note.contents}),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                'actionCustomerNote: Other methods is denied.',
            )
    else:
        return HttpResponse('actionCustomerNote: Not ajax is denied.')


def actionCustomerIPaddrs(request, slug, pk):
    if request.is_ajax():
        supportREST(request)
        try:
            customer = Customer.objects.get(name=slug)
        except ObjectDoesNotExist:
            return HttpResponse(u'등록되지 않은 고객.', status=500)
        else:
            if request.method == "POST":
                jsonContext = []
                # import ipdb;ipdb.set_trace()
                requestPOST = request.POST.copy()
                requestPOST['ip'] = request.POST['ip'].replace(' ', '')

                try:
                    for i in ipValidation(requestPOST['ip']):
                        try:
                            # import ipdb;ipdb.set_trace()
                            ip, created = IPaddr.objects.get_or_create(
                                addr=i,
                            )
                        except:
                            return HttpResponse('0')
                        else:
                            Note.objects.create(
                                contents=request.POST['note'],
                                writer=request.user,
                                content_object=ip,
                            )
                            customer.ipaddrs.add(ip)

                            jsonContext.append({"addr": i, "pk": ip.pk})
                    return HttpResponse(simplejson.dumps(jsonContext), content_type="application/json")
                except:
                    return HttpResponse('0')
            elif request.method == "DELETE":
                try:
                    ip = IPaddr.objects.get(pk=pk)
                except ObjectDoesNotExist:
                    return HttpResponse(u'등록되지 않은 IP.', status=500)
                else:
                    try:
                        # import ipdb;ipdb.set_trace()
                        customer.ipaddrs.remove(ip)
                    except:
                        printException(sys.exc_info())
                        return HttpResponse(u'remove() 실패.', status=500)
                    else:
                        Note.objects.create(
                            contents=u"%s 고객사에서 제거됨." % slug,
                            writer=request.user,
                            content_object=ip
                        )
                        return HttpResponse(u'1')
            else:
                return HttpResponse('addCustomerIP: Other methods is denied.')
            #end if
        #end else
    #end if
    else:
        return HttpResponse('addCustomerIP: Not ajax is denied.')

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def listing(request, slug, kind, page):
    customer = Customer.objects.get(name=slug)
    contact_list = getattr(customer, kind).all()
    htmlPage = "listNext.html"

    # import ipdb;ipdb.set_trace()

    if 'dsc' in request.GET and request.GET['dsc']:
        if 'dsc' in request.GET:
            contact_list = contact_list.order_by("-" + request.GET['col'])
        else:
            contact_list = contact_list.order_by(request.GET['col'])

    paginator = Paginator(contact_list, 5)  # Show 5 contacts per page

    if 'last' in request.GET and request.GET['last'] == "last":
        page = page or paginator.num_pages
        htmlPage = "listPrevious.html"
        print "in", page

    # import ipdb;ipdb.set_trace()
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    variables = RequestContext(request, {
        'contacts': contacts,
    })

    return render_to_response(htmlPage, variables)


def actionCustomerDomains(request, slug, pk):
    if request.is_ajax():
        supportREST(request)
        try:
            customer = Customer.objects.get(name=slug)
        except ObjectDoesNotExist:
            return HttpResponse(u'등록되지 않은 고객.', status=500)
        else:
            if request.method == "POST":
                form = CustomerRegistrationForm(request.POST)

                if "domains" not in form.errors:
                    domain, created = Domain.objects.get_or_create(
                        url=request.POST['domains'],
                    )

                    domainsNote = request.POST['domainsNote']

                    if domainsNote == '':
                        domainsNote = u"%s 고객사에서 추가함" % slug

                    Note.objects.create(
                        contents=domainsNote,
                        writer=request.user,
                        content_object=domain,
                    )
                    customer.domains.add(domain)

                    return HttpResponse(
                        simplejson.dumps({'id': domain.pk}),
                        content_type="application/json"
                    )
                else:
                    return HttpResponse(status=500)
            #end if request.method == "POST":
            elif request.method == "DELETE":
                try:
                    domain = Domain.objects.get(pk=pk)
                except ObjectDoesNotExist:
                    return HttpResponse(u'등록되지 않은 URL.', status=500)
                else:
                    try:
                        customer.domains.remove(domain)
                    except:
                        printException(sys.exc_info())
                        return HttpResponse(u'remove() 실패.', status=500)
                    else:
                        Note.objects.create(
                            contents=u"%s 고객사에서 삭제됨." % slug,
                            writer=request.user,
                            content_object=domain,
                        )

                        return HttpResponse(status=204)
            else:
                return HttpResponse(u'0', status=500)
        #end else
    #end if request.is_ajax():
    else:
        return HttpResponse(u"Not ajax is denied", status=500)


def actionCustomerEquipments(request, slug, pk):
    if request.is_ajax():
        supportREST(request)
        try:
            customer = Customer.objects.get(name=slug)
        except ObjectDoesNotExist:
            return HttpResponse(u'등록되지 않은 고객.', status=500)
        else:
            if request.method == "POST":
                form = CustomerRegistrationForm(request.POST)
                if 'equipmentsType' not in form.errors:
                    try:
                        for i in ipValidation(
                            request.POST['equipmentsIpaddr'],
                        ):
                            try:
                                ip, created = IPaddr.objects.get_or_create(
                                    addr=i
                                )
                                Note.objects.create(
                                    content_object=ip,
                                    writer=request.user,
                                    contents=u"%s 고객사의 장비로 추가됨." % slug,
                                )
                                equipment = Equipment.objects.create(
                                    ipaddr=ip,
                                    type=request.POST['equipmentsType'],
                                )

                                customer.equipments.add(equipment)
                            except:
                                printException(sys.exc_info())
                                return HttpResponse(u"1", status=500)
                            else:
                                return HttpResponse(
                                    simplejson.dumps({"id": equipment.pk}),
                                    content_type="application/json"
                                )
                    except:
                        return HttpResponse(u"3", status=500)
                else:
                    print form.errors
                    return HttpResponse(u"2", status=500)
            elif request.method == "DELETE":
                try:
                    equipment = Equipment.objects.get(pk=pk)

                    customer.equipments.remove(equipment)

                    Note.objects.create(
                        contents=u"%s 고객사에서 삭제됨." % slug,
                        writer=request.user,
                        content_object=equipment.ipaddr,
                    )
                except:
                    return HttpResponse(u"remove() error", status=500)
                else:
                    return HttpResponse(status=204)
            else:
                return HttpResponse(u"3", status=500)
    #end if request.is_ajax():
    else:
        return HttpResponse(u"Not ajax is denied", status=500)


def actionCustomerPersonInCharges(request, slug, pk):
    if request.is_ajax():
        supportREST(request)
        try:
            customer = Customer.objects.get(name=slug)
        except:
            return HttpResponse(u'등록되지 않은 고객.', status=500)
        else:
            if request.method == "POST":
                form = CustomerRegistrationForm(request.POST)

                if "personInChargesEmail" not in form.errors:
                    try:
                        personInCharge = PersonInCharge.objects.create(
                            name=request.POST['personInChargesName'],
                            telephone1=request.POST['personInChargesTel'],
                            mobile1=request.POST['personInChargesMobile'],
                            email1=request.POST['personInChargesEmail'],
                        )
                    except:
                        printException(sys.exc_info())
                        return HttpResponse(sys.exc_info(), status=500)
                    else:
                        customer.personInCharges.add(personInCharge)

                        return HttpResponse(
                            simplejson.dumps({"id": personInCharge.pk}),
                            content_type="application/json"
                        )
                else:
                    print form.errors
                    return HttpResponse("담당자 전자우편 오류", status=500)
            #end if request.method == "POST":
            elif request.method == "DELETE":
                try:
                    personInCharge = PersonInCharge.objects.get(pk=pk)
                except:
                    printException(sys.exc_info())
                    return HttpResponse(u"등록 되지 않은 담당자", status=500)
                else:
                    customer.personInCharges.remove(personInCharge)

                    return HttpResponse(status=204)
            else:
                return HttpResponse(u"Method 오류", status=500)
    #end if request.is_ajax():
    else:
        return HttpResponse(u"3", status=500)


@login_required
def customerDetail(request, slug):
    if request.method == "DELETE":
        try:
            Customer.objects.get(name=slug).delete()
        except:
            return HttpResponse(status=500)
        else:
            return HttpResponse(
                simplejson.dumps({"redirect": reverse('customer')}),
                content_type="application/json",
            )
    else:
        return customerDetailView.as_view()(request, slug=slug)

@login_required
def responsingAttackDetection(request):
    if request.method == "GET":

        return responsingAttackDetectionList.as_view()(request)

        # variables = RequestContext(request, {
        #     'user': request.user,
        # })
        # return render_to_response(
        #     'responsingAttackDetection.html',
        #     variables
        # )
    elif request.method == "POST":
        form = ResponsingAttackDetectionForm(request.POST)

        if form.is_valid():
            attackerIp, isAttackerIpCreated = IPaddr.objects.get_or_create(
                addr=form.cleaned_data['attackerIp'],
            )
            victimIp, isVictimIpCreated = IPaddr.objects.get_or_create(
                addr=form.cleaned_data['victimIp'],
            )
            customer = Customer.objects.get(
                name=form.cleaned_data['customer'],
            )
            ResponsingAttackDetection.objects.create(
                kind=form.cleaned_data['kind'],
                attackerIp=attackerIp,
                victimIp=victimIp,
                user=request.user,
                customer=customer,
                emailRecipient=form.cleaned_data['emailRecipient'],
                smsRecipient=form.cleaned_data['smsRecipient'],
                note=form.cleaned_data['note'],
            )

        return HttpResponseRedirect(reverse('responsingAttackDetection'))


def responsingAttackDetectionNew(request):
    if request.method == "GET":
        form = ResponsingAttackDetectionForm()

        variables = RequestContext(request, {
            'form': form,
            'action': reverse('responsingAttackDetection')
        })

        return render_to_response(
            'responsingAttackDetectionNew.html',
            variables
        )


class responsingAttackDetectionList(ListView):
    model = ResponsingAttackDetection
    context_object_name = 'responsingAttackDetection'
    template_name = "responsingAttackDetection.html"
    allow_empty = True


class responsingAttackDetectionDetailView(DetailView):
    model = ResponsingAttackDetection
    context_object_name = 'responsingAttackDetectionDetailView'
    template_name = 'responsingAttackDetectionDetail.html'


def responsingAttackDetectionDetail(request, slug):
    if request.method == 'GET':
        return responsingAttackDetectionDetailView.as_view()(request, slug=slug)
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass
    elif request.method == 'PUT':
        pass
    else:
        return HttpResponse(status=500)


@login_required
def userDetail(request, slug):
    if request.method == "GET":
        return UserDetailView.as_view()(request, slug=slug)
    else:
        return HttpResponse(status=500)


class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    template_name = 'userDetail.html'
    context_object_name = 'userDetailView'


@login_required
def ipDetail(request, slug):
    if request.method == 'GET':
        if iptools.validate_ip(slug):
            return IpDetailView.as_view()(request, slug=slug)
        else:
            return HttpResponse("no ip", status=404)

class IpDetailView(DetailView):
    model = IPaddr
    slug_field = 'addr'
    template_name = 'ipDetail.html'
    context_object_name = 'ipDetailView'


@login_required
def getIpAddressCountry(request, ip):
    return HttpResponse(GeoIP(ip))
