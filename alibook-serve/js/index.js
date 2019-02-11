function load_json_data(id,parent_id){
    var html_code = '';
   $.ajax({
    url:'/api/posts/cat/',


    method:"GET",
    success:function(data){
        //catList = data.results;
 
        html_code='<option value="">'+id+'</option>';
        $.each(data,function(key,value){
            if(id == 'category'){
                if(value.parent_code =='0'){
                       html_code +='<option value="'+value.code+'">'+value.name+'</option>';

                }
            }else{
                if(value.parent_code == parent_id){
            html_code +='<option value="'+value.code+'">'+value.name+'</option>';
            
                }
            }
            
        });
        
        $('#'+id).html(html_code)

    },
    error:function(data){
        console.log('error')
        console.log(data)

    }
})
    
}
$(document).on('change','#category',function(){
    var cat_id =$(this).val()
    if(cat_id != '')
        {
           load_json_data('subcategory',cat_id) 
        }
    else
    {
        $('#subcategory').html('<option value=""> subcategory</option>');
        $('#brand').html('<option value=""> Brand</option>');
    }
    
});
$(document).on('change','#subcategory',function(){
    var sub_cat_id =$(this).val()
    if(sub_cat_id != '')
        {
           load_json_data('brand',sub_cat_id) 
        }
    else
    {
        $('#brand').html('<option value="">Select Brand</option>');
    }
    
});
    
