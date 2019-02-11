var app = angular.module('app',['ngRoute','ngResource','ngCookies']);
  
app.config(function($routeProvider,$locationProvider){
    $locationProvider.html5Mode({enabled:true})
    $routeProvider
    .when('/',{
        templateUrl :function(params){
            return 'api/templates/'+params.name +'/home.html';
        } ,
//        controller:'homeController'
    })    

     .when('/accounts/:name',{
        templateUrl :function(params){
            return 'api/templates/'+params.name +'/profile.html';
        },
     })        
//     .when('/accounts/login',{
//        templateUrl :function(params){
//            return 'api/templates/'+params.name +'/login.html';
//        },
//     })    
    .when('/pages',{
        templateUrl :function(params){
            return 'api/templates/'+params.name +'/page_list.html';
        }
         ,
     })    
    .when('/pages/new',{
        templateUrl :function(params){
            return 'api/templates/'+params.name +'/page_new.html';
        }
         ,
     })
    .when('/pages/:name',{
        templateUrl :function(params){
            return 'api/templates/'+params.name +'/page.html';
        }
         ,
     })    
    .when('/groups/:name',{
        templateUrl :function(params){
            return 'api/templates/'+params.name +'/group.html';
        }
         ,
     })
    .when('/groups',{
        templateUrl :function(params){
            return 'api/templates/'+params.name +'/group_list.html';
        }
         ,
     })    
    .when('/groups/new/add',{
        templateUrl :function(params){
            return 'api/templates/'+params.name +'/group_new.html';
        }
         ,
     })    
    .when('/files/:op/:pk',{
        templateUrl :function(params){
            return 'api/templates/'+params.pk +'/photo_list.html';
        }
         ,
     })    
     .when('/search',{
        templateUrl :function(params){
            return 'api/templates/'+params.pk +'/search.html';
        }
         ,
     })     
    .when('/inbox',{
        templateUrl :function(params){
            return 'api/templates/'+params.pk +'/inbox.html';
        }
         ,
     })
})

var getUrl =window.location;   

var getBaseUrl =getUrl.protocol+"//"+getUrl.host+"/"+getUrl.pathname.split('/')[0];   

function getCookie(name) {
var cookieValue = null;
if (document.cookie && document.cookie !== '') {
var cookies = document.cookie.split(';');
for (var i = 0; i < cookies.length; i++) {
var cookie = jQuery.trim(cookies[i]);
// Does this cookie string begin with the name we want?
if (cookie.substring(0, name.length + 1) === (name + '=')) {
cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
break;
}
}
}
return cookieValue;
}
var csrftoken = getCookie('csrftoken');

app.service('searchService',[function(){
    this.searchList=[];
    this.searchListPage=[];
    this.searchListGroup=[];
    this.searchListPost=[];
    this.messageList=[];
    
}])
app.controller('searchController',['$scope','searchService','$cookies','$location','$http','$rootScope',function($scope,searchService,$cookies,$location,$http,$rootScope){
        $scope.searchList= searchService.searchList;
        $scope.searchListGroup= searchService.searchListGroup;
        $scope.searchListPage= searchService.searchListPage;
        $scope.searchListPost= searchService.searchListPost;
   
}]);
app.controller('inboxController',['$scope','searchService','$cookies','$location','$http','$rootScope',function($scope,searchService,$cookies,$location,$http,$rootScope){
//        $scope.messageList= searchService.messageList;
    var requestUser;

     $scope.conversation=[];
     $scope.to_userID;
      $scope.to_userName='';
    $scope.get_conversation=function(fusername,tusername){

        var url='/api/chat/conversation/'+fusername+'/'+tusername+'/'

        $http(
            {
            method:"GET",
            url:url,
             headers:{"X-CSRFToken":csrftoken},
            }
             ).then(
            function(response){
                $scope.conversation=response.data.results;
                requestUser=angular.element(document.querySelector("reID"));
                $scope.requestUserID =requestUser.attr('pk');
                if($scope.conversation[0].to_user.id ==$scope.requestUserID){
                    $scope.to_userID=$scope.conversation[0].from_user.id
                    $scope.to_userName=$scope.conversation[0].from_user.username
                }else{
                 $scope.to_userID=$scope.conversation[0].to_user.id

                }
               },

             function(response){
                console.log(response)
             }

        ) 

        };
    $scope.get_conversations=function(){

        var url='/api/chat/list/cons/'

        $http(
            {
            method:"GET",
            url:url,
             headers:{"X-CSRFToken":csrftoken},
            }
             ).then(
            function(response){
                $scope.conversationList=response.data.results;
               },

             function(response){
                console.log(response)
             }

        ) 

        };
     $scope.get_conversations()
    
    $scope.message={};
    $scope.sendMessage=function(pk=0){
        var url='/api/chat/create/'+pk+'/'

        console.log(url)
        $http(
            {
            method:"POST",
            url:url,
            data:$scope.message,
            headers:{"X-CSRFToken":csrftoken},
              }
             ).then(
            function(response){
                console.log(response)
            $scope.conversation.unshift(response.data)
                $("#msgContent textarea").val("")


               },

             function(response){
                console.log(response)}

        ) 

    };
   
}]);

