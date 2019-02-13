from django.shortcuts import render
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType

from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse,Http404
from django.contrib.auth import get_user_model

User=get_user_model()


from accounts.models import FriendRequest
from accounts.forms import UserLoginForm
from posts.models import Post
from comments.models import Comment
from pages.models import Page
from clubs.models import Group ,JoinRequest

from posts.forms import PostCreateForm
from chat.forms import MessageCreateForm
from pages.forms import PageCreateForm
from clubs.forms import GroupCreateForm
from accounts.forms import UserLoginForm


class AngularTemplateView(View):
    def get(self,request,item=None,name=None,*args,**kwargs):
        template_path=settings.TEMPLATES[0]["DIRS"][0]
        final_path=os.path.join(template_path,"ang","app",item+".html")
        users=User.objects.all()[:4]


        if item=='home':
            users=User.objects.all()[:4]
            if self.request.user.is_authenticated:
                friends=self.request.user.profile.friends.all()
            else:
                friends=[]
              
            return render(request,final_path,{'request':self.request,
                                                  'post_form':PostCreateForm,
                                                  'login_form':UserLoginForm,
                                                  'users':users,
                                                  'friends':friends,
                                                 })
        elif item=='profile':
            try:
                if self.request.user.is_authenticated:
                    user=User.objects.get(username=name)
                    obj=user.profile
                    friends=user.profile.friends.all()
                    sent_frequests=FriendRequest.objects.filter(from_user= user)
                    res_frequests=FriendRequest.objects.filter(to_user= user)
                    status='None'
                    op='None'
                    if FriendRequest.objects.filter(from_user=self.request.user,to_user=user):
                        status='Cancel Friend Request'
                        op='cancel'
                    elif FriendRequest.objects.filter(to_user=self.request.user,from_user=user):
                        status='Confirm Friend Request'
                        op='confirm'
                    elif self.request.user.profile in friends:
                        status='UnFriend'
                        op='delete'
                    else :
                        status='Add Friend'
                        op='send'
                    if self.request.user.profile in user.followed_by.all():
                        followStatus="Unfollow"
                    else:
                         followStatus="Follow"

                    return render(request,final_path,{'request':self.request,
                                                          'post_form':PostCreateForm,
                                                          'message_form':MessageCreateForm,
                                                          'status':status,
                                                          'op':op,
                                                          'users':users,
                                                          'friends':friends,
                                                          'sent_frequests':sent_frequests,
                                                          'res_frequests':res_frequests,
                                                          'obj':obj,
                                                          'followStatus':followStatus
                                                         })
                else:
                    return render(request,'ang/app/login.html',{'request':self.request,
                                                          'form':UserLoginForm,
                                                         })
            except:
                return render(request,'ang/app/login.html',{'request':self.request,
                                                          'form':UserLoginForm,
                                                         })
                

        elif item=='page':
            likePage='Like'
            page = Page.objects.get(name=name)
            if request.user in page.liked.all():
                likePage='Unlike'

            return render(request,final_path,{'object':page,
                                             'post_form':PostCreateForm,
                                             'likePage':likePage,
                                             })
        elif item=='group':
            status='None'
            op='None'
            group = Group.objects.get(name=name)
            if JoinRequest.objects.filter(user=self.request.user,group=group):
                status='Cancel Join Request'
                op='cancel'

            elif self.request.user in group.joined.all():
                status='Leave Group'
                op='delete'
            else :
                status='Join'
                op='send'
            return render(request,final_path,{'object':group,
                                             'post_form':PostCreateForm,
                                             'op':op,
                                             'status':status,
                                             })
        elif item=='post_list':
            return render(request,final_path,{ })

        elif item=='page_list':
            return render(request,final_path,{ })

        elif item=='page_list_item':
            return render(request,final_path,{ })

        elif item=='group_list':
            return render(request,final_path,{ })

        elif item=='group_list_item':
            return render(request,final_path,{ })

        elif item=='page_new':
            return render(request,final_path,{'form':PageCreateForm })

        elif item=='group_new':
            return render(request,final_path,{'form':GroupCreateForm })
        elif item=='photo_list':
            user=User.objects.get(pk=name)
            return render(request,final_path,{'user':user })

        elif item=='photo':
            return render(request,final_path,{ })

        elif item=='login':
            return render(request,final_path,{'form':UserLoginForm, })

        elif item=='search':
            return render(request,final_path,{ })

        elif item=='inbox':
            return render(request,final_path,{ })
        
        elif item=='post':
            content_type=ContentType.objects.get_for_model(Post)
            post=Post.objects.get(id=name)
            comment_count=Comment.objects.filter(content_type=content_type,object_id=post.id).count()             
            return render(request,final_path,{'id':name,
                                            })


#def get_angular_template(request,item=None):
#    print(item)
#    return render(request,"ang/app/post-list.html",{})