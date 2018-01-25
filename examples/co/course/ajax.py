from django_ajax.decorators import ajax
import pickle   
from django.utils.translation import ugettext as _
import brukva
bclient = brukva.Client()
bclient.connect()
import json
import logging
logger = logging.getLogger(__name__)
from course.utils import *
from course.models import *
import time
    
@ajax
def turn_owner_cam_on(request):
    lesson = Lesson.objects.get(pk=request.GET['lesson_id'])
    lesson.is_camera_on = True
    lesson.save()
    request.user.is_cam_on = True
    request.user.save()
    psp = get_participants_exclude_one(lesson,request.user)
    #import pdb; pdb.set_trace()
    for u in psp:
        mes = { 'act': 'owner_turn_cam_on', 'lesson_id': lesson.id, 'user_id': u.id }
        r = 'lesson_%s_%s' % (lesson.id, u.id)
        bclient.publish(r, json.dumps(mes))
    data = {
            'inner-fragments': { 
                '#owner_cam': owner_cam_template(lesson,request.user,type='out'),
                
             },   
                
           }
    
    return data       
    

@ajax
def turn_owner_cam_off(request):
    lesson = Lesson.objects.get(pk=request.GET['lesson_id'])
    lesson.is_camera_on = False
    lesson.save()
    request.user.is_cam_on = False
    request.user.save()
    psp = get_participants_exclude_one(lesson,request.user)
    #import pdb; pdb.set_trace()
    for u in psp:
        mes = { 'act': 'owner_turn_cam_off', 'lesson_id': lesson.id, 'user_id': u.id }
        r = 'lesson_%s_%s' % (lesson.id, u.id)
        bclient.publish(r, json.dumps(mes))
    data = {
            'inner-fragments': { 
                '#owner_cam': '<h3 align="center">Camera is disabled</h3>',
                
             },   
                
           }
    
    return data   



@ajax
def show_owner_cam(request):
    lesson = Lesson.objects.get(pk=request.GET['lesson_id'])
    data = {
            'inner-fragments': { 
                '#owner_cam': owner_cam_template(lesson,request.user,type='in'),
                
             },   
                
           }
    
    return data       
    

@ajax
def hide_owner_cam(request):
    lesson = Lesson.objects.get(pk=request.GET['lesson_id'])
    data = {
            'inner-fragments': { 
                '#owner_cam': '<h3 align="center">Camera is disabled</h3>',
                
             },   
                
           }
    
    return data   




@ajax
def update_participants(request):
    lesson = Lesson.objects.get(pk=request.GET['lesson_id'])
    ret = ''
    for u in get_participants(lesson):
        ret = ret + u.thumb
    data = {
            'inner-fragments': { 
                '#participants': ret,
                
             },   
                
           }
    
    return data   

@ajax
def update_history(request):
    lesson = Lesson.objects.get(pk=request.GET['lesson_id'])
    ret = ''
    for e in Event.objects.filter(lesson=lesson):
        ret = ret + '<li><a href="#">%s</a>&nbsp;%s:%s:%s</li>' % (e, e.created.hour,e.created.minute,e.created.second)
    data = {
            'inner-fragments': { 
                '#history': ret,
                
             },   
                
           }
    
    return data   



@ajax
def update_chat_messages(request):
    lesson = Lesson.objects.get(pk=request.GET['lesson_id'])
    ret = ''
    for e in ChatMessages.objects.filter(lesson=lesson):
        ret = ret + '<li> %s <span> %s </span> <b> %s </b></li>' % ( e.user.thumb, e.text, e.user.user_name)
    data = {
            'inner-fragments': { 
                '#chat_text_messages': ret,
                
             },   
                
           }
    
    return data 




@ajax
def show_student_cam(request,type):
    
    lesson = Lesson.objects.get(pk=request.GET['lesson_id'])
  
    
    data = {
            'prepend-fragments': { 
                '#student_cam_list': student_cam_template(lesson,request.GET['user_id'],type),
                
             },   
                
           }
    
    
    return data       
    

@ajax
def hide_student_cam(request):
    lesson = Lesson.objects.get(pk=request.GET['lesson_id'])
    data = {
            'inner-fragments': { 
                '#student_cam': '<h3 align="center">Camera is disabled</h3>',
                
             },   
                
           }
    
    return data 

@ajax
def delete_event(request):
    e = Event.objects.get(pk=int(request.GET['id']))
    id = str(e.id)
    e.delete()
    data = {
            'fragments': { 
                '#event_'+id: '',
                
             },   
                
           }
    
    return data 