app.controller('rightController',['$scope','$cookies','$location','$http','$rootScope',function($scope,$cookies,$location,$http,$rootScope){
    $scope.message={};
    $scope.sendMessage=function(pk=0){
        var url='/api/chat/create/'+pk+'/'

        console.log(url)
        $http(
            {
            method:"POST",
            url:url,
            data:$scope.message,
            headers:{"X-CSRFToken":csrftoken},
              }
             ).then(
            function(response){
                $("#sendModal textarea").val("")
                $("#sendModal").modal('hide')
                

               },

             function(response){
                console.log(response)}

        ) 

    };
}]);
app.controller('headerController',['$scope','searchService','$cookies','$location','$http','$rootScope',function($scope,searchService,$cookies,$location,$http,$rootScope){
        $scope.searchList= searchService.searchList;
        $scope.searchListPage= searchService.searchListPage;
        $scope.searchListGroup= searchService.searchListGroup;
        $scope.$watch('searchList',function(){
            searchService.searchList=$scope.searchList;
        });          
        $scope.searchListPost= searchService.searchListPost;
        $scope.$watch('searchListPost',function(){
            searchService.searchListPost=$scope.searchListPost;
        });       
        $scope.$watch('searchListPage',function(){
            searchService.searchListPage=$scope.searchListPage;
        });        
        $scope.$watch('searchListGroup',function(){
            searchService.searchListGroup=$scope.searchListGroup;
        });
        $scope.$watch('messageList',function(){
            searchService.messageList=$scope.messageList;
        });
        $scope.actionList;
        $scope.user={};
        $scope.signup={};
        var tokenExists= $cookies.get("token")
        if(tokenExists){
         //verify token
         $scope.loggedIn=true;
         $cookies.remove("token")
         $scope.user.username=$cookies.get("username")
        }
        $scope.login=function(){
             var url='/api/accounts/login/'
             
             $http(
                 {
                 method:"POST",
                 url:url,
                 data:$scope.user,
//                  headers:{"X-CSRFToken":csrftoken},
                 }
                  ).then(
                 function(response){
                  $cookies.put("token",response.data.token)
                  $cookies.put("username",$scope.user.username)
                  $location.path('/')
                  console.log(response.data.token)
                    },

                  function(response){
                     console.log(response)
                  }

             )         
        };        
       $scope.registerUser=function(){
             var url='/api/accounts/signup/'
             if($scope.signup.password1 ==$scope.signup.password2 ){
                   $scope.signup.password =$scope.signup.password2;
             
                  $http(
                      {
                      method:"POST",
                      url:url,
                      data:$scope.signup,
                       headers:{"X-CSRFToken":csrftoken},
                      }
                       ).then(
                      function(response){
                          console.log(response.data)
                         },

                       function(response){
                          console.log(response)
                       }  ) 
             }
             else{
              alert('')
             }
        };
  $scope.search={}
        $scope.search.op='users'

 $scope.onSelectChange=function(value){
            $scope.search.op=value;
     
 }
 $scope.search_data=function(){

        var url='/api/posts/search/?op='+$scope.search.op+'&content='+$scope.search.content;
        $http(
            {
            method:"GET",
            url:url,
             headers:{"X-CSRFToken":csrftoken},
            }
             ).then(
            function(response){
                if($scope.search.op=='users')
                    {     $scope.searchList=response.data;
                    }
                else if($scope.search.op=='groups'){
                    $scope.searchListGroup=response.data;
                }                
                else if($scope.search.op=='pages'){
                    $scope.searchListPage=response.data;
                }                
                else if($scope.search.op=='posts'){
                    $scope.searchListPost=response.data;
                    console.log( $scope.searchListPost)
                }
                  $location.path('/search')
               },

             function(response){
                console.log(response)
             }

        ) 

        };    
 
 $scope.get_actions=function(){

        var url='/api/actions/list/'

        $http(
            {
            method:"GET",
            url:url,
             headers:{"X-CSRFToken":csrftoken},
            }
             ).then(
            function(response){
                $scope.actionList=response.data.results;
               },

             function(response){
                console.log(response)
             }

        ) 

        };
     $scope.get_actions() 
    
    $scope.get_messages=function(pk=0){

        var url='/api/chat/list/'

        $http(
            {
            method:"GET",
            url:url,
             headers:{"X-CSRFToken":csrftoken},
            }
             ).then(
            function(response){
                $scope.messageList=response.data.results;
               },

             function(response){
                console.log(response)
             }

        ) 

        };
     $scope.get_messages()

    
}]);
app.controller('photoController',['$scope',  '$resource','$http',function($scope, $resource,$http){
    
    $scope.profileimgList;
   
    $scope.get_photos=function(op,pk){

        var url='/api/files/photos/'+op+'/'+pk+'/'

        $http(
            {
            method:"GET",
            url:url,
            }
             ).then(
            function(response){
                $scope.profileimgList=response.data.results;
               },

             function(response){
                console.log(response)
             }

        ) 

        };
}]);
app.controller('adminListController',['$scope',  '$resource','$http',function($scope, $resource,$http){
    
    var objectType=angular.element(document.querySelector("call"));
    $scope.pk =objectType.attr('pk');
    $scope.op =objectType.attr('op');
    $scope.pageAdmin={}
    console.log($scope.pk)
    console.log($scope.op)
    
    $scope.ToggleAdmin=function(username){
        var name = username;
        console.log(username)
        if(! username){
            name=$scope.pageAdmin.username;
        }
        var url;
        if($scope.op == 'group'){
         url='/api/groups/'+$scope.pk+'/admin/?username='+name
            }
        else{
            url='/api/pages/'+$scope.pk+'/admin/?username='+name

        }

    $http(
        {
        method:"GET",
        url:url,
        data:$scope.pageAdmin,
//        headers:{"X-CSRFToken":csrftoken},
          }
         ).then(
        function(response){
            
            console.log(response.data)
            if(response.data.admin==true){
 
                console.log('admin added')
            } 
            else {
 
                console.log('admin removed')
 
            } 
               
           },

         function(response){
            console.log(response)}
 
    ) 

    };
}]);

