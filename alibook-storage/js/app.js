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
    .when('/posts/:pk',{
        templateUrl :function(params){
            return 'api/templates/'+params.pk +'/post.html';
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
    .when('/accounts/reset/:uid/:token',{
        templateUrl :function(params){
            return 'api/templates/'+params.uid +'/password_confirm.html';
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
    
    .when('/password_reset',{
        templateUrl :function(params){
            return 'api/templates/'+params.pk +'/password_reset.html';
        }
         ,
     })    
    .otherwise({
        template  : 'Not Found' })
}).run(function($cookies, $rootScope, $http) {
  	if ($cookies.get('token')) {
      $http.defaults.headers.common['Authorization'] = 'Token ' + $cookies.get('token');
    } else {
        $("#loginModal").modal('show')    }
  });

app.config([
    '$httpProvider',function($httpProvider){
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        
    }
]);

var getUrl =window.location;   

var getBaseUrl =getUrl.protocol+"//"+getUrl.host+"/"+getUrl.pathname.split('/')[0];   
//
//function getCookie(name) {
//var cookieValue = null;
//if (document.cookie && document.cookie !== '') {
//var cookies = document.cookie.split(';');
//for (var i = 0; i < cookies.length; i++) {
//var cookie = jQuery.trim(cookies[i]);
//// Does this cookie string begin with the name we want?
//if (cookie.substring(0, name.length + 1) === (name + '=')) {
//cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//break;
//}
//}
//}
//return cookieValue;
//}
//var csrftoken = getCookie('csrftoken');

app.service('searchService',[function(){
    this.searchList=[];
    this.searchListPage=[];
    this.searchListGroup=[];
    this.searchListPost=[];
    this.messageList=[];
    this.loggedIn=false;
    
}])
app.controller('searchController',['$scope','searchService','$cookies','$location','$http','$rootScope',function($scope,searchService,$cookies,$location,$http,$rootScope){
        $scope.searchList= searchService.searchList;
        $scope.searchListGroup= searchService.searchListGroup;
        $scope.searchListPage= searchService.searchListPage;
        $scope.searchListPost= searchService.searchListPost;
   
}]);
app.controller('resetController',['$scope', '$routeParams', '$http' ,function($scope, $routeParams, $http ){
    
        $scope.resetPasswordValue = {};
        $scope.confirmPasswordValue = {};

        $scope.resetPassword= function(){
                var url="/rest-auth/password/reset/"
           

        $http(
            {
            method:"POST",
            url:url,
            data:{
                    'email':$scope.resetPasswordValue.email
                }
            }
             ).then(
            function(response){
                 console.log(response.data )
                $("#confirmPasswordError").text(response.data.detail)

               },

             function(response){
                console.log(response)
             }

        ) 
        };
        $scope.confirmResetPassword= function(uid,token,password1,password2){
                var url="/rest-auth/password/reset/confirm/"

        if($scope.confirmPasswordValue.password1 == $scope.confirmPasswordValue.password2){
        $http(
            {
            method:"POST",
            url:url,
            data:{
                    'uid': $routeParams.uid,
                    'token': $routeParams.token,
                    'new_password1': $scope.confirmPasswordValue.password1,
                    'new_password2': $scope.confirmPasswordValue.password2                }
            }
             ).then(
            function(response){
                 console.log(response )
               },

             function(response){
                console.log(response)
                 $("#confirmPasswordError").text("")
                 $("#confirmPasswordError").text(response.data.new_password2)
                 $("#confirmPasswordError").text(response.data.detail)
                 $("#confirmPasswordError").text(response.data.token +" for token ,Link must be Expired")
             }

        )}else{
        $("#confirmPasswordError").text('Passwords Must Match')

        } 
            
    
       
        };
    
   
}]);
app.controller('postDetailController',['$scope','searchService','$cookies','$location','$http','$rootScope',function($scope,searchService,$cookies,$location,$http,$rootScope){
    
        $scope.postDetail;
        var postID=angular.element(document.querySelector("post"));
        $scope.pk =postID.attr('pk');
        $scope.get_post= function(){
                var url='/api/posts/'+$scope.pk+'/'
                console.log(url)

        $http(
            {
            method:"GET",
            url:url,
            }
             ).then(
            function(response){
                 console.log(response.data)
                $scope.postDetail=response.data[0];
               },

             function(response){
                console.log(response)
             }

        ) 
        };
    $scope.get_post();
    
   
}]);
app.controller('inboxController',['$scope','searchService','$cookies','$location','$http','$rootScope',function($scope,searchService,$cookies,$location,$http,$rootScope){
//        $scope.messageList= searchService.messageList;
    var requestUser;

     $scope.loggedIn=searchService.loggedIn;
     $scope.conversation=[];
     $scope.to_userID;
      $scope.to_userName='';
    $scope.delete_message=function(pk=0){
       var url='/api/chat/delete/'+pk+'/'

        console.log(url)
        $http(
            {
            method:"DELETE",
            url:url,
              }
             ).then(
            function(response){
                console.log(response)

               },

             function(response){
                console.log(response)}

        ) 
    }
    $scope.delete_conversation=function(pk=0){
        var url='/api/chat/con/delete/'+pk+'/hide/' 

        console.log(pk)
        
    $http(
        {
        method:"GET",
        url:url,
          }
         ).then(
        function(response){
             console.log(response)  
           },

         function(response){
            console.log(response)}
 
    ) 
        
    }
    $scope.get_conversation=function(fusername,tusername){

        var url='/api/chat/conversation/'+fusername+'/'+tusername+'/'

        $http(
            {
            method:"GET",
            url:url,
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
    if($scope.loggedIn){ 
     $scope.get_conversations()
    }
    $scope.message={};
    $scope.sendMessage=function(pk=0){
        var url='/api/chat/create/'+pk+'/'

        console.log(url)
        $http(
            {
            method:"POST",
            url:url,
            data:$scope.message,
              }
             ).then(
            function(response){
                console.log(response)
            $scope.conversation.unshift(response.data)

                $("#msgContent").val("")


               },

             function(response){
                console.log(response)}

        ) 

    };
   
}]);

app.controller('rightController',['$scope','$cookies','$location','$http','$rootScope',function($scope,$cookies,$location,$http,$rootScope){
        var currentUserNameContainer= angular.element(document.querySelector("call"));
    $scope.currentUserName =currentUserNameContainer.attr('username')
   if ($scope.currentUserName == $cookies.get("username")){
       $scope.owner=true;
   }else{
       $scope.owner=false;

   }
    $scope.message={};
    $scope.sendMessage=function(pk=0){
        var url='/api/chat/create/'+pk+'/'
        $http(
            {
            method:"POST",
            url:url,
            data:$scope.message,
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
        $scope.$watch('loggedIn',function(){
            searchService.loggedIn=$scope.loggedIn;
            if($scope.loggedIn ==true){
                 $scope.get_messages();
             $scope.loggedInUsername =$cookies.get("username");

            }else{         $scope.loggedInUsername =$cookies.remove("username");

            }
        });
        $scope.actionList;
        $scope.user={};
        $scope.signup={};

         //verify token
         $scope.loggedIn=false;
         $scope.loggedInUsername =$cookies.get("username");
        var tokenExists = $cookies.get("token")
        if(tokenExists){
            $scope.loggedIn=true;
        }
        $scope.login=function(user){
             var url='/api/accounts/login/'
              $http(
                 {
                 method:"POST",
                 url:url,
                 data:$scope.user,
                 }
                  ).then(
                 function(response){
                  console.log(response)
                  $cookies.put("token",response.data.token)
                  $cookies.put("username",user.username)
                $scope.loggedIn=true;
                    $("#loginModal").modal('hide')

                  $location.path('/')
                    },

                  function(response){
                     console.log(response)
                  }

             )
        }
        $scope.logout=function(user){
             var url='/api/accounts/logout/'
              $http(
                 {
                 method:"POST",
                 url:url,
                 }
                  ).then(
                 function(response){
                  console.log(response)
                  $cookies.remove("token")
                  $cookies.remove("username")
                $scope.loggedIn=false;
                  $location.path('/')
                    },

                  function(response){
                     console.log(response)
                  }

             )
        }        
        $scope.chpassword={};
        $scope.changePassword=function(chpassword){
             var url='/api/accounts/change_password/'
             if($scope.chpassword.password ==$scope.chpassword.password1){ 

              $http(
               {
                 method:"POST",
                 url:url,
                 data:$scope.chpassword ,
                 }
                  ).then(
                 function(response){
                  console.log(response)

                    $("#changePasswordModal").modal('hide')

                  $location.path('/')
                    },

                  function(response){
                     console.log(response)
                  }

             )
             }else{
                 $("#changePasswordModal #changePasswordError").text('Passwords Must Match')

             }
        }
//        };                $scope.user={};
//        $scope.signup={};
//        var tokenExists= $cookies.get("token")
//        if(tokenExists){
//         //verify token
//         $scope.loggedIn=true;
//         $cookies.remove("token")
//         $scope.user.username=$cookies.get("username")
//        }
//        $scope.login=function(){
//             var url='/api/accounts/login/'
//             
//             $http(
//                 {
//                 method:"POST",
//                 url:url,
//                 data:$scope.user,
////                  headers:{"X-CSRFToken":csrftoken},
//                 }
//                  ).then(
//                 function(response){
//                  $cookies.put("token",response.data.token)
//                  $cookies.put("username",$scope.user.username)
//                  $location.path('/')
//                  console.log(response.data.token)
//                    },
//
//                  function(response){
//                     console.log(response)
//                  }
//
//             )         
//        };        
       $scope.registerUser=function(){
             var url='/api/accounts/signup/'
             console.log($scope.signup)
             if($scope.signup.password1 ==$scope.signup.password2 ){
                   $scope.signup.password =$scope.signup.password2;
             
                  $http(
                      {
                      method:"POST",
                      url:url,
                      data:$scope.signup,
                      }
                       ).then(
                      function(response){
                          console.log(response.data)
                        $("#signupModal").modal('hide')
                            $location.path('/')
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
            }
             ).then(
            function(response){
                $scope.actionList=response.data;
                  
                 console.log(response.data.results)
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
    

    
}]);

app.controller('photoController',['$scope',  '$resource','$http',function($scope, $resource,$http){
    $scope.comment={}  
    
 
    $scope.AddComment=function(pk,op){
      
    var url="/api/comments/create/"+op+"/"+pk
console.log('urrrrr')
console.log(url)
    $http(
        {
        method:"POST",
        url:url,
        data:$scope.comment[pk],
          }
         ).then(
        function(response){
            if(op=='commentpicture'){  
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
    
    
    $scope.c ={}
    $scope.postsLikes ={}
    $scope.commetnsLikes ={}
    $scope.ncurl ={}
    $scope.reply ={}
    $scope.nreplyurl ={}
        
    $scope.get_comments=function(pk,op){
        var url="/api/comments/"+op+"/"+pk
        console.log(url)
        if(op == 'commentpicture'){ 

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
                if(op == 'commentpicture'){ 
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
    $scope.profileimgList;
    $scope.photo;
    $scope.likeBtn = angular.element(document.querySelector("#likeBtn"));
 
    $scope.likePicture=function(url,pk){
        var likedUrl =getBaseUrl+url+pk+'/like/'
        console.log(likedUrl)
        console.log(url)
    $http(
        {
        method:"GET",
        url:likedUrl,
          }
         ).then(
        function(response){ 
         if(url='api/comments/'){
            if(response.data.liked){
                angular.element(document.querySelector("#commentLike"+pk)).text('Unlike')
            }else{
                angular.element(document.querySelector("#commentLike"+pk)).text('Like')
            }
         }else{
             
       
         if(response.data.liked){
                $scope.likeBtn.text("Unlike") 
            }else{
                 $scope.likeBtn.text("Like")
            }
               }
           },

         function(response){
            console.log(response)}
 
    )
    }
    $scope.photoClicked=function(photo){
          
        $scope.photo=photo;
    };
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
app.controller('adminListController',['$scope', '$location',  '$resource','$http',function($scope, $location,$resource,$http){
    
    var objectType=angular.element(document.querySelector("call"));
    $scope.pk =objectType.attr('pk');
    $scope.op =objectType.attr('op');
    $scope.pageAdmin={}

    
    $scope.ToggleAdmin=function(username){
        var name = username;
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

app.controller('leftSideController',['$scope', '$cookies','$location', '$resource','$http',function($scope,$cookies, $location,$resource,$http){

    $scope.files=[]; 
    
    $scope.owner=false;
 $scope.currentUserName= angular.element(document.querySelector("call")).attr('username')
   if ($scope.currentUserName == $cookies.get("username")){
       $scope.owner=true;
   }else{
       $scope.owner=false;

   }
    
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
                       headers:{'Content-Type':undefined},
                       transformRequest:angular.identity,
                       }).then(
                        function(response){
                         $scope.files=[]
                        $scope.img_new= response.data.img;
                            $location.path('/accounts/'+$scope.currentUserName+'/')

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
          }
         ).then(
        function(response){
            
            console.log(response.data.op)
            if(response.data.op == 'send'){
                $scope.friendStatus.text('Cancel Request')
                $scope.friendOp='cancel'
            } 
            else if(response.data.op == 'cancel'){
                $scope.friendStatus.text('Add Friend')
                $scope.friendOp='send'


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
app.controller('postListController',['$scope','searchService','$cookies', '$resource','$http',function($scope,searchService,$cookies, $resource,$http){
    var currentUserNameContainer= angular.element(document.querySelector("call"));
    $scope.currentUserName =currentUserNameContainer.attr('username')
    $scope.loggedInUsername = $cookies.get("username")
   if ($scope.currentUserName ==$scope.loggedInUsername ){
       $scope.owner=true;
   }else{
       $scope.owner=false;

   }     

        $scope.postDetail;
        var postID=angular.element(document.querySelector("post"));
        $scope.postPk =postID.attr('pk');
        $scope.get_post= function(){
                var url='/api/posts/'+$scope.postPk+'/'

                $http(
                    {
                    method:"GET",
                    url:url,
                    }
                     ).then(
                    function(response){
                         console.log(response.data)
                        $scope.postDetail=response.data[0];
                       },

                     function(response){
                        console.log(response)
                     }

                ) 
        };
   
    
   
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
                       headers:{'Content-Type':undefined},
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
 $scope.editpost={};
 $scope.getPostPK=function(ppk=0 ,parentid=0){
  $scope.ppk=ppk;
  $scope.parentpk=parentid;
 }
 $scope.editPost=function(genre){
     var url;
     var mymodal;
        if(genre =='post')
        {   url='/api/posts/'+$scope.ppk+'/'
            mymodal ='#editPostModal'
       }else{
            url='/api/comments/'+$scope.ppk+'/'
            mymodal ='#editCommentModal'
       }
        var postType=angular.element(document.querySelector(".post-form")).attr('postType');
        var fileType=angular.element(document.querySelector(".post-form")).attr('fileType');

    $http(
        {
        method:"PUT",
        url:url,
        data:$scope.editpost,
          }
         ).then(
        function(response){
            
            if(!$scope.postList){
               $scope.postList=[] 
            }
            
            if(genre =='post'){ 
             $scope.postList.unshift(response.data)
            }else if(genre =='comment'){
                 $scope.c[$scope.parentpk].unshift(response.data)

            }else if(genre =='reply'){
                 $scope.reply[$scope.parentpk].unshift(response.data)
                 mymodal ='#editReplyModal'

            }
            $(mymodal).modal("hide")
               
           },

         function(response){
            console.log(response)}
 
    ) 

    }; 
    $scope.deletePost=function(genre){
        if(genre =='post')
        {        var url='/api/posts/'+$scope.ppk+'/'
       }else{
            var url='/api/comments/'+$scope.ppk+'/'
       }       
        var postType=angular.element(document.querySelector(".post-form")).attr('postType');
        var fileType=angular.element(document.querySelector(".post-form")).attr('fileType');

    $http(
        {
        method:"DELETE",
        url:url,
          }
         ).then(
        function(response){
            
  
               
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
       
       console.log(likedUrl)

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
    if($scope.postPk){
         $scope.get_post();
    }else{
            $scope.get_data();

    }
$scope.loggedIn=searchService.loggedIn;
    $scope.$watch('loggedIn',function(){
            searchService.loggedIn=$scope.loggedIn;
            if($scope.loggedIn ==true){
 
    if($scope.postPk){
         $scope.get_post();
    }else{
            $scope.get_data();

    }
            }
        });

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
            return 'api/templates/'+params.name +'/photo.html';
        } , 
        
    }
})
app.directive("jrequests",function(){
    return {
        //templateUrl :'api/templates/jrequests_list.html'
        template:  '<div ng-repeat="r in requestList">{{r.user.username}} | {{r.created_at}} <hr/><a  href="#" ng-click="joinRequest(\'api/groups/\', r.group.pk ,\'confirm\')" > <span id="adminGroupStatus">Confirm </span><a  href="#" ng-click="joinRequest(\'api/groups/\', r.group.pk ,\'delete\')" > <span id="adminGroupStatus">Delete </span></div>'
        
    }
})

