var app=angular.module("app",["ngRoute","ngResource"]);

app.config(function($locationProvider ,$routeProvider){
    //$locationProvider.html5Mode({enabled:true})
    $routeProvider

     .when("/pages/:pageSlug/",{
        templateUrl:'/api/templates/post-list.html',
        controller:"myController"
    })
        
 
    

});



app.service("cityService",function(){
    this.city="aden";

})

app.controller("myController",["$scope","cityService","$http","$routeParams",function($scope,cityService,$http,$routeParams){
        $scope.city=cityService.city;
        $scope.posts;
        $scope.$watch("city",function(){
                cityService.city=$scope.city;
                });
    
    $scope.pageSlug=$routeParams.pageSlug;
    $scope.postUrl='/api/posts/'+$scope.pageSlug;
    $scope.posts;
    

$scope.postUrl='/api/posts/';

$http.get($scope.postUrl)
    .then(function(results){
    $scope.posts=results.data.results
    console.log("fetchhing")
    console.log($scope.posts)
    //console.log(results.data.results[0].id)
    //.log(results.data.results.length)


});
   
console.log("jjjjj")

    
}]);
app.controller("mainController",["$scope","cityService","$http","$routeParams",function($scope,cityService,$http,$routeParams){
        $scope.$watch("city",function(){
                cityService.city=$scope.city;
                });
    
    $scope.pageSlug=$routeParams.pageSlug;
    $scope.postUrl='/api/posts/'
    $scope.posts;
    


$http.get($scope.postUrl)
    .then(function(results){
    $scope.posts=results.data.results
    console.log("fetchhing")
    console.log($scope.posts)
    //console.log(results.data.results[0].id)
    //.log(results.data.results.length)


});
   
console.log("jjjjj")

    
}]);
app.controller("controller",["$scope","cityService",function($scope,cityService){
            $scope.city=cityService.city;

    
}])