app.controller('leftSideController',['$scope', '$resource','$http',function($scope, $resource,$http){

    $scope.files=[]; 
    
    
    $scope.onFileChange = function(files){
         $scope.files=files;

    }
    $scope.AddFile = function(imgType,pk=0){
        if($scope.files.length !=0)
           { 
            var url='api/files/create/'+imgType+'/'+pk+'/';
            var formData = new FormData();
            if($scope.files.length >1){ 
                for(i in $scope.files.length){  
                    formData.append('file',$scope.files[i]);
                    }
            }else{
              formData.append('file',$scope.files[0]);

            }

            $http.post(url,formData,{
                       withCredentials:true,
                       headers:{"X-CSRFToken":csrftoken,'Content-Type':undefined},
                       transformRequest:angular.identity,
                       }).then(
                        function(response){
                         $scope.files=[]
                        $scope.img_new= response.data.img;
                            $location.path('/')

                        },
                        function(response)
                            {
                            console.log(response)
                            }
                            )
           }

    }; 
    
    
    var friendStatus=angular.element(document.querySelector("#status"));
    $scope.friendStatus =friendStatus;
    $scope.friendOp=friendStatus.attr('op');
    
    $scope.friendRequest=function(fpk,tpk){
        
        var url='/api/posts/'+$scope.friendOp+'/'+fpk+'/'+tpk


    $http(
        {
        method:"GET",
        url:url,
        headers:{"X-CSRFToken":csrftoken},
          }
         ).then(
        function(response){
            
            console.log(response.data.op)
            if(response.data.op == 'send'){
                $scope.friendStatus.text('Cancel Request')
                $scope.friendOp='cancel'
                console.log('op')
                console.log( $scope.friendOp)
            } 
            else if(response.data.op == 'cancel'){
                $scope.friendStatus.text('Add Friend')
                $scope.friendOp='send'
                console.log('op')
                console.log( $scope.friendOp)

            } 
               
           },

         function(response){
            console.log(response)}
 
    ) 

    }; 
$scope.followStatus= angular.element(document.querySelector("#followStatus")).attr('followStatus')
    $scope.follow=function(username){
        var url='/api/accounts/'+username+'/follow/' 


        $http(
            {
            method:"GET",
            url:url,
            headers:{"X-CSRFToken":csrftoken},
              }
             ).then(
            function(response){

                console.log(response.data.op)
                    $scope.followStatus=response.data.followStatus
                    console.log( $scope.followStatus)

               },

             function(response){
                console.log(response)}

        ) 

    };
}]);


