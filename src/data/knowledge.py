# -*- coding: utf-8 -*-

from ck.models import CircleKnowledgeComment, CompanyKnowledgeComment
from src.error import TooMuchCommentsError

#   event_code
#       0:  その他(event)
#       1:  並んだ時間(start, finish)
#       2:  売り切れた時間(event)
#       3:  現数が変更された時間(event)
def register_circleknowledgecomment(parent_circle_knowledge, parent_user, comiket_number, comment, event_code, onymous,
                                    parent_group=None, event_time_hour=None, event_time_min=None, start_time_hour=None,
                                    start_time_min=None, finish_time_hour=None, finish_time_min=None):
    ckc = CircleKnowledgeComment.objects.filter(parent_circle_knowledge=parent_circle_knowledge, parent_user=parent_user,
                                           comiket_number=comiket_number)
    if len(ckc) >= 5:
        raise TooMuchCommentsError
    ckc = CircleKnowledgeComment()
    ckc.parent_circle_knowledge = parent_circle_knowledge
    ckc.parent_user = parent_user
    ckc.comiket_number = comiket_number
    ckc.comment = comment
    ckc.event_code = event_code
    ckc.onymous = onymous
    if parent_group:
        ckc.parent_group = parent_group
    if event_code == 1:
        ckc.start_time_hour = start_time_hour
        ckc.start_time_min = start_time_min
        ckc.finish_time_hour = finish_time_hour
        ckc.finish_time_min = finish_time_min
    else:
        ckc.event_time_hour = event_time_hour
        ckc.event_time_min = event_time_min
    ckc.save()

def delete_circleknowledgecomment(comment_id):
    try:
        ckc = CircleKnowledgeComment.objects.get(id=comment_id)
        ckc.delete()
        return True
    except:
        return False

#   event_code
#       0:  その他(event)
#       1:  並んだ時間(start, finish)
#       2:  売り切れた時間(event)
#       3:  現数が変更された時間(event)
def register_companyknowledgecomment(parent_company_knowledge, parent_user, comiket_number, comment, event_code, onymous, day,
                                    parent_group=None, event_time_hour=None, event_time_min=None, start_time_hour=None,
                                    start_time_min=None, finish_time_hour=None, finish_time_min=None):
    ckc = CompanyKnowledgeComment.objects.filter(parent_company_knowledge=parent_company_knowledge, parent_user=parent_user,
                                           comiket_number=comiket_number)
    if len(ckc) >= 5:
        raise TooMuchCommentsError
    ckc = CompanyKnowledgeComment()
    ckc.parent_company_knowledge = parent_company_knowledge
    ckc.parent_user = parent_user
    ckc.comiket_number = comiket_number
    ckc.comment = comment
    ckc.event_code = event_code
    ckc.onymous = onymous
    ckc.day = day
    if parent_group:
        ckc.parent_group = parent_group
    if event_code == 1:
        ckc.start_time_hour = start_time_hour
        ckc.start_time_min = start_time_min
        ckc.finish_time_hour = finish_time_hour
        ckc.finish_time_min = finish_time_min
    else:
        ckc.event_time_hour = event_time_hour
        ckc.event_time_min = event_time_min
    ckc.save()

def delete_companyknowledgecomment(comment_id):
    try:
        ckc = CompanyKnowledgeComment.objects.get(id=comment_id)
        ckc.delete()
        return True
    except:
        return False