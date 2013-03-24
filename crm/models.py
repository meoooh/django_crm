# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, to_field='username')
    mobile = models.CharField(unique=True, max_length=20,)
    lastIp= models.GenericIPAddressField(null=True)
    position = models.CharField(max_length=20, null=True)
    function = models.CharField(max_length=20, null=True)
    level = models.CharField(max_length=20, null=True)
    team = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=70)

    def __unicode__(self):
        return '%s, %s, %s, %s, %s, %s, %s, %s'%(
                self.user.username, 
                self.name,
                self.mobile, 
                self.lastIp, 
                self.position, 
                self.function, 
                self.level, 
                self.team, 
            )

class WorkDailyRecord(models.Model):
    user = models.ForeignKey(User, to_field='username')
    date = models.DateTimeField(auto_now_add=True)
    contents = models.TextField()
    check_user = models.ManyToManyField(
                User,
                related_name='checked_user_record_set',
            )
    target_user = models.ManyToManyField(
                User,
                related_name='target_user_record_set',
            )

    ONGOING_OR_END =(
                ('ing', '진행중'),
                ('end', '완료'),
            )


    ongoing_or_end = models.CharField(
                max_length=3,
                choices=ONGOING_OR_END,
                default='ing',
            )

    def __unicode__(self):
        return '%s, %s, %s, check_user: %s, target_user: %s, ongoing_or_end: %s'%(
                    self.user.get_profile().name,
                    self.date,
                    self.contents,
                    self.check_user.all(),
                    self.target_user.all(),
                    self.ongoing_or_end,
                )
    
class Note(models.Model):
    contents = models.TextField()
    writer = models.ForeignKey(User, to_field='username')
    date = models.DateTimeField(auto_now_add=True)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['pk'] # date를 기준으로 정렬
    
    def __unicode__(self):
        #return {u'name':u'%s'%self.writer.get_profile().name, u'contents':u'%s'%self.contents, u'date':u'%s'%self.date}
        return "writer: %s, contents: %s, date: %s"%(self.writer.get_profile().name, self.contents, self.date)
        
    def to_dict(self):
        # import ipdb;ipdb.set_trace()
        #return {u'name':u'%s'%self.writer.get_profile().name, u'contents':u'%s'%self.contents, u'date':u'%s'%self.date.strftime("%Y-%m-%d %I:%M:%S %p")}
        return {u'id':self.pk, u'name':self.writer.get_profile().name, u'contents':self.contents, u'date':self.date.isoformat()}
        
    def span(self):
        # import ipdb;ipdb.set_trace()
        return u'<span class="time">%s</span><span class="contents"><strong>%s</strong></span><span class="name">[%s]</span><span class="button"><button class="btn btn-mini modify" type="button" onclick="ModifyCustomerNote.call(this);">수정</button><button class="btn btn-mini delete" type="button" onclick="deleteCustomerNote.call(this);">삭제</button></span>'%(self.date.isoformat(), self.contents, self.writer.get_profile().name)
        # return u'한글'+self.contents
        
class IPaddr(models.Model):
    notes = generic.GenericRelation(Note, null=True)
    addr = models.GenericIPAddressField(unique=True,)
    country = models.CharField(max_length=30, null=True)
    
    class Meta:
        ordering = ['addr'] # 정렬
    
    def __unicode__(self):
        return "addr: %s, country: %s, len(notes): %d"%(self.addr, self.country, self.notes.all().count())
        
    def span(self):
        return u'<span class="ipaddr">%s</span><span class="button"><button type="button" class="close" data-dismiss="modal" aria-hidden="true" onclick="deleteCustomerIPaddrs.call(this);">x</button></span>'%(self.addr)
    
class PersonInCharge(models.Model):
    name = models.CharField(max_length=50,)
    telephone1 = models.CharField(null=True, max_length=20)
    telephone2 = models.CharField(null=True, max_length=20)
    mobile1 = models.CharField(null=True, max_length=20)
    mobile2 = models.CharField(null=True, max_length=20)
    email1 = models.EmailField(null=True)
    email2 = models.EmailField(null=True)
    notes = generic.GenericRelation(Note, null=True)
    
    def __unicode__(self):
        return "name: %s, telephone1: %s, telephone2: %s, mobile1: %s, mobile2: %s, email1: %s, email2: %s, len(notes): %d"%(self.name, self.telephone1, self.telephone2, self.mobile1, self.mobile2, self.email1, self.email2, self.notes.all().count())
        
    def span(self):
        return u'<ul class="unstyled"><li><span class="name">%s</span></li><li><span class="tel">%s</span></li><li><span class="mobile">%s</span></li><li><span class="email">%s</span></li></ul>'%(self.name, self.telephone1, self.mobile1, self.email1)

    
class Domain(models.Model):
    url = models.URLField(unique=True,)
    notes = generic.GenericRelation(Note, null=True)
    
    def __unicode__(self):
        return "url: %s, len(notes): %d"%(self.url, self.notes.all().count())
        
    def span(self):
        return u'<span class="domain">%s</span><button type="button" class="close" data-dismiss="modal" aria-hidden="true" onclick="deleteCustomerDomains.call(this);">x</button>'%(self.url)
    
class Equipment(models.Model):
    types =(
                ('IDS', 'IDS'),
                ('IPS', 'IPS'),
                ('방화벽', '방화벽'),
                ('웹방화벽', '웹방화벽'),
                ('스위치', '스위치'),
                ('Anti-DDos', 'Anti-DDos'),
                ('Log', 'Log'),
                ('UTM', 'UTM'),
                ('기타', '기타'),
            )
    
    type = models.CharField(
                choices=types,
                default='etc',
                max_length=4,
                null=True,
            )
    ipaddr = models.ForeignKey(IPaddr, to_field='addr')
    
    class Meta:
        ordering = ['pk']
    
    def __unicode__(self):
        return "type: %s, ipaddr: %s"%(self.type, self.ipaddr)
        
    def span(self):
        # import ipdb;ipdb.set_trace()
        return u'<ul class="unstyled"><li><span class="type">%s</span><button type="button" class="close" data-dismiss="modal" aria-hidden="true" onclick="deleteCustomerEquipments.call(this);">×</button></li><li><span class="ipaddr">%s</span></li></ul>'%(self.type, self.ipaddr.addr)
    
class Customer(models.Model):
    name = models.CharField(max_length=50, unique=True,)
    personInCharges = models.ManyToManyField(PersonInCharge, null=True, related_name='customer_personincharges_personincharge_set')
    position = models.CharField(null=True, max_length=50,)
    serviceName = models.CharField(null=True, max_length=50,)
    detailedServiceName = models.CharField(null=True, max_length=50,)
    serviceNumber = models.CharField(null=True, max_length=50,)
    dataFolder = models.CharField(null=True, max_length=50,)
    workers = models.ManyToManyField(User, related_name='customer_workers_user_set', null=True)
    salespersons = models.ManyToManyField(User, related_name='customer_salespersons_user_set', null=True)
    notes = generic.GenericRelation(Note, null=True)
    ipaddrs = models.ManyToManyField(IPaddr, related_name='customer_ipaddrs_ipaddr_set', null=True)
    domains = models.ManyToManyField(Domain, related_name='customer_domains_domain_set', null=True)
    equipments = models.ManyToManyField(Equipment, related_name='customer_equipments_equipment_set', null=True)
    alertEmails = models.ManyToManyField(PersonInCharge, related_name='customer_alertEmails_personincharge_set', null=True)
    alertSMSs = models.ManyToManyField(PersonInCharge, related_name='customer_alertSMSs_personincharge_set', null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return "name: %s"%self.name