app.controller('pageCreateController',['$scope', '$resource','$http',function($scope, $resource,$http){
    var create_type = angular.element(document.querySelector("call"));
    $scope.page;
    var url;
    $scope.create_type=create_type.attr("op")
    $scope.AddPage=function(){
        if( $scope.create_type == 'page'){
               url='/api/pages/create/';}
        else{
            url='/api/groups/create/';
        }

    $http(
        {
        method:"POST",
        url:url,
        data:$scope.page,
        headers:{"X-CSRFToken":csrftoken},
          }
         ).then(
        function(response){
        $(".page-form textarea").val("")
        $(".page-form input").val("")
               console.log(response)
           },

         function(response){
            console.log(response)}
 
    ) 

        
        
    }
}]);
app.controller('pageListController',['$scope', '$resource','$http',function($scope, $resource,$http){
    
    

    $scope.searchOp='my'
    
    var list_type = angular.element(document.querySelector("call"));
    $scope.page = angular.element(document.querySelector("#page"));
//    var page=angular.element(document.querySelector("#page"));

    $scope.list_type=list_type.attr("op")
    $scope.likePage = function( url,pk){

       var likedUrl =getBaseUrl+url+pk+'/like/'
        console.log(likedUrl)
    $http(
        {
        method:"GET",
        url:likedUrl,
          }
         ).then(
        function(response){            
        if(url=='api/pages/'){
         if(response.data.liked){
               $scope.page.text("Unlike") 
            }else{
                $scope.page.text("Like")
            }
         }
           },

         function(response){
            console.log(response)}
 
    )

    }
    $scope.get_pages = function(){
 
        if($scope.list_type == 'g'){
        if($scope.nextgrouptUrl){
            $scope.groupurl= $scope.nextgroupUrl;
        }
        else{
            $scope.groupurl='/api/groups';
            }
        $http({method:"GET",
              url:$scope.groupurl,
            params:{
               "op":$scope.searchOp,
                     },
              }).then(
            function(response){
            $scope.groupList = response.data.results
                if(response.data.next){
                    $scope.nextgroupUrl=response.data.next
                    document.querySelector("#loadmore").style.cssText="display : block"

                 }
                else{
                     document.querySelector("#loadmore").style.cssText="display : none"
                 }             


            },
            function(response){
                console.log(response)}

        )    }else{ 

        if($scope.nextPageUrl){
            $scope.pageurl= $scope.nextPageUrl;
        }
        else{
            $scope.pageurl='/api/pages';
            }
        $http({method:"GET",
              url:$scope.pageurl,
            params:{
               "op":$scope.searchOp,
                     },
              }).then(
            function(response){
            $scope.pageList = response.data.results
                if(response.data.next){
                    $scope.nextPageUrl=response.data.next
                    document.querySelector("#loadmore").style.cssText="display : block"

                 }
                else{
                     document.querySelector("#loadmore").style.cssText="display : none"
                 }             


            },
            function(response){
                console.log(response)}

    )}};
    $scope.get_pages();
}])
app.controller('postListController',['$scope','$cookies', '$resource','$http',function($scope,$cookies, $resource,$http){

     $scope.AddFile = function(imgType,pk=0){
 
        if($scope.files.length !=0)
           { 
            var url='api/files/create/'+imgType+'/'+pk+'/';
            var formData = new FormData();
            if($scope.files.length >1){ 
                for(i in $scope.files.length){  
                    formData.append('file',$scope.files[i]);
                    }
            }else{
              formData.append('file',$scope.files[0]);

            }

            $http.post(url,formData,{
                       withCredentials:true,
                       headers:{"X-CSRFToken":csrftoken,'Content-Type':undefined},
                       transformRequest:angular.identity,
                       }).then(
                        function(response){
                         $scope.files=[]
                        $scope.img_new= response.data.img;
                            console.log($scope.img_new)

                        },
                        function(response)
                            {
                            console.log(response)
                            }
                            )
           }

    }; 
    
    $scope.AddPost=function(pk=0){
        var url='/api/posts/create/'
       
        var postType=angular.element(document.querySelector(".post-form")).attr('postType');
        var fileType=angular.element(document.querySelector(".post-form")).attr('fileType');

        if(postType=='user'){
            url="/api/posts/create/"
        }else if(postType=='page'){
            url="/api/posts/create/page/"+pk+'/'
        }else if(postType=='group'){
            url="/api/posts/create/group/"+pk+'/'
        } 

    $http(
        {
        method:"POST",
        url:url,
        data:$scope.post,
        headers:{"X-CSRFToken":csrftoken},
          }
         ).then(
        function(response){
            
            if(!$scope.postList){
               $scope.postList=[] 
            }
            $(".post-form textarea").val("")
            $scope.AddFile(fileType,response.data.id);
            $scope.postList.unshift(response.data)

               
           },

         function(response){
            console.log(response)}
 
    ) 

    };
    $scope.nextPostUrl;
    $scope.posturl;
    $scope.notFound=true;
    $scope.pk; 
    
    $scope.get_comments=function(pk,op){
        var url="/api/comments/"+op+"/"+pk
    if(op == 'comment'){ 

    if($scope.ncurl[pk]){
        url= $scope.ncurl[pk];
    }}else{
        if($scope.nreplyurl[pk]){
            url= $scope.nreplyurl[pk];
        }
        
    }    
        $http(
        {
        method:"GET",
        url:url,
          }
         ).then(
        function(response){
            if(op == 'comment'){ 
            $scope.c[pk]=response.data.results; 
            if(response.data.next){
                $scope.ncurl[pk]=response.data.next
                document.querySelector("#cloadmore"+pk.toString()).style.cssText="display : block"

             }
            else{
                 document.querySelector("#cloadmore"+pk.toString()).style.cssText="display : none"
             }
            }else{
               
             $scope.reply[pk]=response.data.results; 
            if(response.data.next){
                $scope.nreplyurl[pk]=response.data.next
                document.querySelector("#rloadmore"+pk.toString()).style.cssText="display : block"

             }
            else{
                 document.querySelector("#rloadmore"+pk.toString()).style.cssText="display : none"
             }               
                }
           },

         function(response){
            console.log(response)}
 
    ) 
        
    }
    $scope.comment={}
    $scope.post;

    $scope.c ={}
    $scope.postsLikes ={}
    $scope.commetnsLikes ={}
    $scope.ncurl ={}
    $scope.reply ={}
    $scope.nreplyurl ={}
    
          
    $scope.files=[]; 
    
    
    $scope.onPostFileChange = function(files){

         $scope.files=files;

    }

    
    $scope.AddComment=function(pk,op){
      
    var url="/api/comments/create/"+op+"/"+pk

    $http(
        {
        method:"POST",
        url:url,
        data:$scope.comment[pk],
        headers:{"X-CSRFToken":csrftoken},
          }
         ).then(
        function(response){
            if(op=='comment'){  
            if(!$scope.c[pk]){
               $scope.c[pk]=[] 
            }
             $scope.c[pk].unshift(response.data)
                 $(".comment-form .commentInput").val("")

            }else{
            if(!$scope.reply[pk]){
               $scope.reply[pk]=[] 
            }
             $scope.reply[pk].unshift(response.data)
             $(".reply-form .replyInput").val("")

               
            }
           },

         function(response){
            console.log(response)}
 
    ) 
        
    };
    
    
    
    var profile = angular.element(document.querySelector("call"));
//    var page=angular.element(document.querySelector("#page"));

    $scope.pk=profile.attr("pk")
    $scope.op=profile.attr("op")


    $scope.likePage = function( url,pk){

       var likedUrl =getBaseUrl+url+pk+'/like/'
       console.log(url)

    $http(
        {
        method:"GET",
        url:likedUrl,
          }
         ).then(
        function(response){
         if(url=='api/posts/'){
    $scope.postsLikes[pk] = angular.element(document.querySelector("#postLike"+pk));

         if(response.data.liked){
              $scope.postsLikes[pk].text("Unlike")

            }else{
              $scope.postsLikes[pk].text("Like")
            }
         }else  if(url=='api/comments/'){
             
        $scope.commetnsLikes[pk] = angular.element(document.querySelector("#commentLike"+pk));

         if(response.data.liked){
              $scope.commetnsLikes[pk].text("Unlike")

            }else{
              $scope.commetnsLikes[pk].text("Like")
            }
         } 
           },

         function(response){
            console.log(response)}
 
    )

    }

    $scope.get_data = function(){
            op=$scope.op;
            pk=$scope.pk;

    if($scope.nextPostUrl){
        $scope.posturl= $scope.nextPostUrl;
    }
    else{
        $scope.posturl='/api/posts/list';
        }
    $http({method:"GET",
          url:$scope.posturl,
        params:{
           "op":op,
           "pk":pk,
                 },
           headers:{"Authorization":$cookies.get("token")},
           
          }).then(
        function(response){
        $scope.postList = response.data.results
            if(response.data.next){
                $scope.nextPostUrl=response.data.next
                document.querySelector("#loadmore").style.cssText="display : block"

             }
            else{
                 document.querySelector("#loadmore").style.cssText="display : none"
             }              
        },
        function(response){
            console.log(response)}
 
    )};
    $scope.get_data();

}]);


