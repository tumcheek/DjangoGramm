$('.like').click(function(){
      $.ajax({
               type: "POST",
               url: $('#like_form').data('url'),
               data: {'pk': $(this).parent().parent().parent().data('post'), 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()},
               dataType: "json",
               context: this,
               success: function(response) {
               if(response.is_liked){
                    $(this).text('Unlike')
               }else{
                    $(this).text('Like')
               }
                    $(this).toggleClass('btn-success');
                    $(this).toggleClass('btn-danger');
                    $(this).next(".count_likes").text(response.likes_count + " Likes");
                },
                error: function(rs, e) {


                }
          });
    })

$('.bookmark').click(function(){
      $.ajax({
               type: "POST",
               url: $('#bookmark_form').data('url'),
               data: {'pk': $(this).parent().parent().parent().data('post'), 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()},
               dataType: "json",
               context: this,
               success: function(response) {
               if(response.is_bookmark){
                    $(this).text('Remove bookmark')
               }else{
                    $(this).text('Bookmark')
               }
                    $(this).toggleClass('btn-success');
                    $(this).toggleClass('btn-danger');

                },
                error: function(rs, e) {


                }
          });
    })

$('.add_new_tag').click(function(){
      $.ajax({
               type: "POST",
               url: $('#new_tag_form').data('url'),
               data: {'pk': $(this).parent().parent().data('post'),
               'tags':$(this).prev().val(),
               'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()},
               dataType: "json",
               context: this,
               success: function(response) {
                console.log(response['tags'])

                for(i=0; i<response['tags'].length; i++){
                    if(response['tags'][i][0]=='#'){
                        let tag = response['tags'][i].slice(1)
                        $(this).parent().parent().find('.post_tags').append(` <span class="tags">#${tag}</span>`)
                    }else{
                        $(this).parent().parent().find('.post_tags').append(` <span class="tags">#${response['tags'][i]}</span>`)
                    }

                }


                },
                error: function(rs, e) {

                }
          });
    })