function load_json_data_create(id,parent_id){
    var html_code = '';
   $.ajax({
    url:'/api/posts/cat/',


    method:"GET",
    success:function(data){ 
        html_code='<option value="">'+"All"+'</option>';
        $.each(data,function(key,value){
            if(id == 'id_category'){
                if(value.parent_code =='0'){
                       html_code +='<option value="'+value.code+'">'+value.name+'</option>';

                }
            }else{
                if(value.parent_code == parent_id){
            html_code +='<option value="'+value.code+'">'+value.name+'</option>';
            
                }
            }
            
        });
        
        $('#'+id).html(html_code)
        

    },
    error:function(data){
        console.log('error')
        console.log(data)

    }
})
    
}
$(document).on('change','#id_category',function(){
    var cat_id =$(this).val()
    if(cat_id != '')
        {
           load_json_data_create('id_subcategory',cat_id) 
        }
    else
    {
        $('#id_subcategory').html('<option value=""> subcategory</option>');
        $('#id_brand').html('<option value=""> Brand</option>');
    }
    
});
$(document).on('change','#id_subcategory',function(){
    var sub_cat_id =$(this).val()
    if(sub_cat_id != '')
        {
           load_json_data_create('id_brand',sub_cat_id) 
        }
    else
    {
        $('#id_brand').html('<option value="">Select Brand</option>');
    }
    
});
   function load_json_data_add_post(id,parent_id){
    var html_code = '';
   $.ajax({
    url:'/api/posts/cat/',


    method:"GET",
    success:function(data){ 
        html_code='<option value="">'+"All"+'</option>';
        $.each(data,function(key,value){
            if(id == 'product_category'){
                if(value.parent_code =='0'){
                       html_code +='<option value="'+value.code+'">'+value.name+'</option>';

                }
            }else{
                if(value.parent_code == parent_id){
            html_code +='<option value="'+value.code+'">'+value.name+'</option>';
            
                }
            }
            
        });
        
        $('#'+id).html(html_code)
        

    },
    error:function(data){
        console.log('error')
        console.log(data)

    }
})
    
}
$(document).on('change','#product_category',function(){
    var cat_id =$(this).val()
    if(cat_id != '')
        {
           load_json_data_add_post('product_subcategory',cat_id) 
        }
    else
    {
        $('#product_subcategory').html('<option value=""> subcategory</option>');
        $('#post_brand').html('<option value=""> Brand</option>');
    }
    
});
$(document).on('change','#product_subcategory',function(){
    var sub_cat_id =$(this).val()
    if(sub_cat_id != '')
        {
           load_json_data_add_post('post_brand',sub_cat_id) 
        }
    else
    {
        $('#post_brand').html('<option value="">Select Brand</option>');
    }
    
});
    
    
    
    
function getParameterByname(name,url){
        if(!url){
            url = window.location.href;
        }
        name = name.replace(/[\[\]]/g,"\\$&");
        var regex = new RegExp("[?&]"+name+"(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g," "));
    }
function loadTweetContainer(tweetContainerId,fetchOne){
        var tweetList =[];
    var nextTweetUrl;
    var tweetContainer;
    if (tweetContainerId){
           tweetContainer=$("#"+tweetContainerId);
  
    }else{
           tweetContainer=$("#posts-container");


    }
    var initialtUrl=tweetContainer.attr("data-url")||"/api/posts/";
    var query = ''
    var content = ''
    var use = ''
    var category =''
    var cat =''
    var subcategory =''
    var brand =''
    var price = ''
    var gender =''
    var city =''
    var country =''
    var page_type =''
    var desc =''
    var code =''
    var street =''
    var shop_list =false;

   var getUrl =window.location;   
   var getBaseUrl =getUrl.protocol+"//"+getUrl.host+"/"+getUrl.pathname.split('/')[0];   

 
function formatTweet(value){
                var verb ="Like"
                var preContent="";
                var container;
                var tweetContent;
                var post_img='';
                var edit=''
                var images=''
                var loc=''
                if(value.is_owner){
                    edit="<a class='btn btn-primary' href='"+getBaseUrl+"posts/"+value.pk+"/update/'>Edit</a><a class='btn btn-danger' href='"+getBaseUrl+"posts/"+value.pk+"/delete/"+value.page.name+"/'>Delete</a>"
                } 
                  if(value.image){
                    post_img ="<img src='"+value.image+"' id='post-img' class=' img-responsive'>"
                    images= "image-url='"+value.image+"'";
                    if(value.image2){
                        images+="image2-url='"+value.image2+"'"

                    }
                    if(value.image3){
                        images+="image3-url='"+value.image3+"'"

                    }
                    if(value.image4){
                        images+="image4-url='"+value.image4+"'"

                    }
                }else{
                    post_img ="<img src='"+value.image+"' id='post-img' class=' img-responsive'>"
                }
                if(shop_list){
                    if(value.country){loc+=value.country}
                    if(value.city){loc+= "  "+value.city}
                    if(value.street){loc+= "  "+value.street}

                    tweetContent ="<div class='col-md-4 col-sm-6 col-xs-12 padleft-right'><figure class='imghvr-fold-up'>"+post_img+
                    "<figcaption><h3>"+value.name+"</h3><p>"+value.description+ "</p><p>"+loc+ "</p><p>Phone : "+value.phone+ "</p></figcaption><a href='"+getBaseUrl+value.name+"'></a></figure></div>"
                    
                }else{
                     if(value.page.country){loc+=value.page.country}
                    if(value.page.city){loc+= "  "+value.page.city}
                    if(value.page.street){loc+= "  "+value.page.street}
                       
                tweetContent ="<div class='col-md-4 col-sm-6 col-xs-12 padleft-right'><figure class='imghvr-fold-up'>"+post_img+
                    "<figcaption><h3>"+value.price+" "+value.currency+" </h3><p>"+value.content+ "</p><p>"+value.description+ "</p><p>Product Code : "+value.pk+ "</p>"+loc + "</p</figcaption><a href='"+getBaseUrl+value.page.name+"'></a></figure>"+edit+"<a   class= 'btn btn-primary showslide'"+ images+"'>Preview</a> </div>"
                
                    }
             
                container = tweetContent
          
    return container
                
    
}
function attachTweet(value,prepend){
                var formattedHtml;
                
                formattedHtml = formatTweet(value)
                if (prepend ==true){
                       tweetContainer.prepend(formattedHtml)

                }
                else {
                       tweetContainer.append(formattedHtml)
   

                }
    
    }
function parseTweet(){
                        if(tweetList[0]){ 
                        if(tweetList[0].is_page ){
                            shop_list=true;
                            }else{
                                shop_list=false;
                            }}
                        if(tweetList == 0){
                            tweetContainer.append("<h2>No Results Found</h2>")

                        }else{
                            $.each(tweetList,function(key,value){
                                 attachTweet(value) 
                              
                            })
                        }
    }
function fetchTweets(url){
                    var fetchUrl;
                    if(!url){
                        fetchUrl= initialtUrl

                    }else{
                        fetchUrl=url
                    }

                           $.ajax({
                            url:fetchUrl,
                            data:{
                                "content":content,
                                "category":category,
                                "subcategory":subcategory,
                                "brand":brand,
                                "price":price,
                                "cat":cat,
                                "country":country,
                                "city":city,
                                "page_type":page_type,
                                "desc":desc,
                                "use":use,
                                "code":code,
                                "street":street,
                                "gender":gender
                            },
    
                            method:"GET",
                            success:function(data){
                                tweetList = data.results;
                                if(data.next){
                                nextTweetUrl=data.next
                                }else{
                                    $("#loadmore").css("display","none")
                                }
                                parseTweet()

                            },
                            error:function(data){
                                console.log('error')
                                console.log(data)

                            }
                        })
        
    }

 
    fetchTweets()
 

$("#loadmore").click(
        function(event){
            event.preventDefault()
            if(nextTweetUrl){
                fetchTweets(nextTweetUrl)
            }
    
})

 $("#search-shop").submit(function(event){
        event.preventDefault()
        category=$("#search-shop #category").val()
        subcategory=$("#search-shop #subcategory").val()
        brand=$("#search-shop #brand").val()
        gender=$("#search-shop #id_gender").val()
        use=$("#search-shop #id_use").val()
        content=$("#search-shop #id_content").val()
        price=$("#search-shop #id_price").val() 
        code=$("#search-shop #id_code").val() 
        street=$("#search-shop #id_street").val() 
     
  
     //search shops
        desc=$("#search-shop #id_page_name").val()
        cat=$("#search-shop #id_cat").val()
        country=$("#search-shop #id_country").val()
        city=$("#search-shop #id_city").val()
    
        page_type=$("#search-shop #id_page_type").val()
             
        console.log('category')
        console.log(category)
        tweetContainer.empty()
        //var url ='?content='+content+'&price='+price
      fetchTweets()

    }) 
$(document).on('click','.showslide',function(event){

        event.preventDefault()
        e=$(this) ;

    $("#slider-images").empty()
    $("#slider-images").append('<div class="item active"><img id="firsts" alt=""/></div>' )
    $("#firsts").attr('src',e.attr("image-url"))
    if(e.attr("image2-url")){
    $("#slider-images").append( "<div class='item'><img src='"+e.attr("image2-url") +"' alt=''/></div>")
    }
    if(e.attr("image3-url")){
    $("#slider-images").append( "<div class='item'><img src='"+e.attr("image3-url") +"' alt=''/></div>")
    }    
    if(e.attr("image4-url")){
    $("#slider-images").append( "<div class='item'><img src='"+e.attr("image4-url") +"' alt=''/></div>")
    }
    $("#slidemodel").modal("show")

    }) 
   
    

}

    
    
    
    

 