app.controller('requestListController',['$scope','$resource','$http',function($scope,$resource,$http){
    $scope.nextjrequesturlUrl;
    $scope.jrequesturl;
    $scope.requestList;
    var profile = angular.element(document.querySelector("call"));
//    var page=angular.element(document.querySelector("#page"));

    $scope.pk=profile.attr("pk")
    $scope.op=profile.attr("op")
    $scope.groupStauts=angular.element(document.querySelector("#groupStatus"))
       
    $scope.joinRequest = function(initialurl,pk,op){
        $scope.groupOp;
        if(!$scope.groupOp){
            $scope.groupOp=op
        }

        url=getBaseUrl+initialurl+$scope.groupOp+'/'+pk
        console.log(url)
        $http(
        {
        method:"GET",
        url:url,
          }
         ).then(
        function(response){
            if(response.data.op == 'send'){
                $scope.groupStauts.text('Cancel Request')
                $scope.groupOp='cancel'
            }            
            else if(response.data.op == 'cancel' ){
                $scope.groupStauts.text('Join Group')
                $scope.groupOp='send'
            }               
            else if(response.data.op == 'delete'){
                $scope.groupStauts.text('Join Group')
                $scope.groupOp='send'
            }            

    
           },

         function(response){
            console.log(response)}
 
    )}
    $scope.get_data = function(){
      
            op=$scope.op;
            pk=$scope.pk;


    if($scope.nextjrequesturlUrl){
        $scope.jrequesturl= $scope.nextjrequesturlUrl;
    }
    else{
        $scope.jrequesturl='/api/groups/requests';
        }
    $http({method:"GET",
          url:$scope.jrequesturl,
        params:{
           "op":op,
           "pk":pk,
                 },
          }).then(
        function(response){
        $scope.requestList = response.data.results
             console.log($scope.requestList)
            if(response.data.next){
                $scope.nextjrequesturlUrl=response.data.next
             }
            else{
                 document.querySelector("#jrloadmore").style.cssText="display : none"
             }             

 
        },
        function(response){
            console.log(response)}
 
    )};
    if(document.querySelector("#jrloadmore")){ 
    $scope.get_data();
    }
    }]);