@ajax
def move_event_to_incubator(request):
    e = Event.objects.get(pk=int(request.GET['id']))
    i = Incubator()
    i.tp = e.tp
    i.image_file = e.image_file
    i.image_url = e.image_url
    i.text = e.text
    i.lesson = e.lesson
    i.created = e.created
    i.text_size = e.text_size
    i.text_color = e.text_color
    i.text_align = e.text_align
    i.save()
    id = str(e.id)
    e.delete()
    data = {
            'fragments': { 
                '#event_'+id: '',
                
             },   

            'append-fragments': { 
                '#incubator_list': i.li_item,
                
             },  
                
           }
    
    return data 




@ajax
def delete_incubator(request):
    e = Incubator.objects.get(pk=int(request.GET['id']))
    id = str(e.id)
    e.delete()
    data = {
            'fragments': { 
                '#incubator_'+id: '',
                
             },   
                
           }
    
    return data 

@ajax
def move_incubator_to_event(request):
    e = Incubator.objects.get(pk=int(request.GET['id']))
    i = Event()
    i.tp = e.tp
    i.image_file = e.image_file
    i.image_url = e.image_url
    i.text = e.text
    i.lesson = e.lesson
    i.created = e.created
    i.text_size = e.text_size
    i.text_color = e.text_color
    i.text_align = e.text_align
    i.save()
    id = str(e.id)
    e.delete()
    data = {
            'fragments': { 
                '#incubator_'+id: '',
                
             },   

            'append-fragments': { 
                '#event_list': i.li_item,
                
             },  
                
           }
    
    return data 


@ajax
def incubator_fire(request):
    e = Incubator.objects.get(pk=int(request.GET['id']))
    psp = get_participants(e.lesson)
    #import pdb; pdb.set_trace()
    for u in psp:
        r = 'lesson_%s_%s' % (e.lesson.id, u.id)
        if(e.tp=='image_file'): 
            m = "<img class='from_publisher' src='%s' />" % e.text
            mes = { 'act': 'clear_writeboard' } 
            bclient.publish(r, json.dumps(mes))
        else:
            m = e.text
      
        mes = {"act":"text_message","message":  m,"lesson_id": e.lesson.id, "user_id": u.id, 'text_size': e.text_size, 'text_color': e.text_color, 'text_align': e.text_align}

        
        bclient.publish(r, json.dumps(mes))
    data = { }
    return data 



@ajax
def take_pic(request):
   
    data = {
            'inner-fragments': { 
                '#my_cam': my_cam_template(request.user),
                
             },   

           
                
           }
    
    return data 


@ajax
def save_pic(request):
    make_thumb(request.user)
    data = {
            'inner-fragments': { 
                '#my_cam': '<h2> %s </h2>' % _('Wait some seconds.'),
                
             },   

           
                
           }
    
    return data 




@ajax
def start_lesson(request):
    
    lesson = Lesson.objects.get(pk=request.GET['lesson_id'])
    if lesson.owner == request.user:
        lesson.is_runing = True
        lesson.save()
        for u in UserProfile.objects.all():
            tar = 'innerpage_%s' % u.id
            mes = {"act":"lesson_started", "lesson_id":  lesson.id}
            bclient.publish(tar, json.dumps(mes))            
    return {} 


@ajax
def stop_lesson(request):    
    lesson = Lesson.objects.get(pk=request.GET['lesson_id'])
    if lesson.owner == request.user:
        lesson.is_runing = False
        lesson.save()
        for u in UserProfile.objects.all():
            tar = 'innerpage_%s' % u.id
            mes = {"act":"lesson_stoped", "lesson_id":  lesson.id}
            bclient.publish(tar, json.dumps(mes))       
    return {} 



@ajax
def alert_lesson_started(request): 
    lesson = Lesson.objects.get(pk=request.GET['lesson_id'])
    link = lesson.get_absolute_url_for_student()
    mess = _('''Lesson <b> %s </b> from course <b> %s </b> just have been started. 
                You can join to this lesson by following a button below. <br>
                <a href="%s" class="btn btn-success red"> Join to this lesson </a>''') % (lesson.name, lesson.course, link)
    return {'lesson_name': lesson.name, 'message': mess} 




@ajax
def alert_lesson_stoped(request): 
    lesson = Lesson.objects.get(pk=request.GET['lesson_id'])
    mess = _('''Lesson <b> %s </b> from course <b> %s </b> just have been stoped. 
                Thank you for visiting us.''') % (lesson.name, lesson.course)
    return {'lesson_name': lesson.name, 'message': mess} 
    return {} 


@ajax
def get_lesson_running(request): 
    lessons = Lesson.objects.filter(is_runing=True)
    data = {
            'inner-fragments': { 
                '#running_lesson': lesson_runing(lessons),     
             },   
           }
    return data