//app.factory('Post',['$resourse','url',function($resourse,url){
//            var url = url;
//             return $resource(url,{},{
//              query:{
//               
//              },
//              get:{
//              
//             }
//             })
// 
//          
//}])
app.directive("posts",function(){
    return {
        templateUrl :function(params){
            return 'api/templates/'+params.name +'/post_list.html';
        } , 
        
    }
})
app.directive("pages",function(){
    return {
        templateUrl :function(params){
            return 'api/templates/'+params.name +'/page_list_item.html';
        } , 
        
    }
})
app.directive("groups",function(){
    return {
        templateUrl :function(params){
            return 'api/templates/'+params.name +'/group_list_item.html';
        } , 
        
    }
})
app.directive("profileimgs",function(){
    return {
        templateUrl :function(params){
            return 'api/templates/'+params.name +'/profile_img_item.html';
        } , 
        
    }
})
app.directive("jrequests",function(){
    return {
        //templateUrl :'api/templates/jrequests_list.html'
        template:  '<div ng-repeat="r in requestList">{{r.user.username}} | {{r.created_at}} <hr/><a  href="#" ng-click="joinRequest(\'api/groups/\', r.group.pk ,\'confirm\')" > <span id="adminGroupStatus">Confirm </span><a  href="#" ng-click="joinRequest(\'api/groups/\', r.group.pk ,\'delete\')" > <span id="adminGroupStatus">Delete </span></div>'
        
    }
})
